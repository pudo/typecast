import six
import sys
import decimal
import locale
from datetime import datetime, date

from typecast.converter import Converter, ConverterError


class String(Converter):
    """ String """
    result_type = six.text_type
    allow_empty = True


class Integer(Converter):
    """ Integer """
    result_type = int

    def deserialize(self, value):
        try:
            value = float(value)
        except:
            return locale.atoi(value)

        if value.is_integer():
            return int(value)
        else:
            raise ConverterError('Invalid integer: %r' % value)


class Boolean(Converter):
    """ A boolean field. Matches true/false, yes/no and 0/1 by default,
    but a custom set of values can be optionally provided. """
    result_type = bool
    true_values = ('t', 'yes', 'y', '1', 'true', 'aye')
    false_values = ('f', 'no', 'n', '0', 'flase', 'nay')

    def serialize(self, value):
        return six.text_type(value).lower()

    def deserialize(self, value):
        if isinstance(value, six.string_types):
            value = value.lower().strip()
            if value in self.true_values:
                return True
            if value in self.false_values:
                return False


class Float(Converter):
    """ Floating-point number """
    result_type = float

    def deserialize(self, value):
        return float(value)


class Decimal(Converter):
    """ Decimal number, ``decimal.Decimal`` or float numbers. """
    result_type = decimal.Decimal

    def deserialize(self, value):
        try:
            return decimal.Decimal(value)
        except:
            value = locale.atof(value)
            if sys.version_info < (2, 7):
                value = str(value)
            return decimal.Decimal(value)
