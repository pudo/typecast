from typesystem.attribute import Attribute # noqa
from typesystem.registry import TypeRegistry
from typesystem.value import StringValue, BooleanValue, IntegerValue
from typesystem.value import DateTimeValue, DateValue, TypeValue, FloatValue
from typesystem.entity import EntityType
from typesystem.util import TypeException # noqa

VALUE_TYPES = [StringValue, BooleanValue, IntegerValue, FloatValue,
               DateTimeValue, DateValue, TypeValue]


def create_registry():
    types = TypeRegistry()
    # register value types
    for type_cls in VALUE_TYPES:
        type_ = type_cls(types)
        types[type_.name] = type_
    return types
