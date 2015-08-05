import unittest
import decimal
from datetime import datetime

from typecast import ConverterError
from typecast import value, date


class ConvertersUnitTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_none(self):
        conv = value.String()
        text = None
        assert conv.stringify(text) == text, conv.stringify(text)
        assert conv.cast(text) == text, conv.cast(text)

    def test_string(self):
        conv = value.String()
        text = 'This is a string'
        assert conv.stringify(text) == text, conv.stringify(text)
        assert conv.cast(text) == text, conv.cast(text)

    def test_integer(self):
        conv = value.Integer()
        num, text = 7842, '7842'
        assert conv.stringify(num) == text, conv.stringify(num)
        assert conv.cast(text) == num, conv.cast(text)

    def test_float(self):
        conv = value.Float()
        num, text = 2.1, '2.1'
        assert conv.stringify(num) == text, conv.stringify(num)
        assert conv.cast(text) == num, conv.cast(text)

        with self.assertRaises(ConverterError):
            conv.cast('banana')

    def test_decimal(self):
        conv = value.Decimal()
        num, text = decimal.Decimal(2.1), '2.1'
        assert float(conv.stringify(num)) == float(text), conv.stringify(num)
        val = float(conv.cast(text) - num)
        assert val < 0.1, (conv.cast(text), val)

        with self.assertRaises(ConverterError):
            conv.cast('banana')

    def test_boolean(self):
        conv = value.Boolean()
        val, text = True, 'true'
        assert conv.stringify(val) == text, conv.stringify(val)
        assert conv.cast(text) == val, conv.cast(text)
        assert conv.cast(None) is None, conv.cast(None)

        conv = value.Boolean()
        val, text = False, 'false'
        assert conv.stringify(val) == text, conv.stringify(val)
        assert conv.cast(text) == val, conv.cast(text)

    def test_date(self):
        conv = date.Date()
        val = datetime(2015, 5, 23).date()
        text = val.isoformat()
        assert conv.stringify(val) == text, conv.stringify(val)
        assert conv.cast(text).isoformat() == text, \
            (conv.cast(text), conv.cast(text).isoformat())

        with self.assertRaises(ConverterError):
            conv.cast('banana')

        with self.assertRaises(ConverterError):
            conv.stringify('banana')

    def test_datetime(self):
        conv = date.DateTime()
        val = datetime.utcnow()
        text = val.isoformat()
        assert conv.stringify(val) == text, conv.stringify(val)
        assert conv.cast(text).isoformat() == text, \
            conv.cast(text)

        with self.assertRaises(ConverterError):
            conv.cast('banana')
