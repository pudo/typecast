import unittest
import decimal
from datetime import datetime

import typecast
from typecast import ConverterError
from typecast import value, date, formats


class ConvertersUnitTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_name(self):
        n = typecast.name('string')
        assert n == 'string', n
        n = typecast.name(7)
        assert n == 'integer', n
        n = typecast.name(False)
        assert n == 'bool', n

    def test_utils(self):
        conv = value.String()
        conv2 = typecast.converter('string')
        assert type(conv2) == type(conv), \
            typecast.converter('string')
        assert typecast.cast('string', 'foo') == 'foo'
        assert typecast.stringify('number', 7) == '7'

    def test_converter(self):
        conv1, conv2, conv3 = value.String(), value.String(), value.Integer()
        dateconv = date.Date(format='%Y-%m-%d')
        assert conv1 == conv2
        assert conv2 != conv3
        assert repr(conv1) == repr(conv2)
        assert '%Y' in repr(dateconv)
        assert dateconv != date.Date()

    def test_date_utils(self):
        dateconv = date.Date(format='%Y-%m-%d')
        dateconv2 = date.Date(format='%Y-%m-%d')
        dateconv3 = date.Date(format='%Y-%mZZ%d')
        assert dateconv == dateconv2
        assert dateconv != dateconv3
        assert dateconv2.test('huhu') == -1
        assert dateconv2.test('2009-01-12')

    def test_jts_spec(self):
        field = {'type': 'date', 'format': '%Y!%m!%d'}
        out = typecast.cast(field, '2009!04!12')
        assert out.year == 2009, out
        assert out.day == 12, out

    def test_cast_test(self):
        conv = value.Integer()
        assert conv.test(1) == 1
        assert conv.test('45454') == 1
        assert conv.test('45454djksdfj') == -1
        assert conv.test(None) == 0

    def test_configs(self):
        configs = list(typecast.instances())
        lens = len(typecast.CONVERTERS) - 3 + len(date.Date.formats) + \
            len(date.DateTime.formats)
        assert len(configs) == lens, (len(configs), lens)

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

    def test_integer_null(self):
        conv = value.Integer()
        num, text = 0, '0'
        assert conv.test('0') == 1
        assert conv.stringify(num) == text, conv.stringify(num)
        assert conv.cast(text) == num, conv.cast(text)

    def test_float(self):
        conv = value.Float()
        num, text = 2.1, '2.1'
        assert conv.stringify(num) == text, conv.stringify(num)
        assert conv.cast(text) == num, conv.cast(text)
        assert conv.cast(num) == num, conv.cast(num)

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

    def test_datetime_formats(self):
        conv = date.DateTime()
        dt = conv.cast('6/16/99 0:00')
        assert dt is not None, dt
        assert dt.year == 1999, dt

        regex = formats.format_regex('%m/%d/%y %H:%M')
        m = regex.match('6/16/99 0:00')
        assert m is not None, m
        m = regex.match('6/16/1999 0:00')
        assert m is None, m

    def test_formats_regex(self):
        regex = formats.format_regex('%Y-%m-%d')
        assert regex.match('2012-01-04')
        assert date.Date().test('2012-01-04') == 1
        assert date.Date(format='%Y-%m-%d').test('2012-01-02') == 1
        assert date.Date().test('2012-01-x04') == -1
