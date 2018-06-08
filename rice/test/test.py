import unittest
from rice.test.model import SimpleClass, NestedClass, WithEnum, WithEnumNested, UserEnum, ListClass
from rice import serialize, deserialize
import json


class TestSerialize(unittest.TestCase):

    def test_simple(self):
        d = {
            "name": "foo",
            "number": 23
        }

        data_class = SimpleClass()
        data_class.name = d["name"]
        data_class.number = d["number"]

        dumped = json.loads(serialize(data_class))
        self.assertDictEqual(d, dumped)

        deserialized = deserialize(json.dumps(dumped), SimpleClass)

        self.assertEqual(data_class.name, deserialized.name)
        self.assertEqual(data_class.number, deserialized.number)

    def test_nested(self):
        d = {
            "simple": {
                "name": "foo",
                "number": 23
            },
            "name": "bar"
        }

        data_class = SimpleClass()
        data_class.name = "foo"
        data_class.number = 23
        nested_class = NestedClass()
        nested_class.name = "bar"
        nested_class.simple = data_class

        dumped = json.loads(serialize(nested_class))
        self.assertDictEqual(d, dumped)

        deserialized_nested = deserialize(json.dumps(dumped), NestedClass)

        self.assertEqual(nested_class.simple.name, deserialized_nested.simple.name)
        self.assertEqual(nested_class.simple.number, deserialized_nested.simple.number)

    def test_enum(self):

        d = {
            "name": "pepe",
            "user_type": "ADMIN"
        }
        we = WithEnum()
        we.name = "pepe"
        we.user_type = UserEnum.ADMIN

        dumped = json.loads(serialize(we))
        self.assertDictEqual(d, dumped)

        deserialized = deserialize(json.dumps(dumped), WithEnum)
        self.assertEqual(deserialized.user_type, we.user_type)
        self.assertEqual(deserialized.name, we.name)

    def test_enum_nested(self):

        d = {
            "name": "super",
            "user_type": "USER",
            "other_enum": {
                "name": "pepe",
                "user_type": "ADMIN"
            }
        }
        we = WithEnum()
        we.name = "pepe"
        we.user_type = UserEnum.ADMIN

        wen = WithEnumNested()
        wen.name = "super"
        wen.user_type = UserEnum.USER
        wen.other_enum = we

        dumped = json.loads(serialize(wen))
        self.assertDictEqual(d, dumped)

        deserialized = deserialize(json.dumps(dumped), WithEnumNested)
        self.assertEqual(deserialized.user_type, wen.user_type)
        self.assertEqual(deserialized.name, wen.name)

        self.assertEqual(deserialized.other_enum.user_type, we.user_type)
        self.assertEqual(deserialized.other_enum.name, we.name)

    def test_list(self):
        d = {
            "simple": {
                "name": "pepe",
                "number": 45
            },
            "simples": [{
                "name": "yolo",
                "number": 33,
            }, {
                "name": "ozelui",
                "number": 11,
            }]
        }

        sl = ListClass(
            simple=SimpleClass("pepe", 45),
            simples=[
                SimpleClass("yolo", 33),
                SimpleClass("ozelui", 11)
            ]
        )

        dumped = json.loads(serialize(sl))
        self.assertDictEqual(d, dumped)

        deserialized = deserialize(json.dumps(dumped), ListClass)
        self.assertEqual(sl.simple.name, deserialized.simple.name)
        self.assertEqual(len(sl.simples), len(deserialized.simples))
        self.assertEqual(sl.simples[1].number, deserialized.simples[1].number)


if __name__ == '__main__':
    unittest.main()
