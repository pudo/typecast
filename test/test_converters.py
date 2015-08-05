import unittest
from datetime import datetime

from typecast import ConverterError
from typecast import value, date


class ConvertersUnitTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_none(self):
        type_ = value.String()
        text = None
        assert type_.serialize(text) == text, type_.serialize(text)
        assert type_.deserialize(text) == text, type_.deserialize(text)

    def test_string(self):
        type_ = value.String()
        text = 'This is a string'
        assert type_.serialize(text) == text, type_.serialize(text)
        assert type_.deserialize(text) == text, type_.deserialize(text)

    def test_float(self):
        type_ = value.Float()
        num, text = 2.1, '2.1'
        assert type_.serialize(num) == text, type_.serialize(num)
        assert type_.deserialize(text) == num, type_.deserialize(text)

        with self.assertRaises(ConverterError):
            type_.deserialize_safe('banana')

    def test_boolean(self):
        type_ = value.Boolean()
        val, text = True, 'true'
        assert type_.serialize(val) == text, type_.serialize(val)
        assert type_.deserialize(text) == val, type_.deserialize(text)
        assert type_.deserialize_safe(None) is None, \
            type_.deserialize_safe(None)

    def test_date(self):
        type_ = date.Date()
        val = datetime(2015, 5, 23)
        text = val.date().isoformat()
        assert type_.serialize(val) == text, type_.serialize(val)
        assert type_.deserialize(text).isoformat() == text, \
            type_.deserialize(text)

        with self.assertRaises(ConverterError):
            type_.deserialize_safe('banana')

        with self.assertRaises(ConverterError):
            type_.serialize_safe('banana')

    def test_datetime(self):
        type_ = date.DateTime()
        val = datetime.utcnow()
        text = val.isoformat()
        assert type_.serialize(val) == text, type_.serialize(val)
        assert type_.deserialize(text).isoformat() == text, \
            type_.deserialize(text)

        with self.assertRaises(ConverterError):
            type_.deserialize_safe('banana')
