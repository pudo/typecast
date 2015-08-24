import six
import dateutil.parser
from datetime import datetime, date

from typecast.formats import DATE_FORMATS, DATETIME_FORMATS
from typecast.formats import format_regex
from typecast.converter import Converter


class DateTime(Converter):
    """ Timestamp """
    result_type = datetime
    formats = DATETIME_FORMATS

    def __init__(self, format=None):
        self.opts = {'format': format}
        self.format = format

    def test(self, value):
        if isinstance(value, six.string_types):
            if len(value.strip()) == 0:
                return 0
            if format_regex(self.format):
                match = format_regex(self.format).match(value)
                return 1 if match is not None else -1
        return super(DateTime, self).test(value)

    def _stringify(self, value, **opts):
        return value.isoformat()

    def _cast(self, value, format=None, **opts):
        """ Optionally apply a format string. """
        if format is not None:
            return datetime.strptime(value, format)
        return dateutil.parser.parse(value)

    @classmethod
    def instances(cls):
        return (cls(format=f) for f in cls.formats)

    def __eq__(self, other):
        if self.__class__ == other.__class__:
            if self.format and other.format:
                return self.format == other.format
            return True

    def __hash__(self):
        return hash(hash(self.__class__) + hash(self.format))

    def __repr__(self):
        return '<%s(%r)>' % (self.__class__.__name__, self.format)


class Date(DateTime):
    """ Date """
    result_type = date
    formats = DATE_FORMATS

    def _stringify(self, value, **opts):
        if isinstance(value, datetime):
            value = value.date()
        return value.isoformat()

    def _cast(self, value, **opts):
        dt = super(Date, self)._cast(value, **opts)
        return dt.date() if isinstance(dt, datetime) else dt
