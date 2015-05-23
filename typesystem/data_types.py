from datetime import datetime, date
from typesystem.util import date_parse, bool_parse


class DataException(Exception):

    def __init(self, data_type, value, message=None, exc=None):
        self.data_type = data_type
        self.value = value
        self.exc = exc
        if message is None:
            if hasattr(exc, 'message'):
                message = exc.message
            elif exc is not None:
                message = unicode(exc)
        self.message = message


class DataType(object):

    def __init__(self, attribute):
        self.attribute = attribute

    def serialize(self, value):
        return value

    def deserialize(self, value):
        return value

    def serialize_safe(self, value):
        if value is None:
            return None
        try:
            obj = self.deserialize_safe(value)
            return self.serialize(obj)
        except DataException:
            raise
        except Exception, e:
            raise DataException(self, value, e)

    def deserialize_safe(self, value):
        if value is None:
            return None
        try:
            return self.deserialize(value)
        except DataException:
            raise
        except Exception, e:
            raise DataException(self, value, e)

    def __unicode__(self):
        return self.__class__.__name__.lower()


class String(DataType):
    pass


class Integer(DataType):

    def serialize(self, value):
        return unicode(value)

    def deserialize(self, value):
        return int(value)


class Boolean(DataType):

    def serialize(self, value):
        return unicode(value)

    def deserialize(self, value):
        if isinstance(value, bool):
            return value
        return bool_parse(value)


class Float(DataType):

    def serialize(self, value):
        return unicode(value)

    def deserialize(self, value):
        return float(value)


class Date(DataType):

    def serialize(self, value):
        return value.isoformat() if isinstance(value, date) else value

    def deserialize(self, value):
        if isinstance(value, date):
            return value
        if isinstance(value, datetime):
            return value.date()
        dt = date_parse(value)
        if dt is not None:
            return dt.date()


class DateTime(DataType):

    def serialize(self, value):
        return value.isoformat() if isinstance(value, datetime) else value

    def deserialize(self, value):
        if isinstance(value, (date, datetime)):
            return value
        return date_parse(value)


class Type(DataType):

    def serialize(self, value):
        if hasattr(value, 'name'):
            return value.name
        return value

    def deserialize(self, value):
        from nomenklatura.schema.type import Type
        from nomenklatura.schema import types
        if isinstance(value, Type):
            return value
        type_ = types[value]
        if type_ is None:
            raise TypeError("Unknown entity type: %s" % value)
        return type_


class Entity(DataType):

    def serialize(self, entity):
        if hasattr(entity, 'id'):
            return entity.id
        return entity

    def deserialize(self, value):
        from nomenklatura.model.entity import Entity
        from nomenklatura.query import EntityQuery
        if isinstance(value, Entity):
            return value
        ent = EntityQuery.by_id(value)
        # if ent is None:
        #    raise TypeError("Entity does not exist: %r" % value)
        return ent


DATA_TYPES = {
    'string': String,
    'boolean': Boolean,
    'text': String,
    'integer': Integer,
    'int': Integer,
    'float': Float,
    'datetime': DateTime,
    'date': Date,
    'type': Type,
    'entity': Entity
}
