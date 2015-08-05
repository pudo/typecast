from datetime import datetime, date

from typecast.util import date_parse, bool_parse, TypeException
from typecast.converter import Converter


class String(Converter):
    """ String """


class Integer(Converter):
    """ Integer """

    def serialize(self, value):
        return unicode(value)

    def deserialize(self, value):
        return int(value)


class Boolean(Converter):
    """ Boolean """

    def serialize(self, value):
        return unicode(value).lower()

    def deserialize(self, value):
        if isinstance(value, bool):
            return value
        return bool_parse(value)


class Float(Converter):
    """ Floating-point number """

    def serialize(self, value):
        return unicode(value)

    def deserialize(self, value):
        return float(value)


class DateTime(Converter):
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


class Date(DateTimeValue):
    """ Date """

    def serialize(self, value):
        if isinstance(value, datetime):
            value = value.date()
        return value.isoformat() if isinstance(value, date) else value

    def deserialize(self, value):
        dt = super(Date, self).deserialize(value)
        return dt.date() if isinstance(dt, datetime) else dt
