import re
import six
import sys
import decimal
import locale

from typecast.converter import Converter, ConverterError


class String(Converter):
    """String."""

    result_type = six.text_type
    jts_name = 'string'
    guess_score = 1
    allow_empty = True


class Integer(Converter):
    """Integer."""

    result_type = int
    jts_name = 'integer'
    guess_score = 6

    def _cast(self, value, **opts):
        try:
            if hasattr(value, 'is_integer') and not value.is_integer():
                raise ConverterError('Invalid integer: %r' % value)
            return int(value)
        except:
            try:
                return int(locale.atoi(value))
            except:
                raise ConverterError('Invalid integer: %r' % value)


class Boolean(Converter):
    """A boolean field.

    Matches true/false, yes/no and 0/1 by default,
    but a custom set of values can be optionally provided.
    """

    result_type = bool
    jts_name = 'boolean'
    guess_score = 7
    true_values = ('t', 'yes', 'y', 'true', 'aye')
    false_values = ('f', 'no', 'n', 'false', 'nay')

    def _stringify(self, value, **opts):
        return six.text_type(value).lower()

    def _cast(self, value, true_values=None, false_values=None, **opts):
        if isinstance(value, six.string_types):
            value = value.lower().strip()

            true_values = true_values or self.true_values
            if value in true_values:
                return True

            false_values = false_values or self.false_values
            if value in false_values:
                return False


class Float(Converter):
    """Floating-point number."""

    result_type = float
    jts_name = 'number'
    guess_score = 3

    def _cast(self, value, **opts):
        return float(value)

    @classmethod
    def instances(cls):
        # We don't want floats to be considered for type-testing, instead
        # use decimals (which are more conservative as a storage mechanism).
        return ()


class Decimal(Converter):
    """Decimal number, ``decimal.Decimal`` or float numbers."""

    result_type = decimal.Decimal
    jts_name = 'number'
    guess_score = 3
    pattern = r'\s*[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?\s*'
    pattern = re.compile(pattern, re.M)

    def _stringify(self, value, **opts):
        return '{0:.7f}'.format(value)

    def _cast(self, value, **opts):
        try:
            return decimal.Decimal(value)
        except:
            value = locale.atof(value)
            if sys.version_info < (2, 7):
                value = str(value)
            return decimal.Decimal(value)
