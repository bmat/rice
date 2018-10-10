import json
from marshmallow import fields
from pydoc import locate
import importlib
from enum import Enum
from docutils.core import publish_doctree
import re
from marshmallow import Schema
import inspect
from marshmallow_enum import EnumField
from datetime import datetime

formats = {
    "json": json
}

# Add suppor for xml y the library is available
try:
    from dicttoxml import dicttoxml

    class Xml(object):
        @staticmethod
        def dumps(d):
            return dicttoxml(d, custom_root="data", attr_type=True)

    formats["xml"] = Xml
except ImportError:
    pass



# If you do a plugin, populate this with your own types and schemas (recommended by using the function register_model)
type_map = {
    str: fields.String(),
    int: fields.Integer(),
    float: fields.Float(),
    datetime: fields.DateTime(),
    None: fields.String()
}

reversed_type_map = {}


def register_model(model_class):
    if model_class not in type_map:
        type_map[model_class] = fields.Nested(model_class.Schema)
        reversed_type_map[model_class.Schema] = model_class


def get_doc_map(data_class):
    m = {}
    for dc in reversed(inspect.getmro(data_class)):
        if dc.__doc__ is not None:
            # Silence error: warning_stream
            doctree = publish_doctree(dc.__doc__, settings_overrides={"warning_stream": False}).asdom()
            lists = doctree.getElementsByTagName("definition_list_item")
            attributes = []

            for i in lists:

                if i.firstChild.tagName == "term" and i.firstChild.firstChild.nodeValue.startswith("Attributes"):
                    for p in i.getElementsByTagName("paragraph"):
                        attributes += ("".join([c.nodeValue for c in p.childNodes if c.nodeValue is not None])).split("\n")

            serializables = {}
            for i in attributes:
                result = re.match(r"([_0-9a-zA-Z]*) \((.*)\)", i)
                if result:
                    attrib_name = result.group(1)
                    attrib_options = result.group(2).split(", ")
                    if len(attrib_options) > 0:
                        attrib_type = attrib_options[0]
                        if "serializable" in attrib_options:
                            serializables[attrib_name] = attrib_type

            m.update(serializables)

    return m


def build_schema(serializables, module):
    schema_attrs = {}
    for var_name, var_type_name in serializables.items():
        if var_type_name == "serializable":
            schema_attrs[var_name] = fields.String()
        else:
            var_type = locate(var_type_name)
            is_list = False
            if var_type is None:
                if not isinstance(module, str):
                    module = module.__module__
                m = importlib.import_module(module)
                if var_type_name[0] == "[" and var_type_name[-1] == "]":
                    is_list = True
                    var_type = getattr(m, var_type_name[1:-1])
                else:
                    var_type = getattr(m, var_type_name)

            if issubclass(var_type, Enum):
                schema_attrs[var_name] = EnumField(var_type)
            else:
                if var_type not in type_map:
                    m = get_doc_map(var_type)

                    schema = build_schema(m, var_type)
                    var_type.Schema = schema
                    register_model(var_type)
                if is_list:
                    schema_attrs[var_name] = fields.List(type_map[var_type])
                else:
                    schema_attrs[var_name] = type_map[var_type]

    schema_class = type("SchemaClass", (Schema,), schema_attrs)
    return schema_class


def serialize(data_object, format='json'):

    if format in formats:
        m = get_doc_map(data_object.__class__)
        Schema = build_schema(m, data_object.__module__)
        schema = Schema()
        data = {}
        for i in schema.declared_fields.keys():
            data[i] = getattr(data_object, i, None)
        dump = schema.dump(data)
        return formats[format].dumps(dump.data)

    else:
        raise Exception("Format '{format}' not supported".format(format=format))


def deserialize(string, object_class, format='json'):
    if format in formats:
        m = get_doc_map(object_class)
        Schema = build_schema(m, object_class.__module__)
        schema = Schema()

        if isinstance(string, str):
            data = formats[format].loads(string)
            loaded_data = schema.load(data).data
        else:
            loaded_data = string
        mod = importlib.import_module(object_class.__module__)
        for key, value in loaded_data.items():
            if isinstance(value, list):
                sub_type = m[key][1:-1]
                elements = []
                for sub_element in value:
                    sub_type_class = getattr(mod, sub_type)
                    elements.append(deserialize(sub_element, sub_type_class))

                loaded_data[key] = elements
            elif isinstance(value, dict):
                sub_type_class = getattr(mod, m[key])
                element = deserialize(value, sub_type_class)
                loaded_data[key] = element
        return object_class(**loaded_data)

    else:
        raise Exception("Format '{format}' not supported".format(format=format))

