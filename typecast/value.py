from datetime import datetime, date

from typecast.util import date_parse, bool_parse, TypeException
from typecast.type import Type


class ValueType(Type):
    """ Value types are data primitives. """
    is_value = True

    def __init__(self, registry):
        name = self.__class__.__name__.replace('Value', '').lower()
        label = self.__doc__.strip()
        super(ValueType, self).__init__(registry, name, {'label': label})


class StringValue(ValueType):
    """ String """


class IntegerValue(ValueType):
    """ Integer """

    def serialize(self, value):
        return unicode(value)

    def deserialize(self, value):
        return int(value)


class BooleanValue(ValueType):
    """ Boolean """

    def serialize(self, value):
        return unicode(value).lower()

    def deserialize(self, value):
        if isinstance(value, bool):
            return value
        return bool_parse(value)


class FloatValue(ValueType):
    """ Floating-point number """

    def serialize(self, value):
        return unicode(value)

    def deserialize(self, value):
        return float(value)


class DateTimeValue(ValueType):
    """ Timestamp """

    def serialize(self, value):
        return value.isoformat() if isinstance(value, datetime) else value

    def deserialize(self, value):
        if isinstance(value, (date, datetime)):
            return value
        dt = date_parse(value)
        if dt is None:
            raise TypeException(self, value, message='Invalid datetime value.')
        return dt


class DateValue(DateTimeValue):
    """ Date """

    def serialize(self, value):
        if isinstance(value, datetime):
            value = value.date()
        return value.isoformat() if isinstance(value, date) else value

    def deserialize(self, value):
        dt = super(DateValue, self).deserialize(value)
        return dt.date() if isinstance(dt, datetime) else dt


class TypeValue(ValueType):
    """ Type """

    def serialize(self, value):
        if hasattr(value, 'name'):
            return value.name
        return value

    def deserialize(self, value):
        if isinstance(value, Type):
            return value
        type_ = self.registry.get(value)
        if type_ is None:
            raise TypeException(self, value, message='Unknown entity type.')
        return type_
