from enum import Enum


class SimpleClass(object):
    """Attributes:
            name (str, serializable): Description of name
            number (int, optional, serializable): Description of number
            no_serializable (float): Item not serializable
        """
    def __init__(self, name=None, number=None):
        self.name = name
        self.number = number
        self.no_serializable = 67


class ListClass(object):
    """Attributes:
            simple (SimpleClass, serializable): Description of simple
            simples ([SimpleClass], serializable): Description of name
        """
    def __init__(self, simple=None, simples=[]):
        self.simple = simple
        self.simples = simples

class NestedClass(object):
    """Attributes:
            simple (SimpleClass, serializable): Description of simple
            name (str, serializable): Description of name
        """
    def __init__(self, simple=None, name=None):
        self.simple = simple
        self.name = name

class UserEnum(Enum):
    USER = "user"
    ADMIN = "admin"

class WithEnum(object):
    """Attributes:
            name (str, serializable): Description of simple
            user_type (UserEnum, serializable): Description of name
        """
    def __init__(self, name=None, user_type=None):
        self.name = name
        self.user_type = user_type

class WithEnumNested(object):
    """Attributes:
            name (str, serializable): Description of simple
            user_type (UserEnum, serializable): Description of name
            other_enum (WithEnum, serializable): Description of name
        """
    def __init__(self, name=None, other_enum=None, user_type=None):
        self.name = name
        self.other_enum = other_enum
        self.user_type = user_type
