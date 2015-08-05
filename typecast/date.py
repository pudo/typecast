import dateutil.parser
from datetime import datetime, date

from typecast.converter import Converter, ConverterError


class DateTime(Converter):
    """ Timestamp """

    def serialize(self, value):
        return value.isoformat() if isinstance(value, datetime) else value

    def deserialize(self, value):
        if isinstance(value, (date, datetime)):
            return value
        try:
            return dateutil.parser.parse(value)
        except (TypeError, ValueError, AttributeError):
            raise ConverterError('Invalid date: %r' % text)


class Date(DateTime):
    """ Date """

    def serialize(self, value):
        if isinstance(value, datetime):
            value = value.date()
        return value.isoformat() if isinstance(value, date) else value

    def deserialize(self, value):
        dt = super(Date, self).deserialize(value)
        return dt.date() if isinstance(dt, datetime) else dt
