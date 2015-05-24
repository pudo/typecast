import yaml

from typesystem.type import Type
from typesystem.attribute import Attribute # noqa
from typesystem.registry import TypeRegistry
from typesystem.util import TypeException # noqa


def load(path):
    """ Load types and attributes from a ``.yaml`` file specified. """
    types = TypeRegistry(Type)
    with open(path, 'rb') as fh:
        data = yaml.load(fh)
        for name, obj in data.get('types', {}).items():
            types[name] = Type(types, name, obj)
    return types
