import yaml

from typesystem.type import Type
from typesystem.attribute import Attribute # noqa
from typesystem.schema import Schema
from typesystem.data_types import DataException # noqa


def load(path):
    """ Load types and attributes from a ``.yaml`` file specified. """
    types = Schema(Type)
    with open(path, 'rb') as fh:
        data = yaml.load(fh)
        for name, obj in data.get('types', {}).items():
            types[name] = Type(name, obj)
    return types
