import yaml

from typesystem.attribute import Attribute # noqa
from typesystem.registry import TypeRegistry
from typesystem.value import StringValue, BooleanValue, IntegerValue, FloatValue
from typesystem.value import DateTimeValue, DateValue, TypeValue
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


def load(path, entity_loader):
    """ Load types and attributes from a ``.yaml`` file specified. """
    types = create_registry()
    with open(path, 'rb') as fh:
        data = yaml.load(fh)
        for name, obj in data.get('types', {}).items():
            types[name] = EntityType(types, name, obj, entity_loader)
    return types
