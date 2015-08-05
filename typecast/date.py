import dateutil.parser
from datetime import datetime, date

from typecast.converter import Converter, ConverterError


class DateTime(Converter):
    """ Timestamp """
    result_type = datetime

    def _stringify(self, value, **opts):
        return value.isoformat()

    def _cast(self, value, format=None, **opts):
        """ Optionally apply a format string. """
        if format is not None:
            return datetime.strptime(value, format)
        return dateutil.parser.parse(value)


class Date(DateTime):
    """ Date """
    result_type = date

    def _stringify(self, value, **opts):
        if isinstance(value, datetime):
            value = value.date()
        return value.isoformat()

    def _cast(self, value, **opts):
        dt = super(Date, self)._cast(value, **opts)
        return dt.date() if isinstance(dt, datetime) else dt
