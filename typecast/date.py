import dateutil.parser
from datetime import datetime, date

from typecast.formats import DATE_FORMATS, DATETIME_FORMATS
from typecast.converter import Converter


class DateTime(Converter):
    """ Timestamp """
    result_type = datetime
    formats = DATE_FORMATS

    def _stringify(self, value, **opts):
        return value.isoformat()

    def _cast(self, value, format=None, **opts):
        """ Optionally apply a format string. """
        if format is not None:
            return datetime.strptime(value, format)
        return dateutil.parser.parse(value)

    @classmethod
    def configs(cls):
        return ((cls(), {'format': f}) for f in cls.formats)


class Date(DateTime):
    """ Date """
    result_type = date
    formats = DATETIME_FORMATS

    def _stringify(self, value, **opts):
        if isinstance(value, datetime):
            value = value.date()
        return value.isoformat()

    def _cast(self, value, **opts):
        dt = super(Date, self)._cast(value, **opts)
        return dt.date() if isinstance(dt, datetime) else dt
