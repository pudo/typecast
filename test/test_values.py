import unittest
from datetime import datetime

from typecast import create_registry, TypeException


class ValueTypesUnitTest(unittest.TestCase):

    def setUp(self):
        self.registry = create_registry()

    def test_registry(self):
        registry = self.registry.keys()
        assert len(registry) == 7, registry
        assert 'string' in registry, registry
        assert 'type' in registry, registry

    def test_none(self):
        type_ = self.registry['string']
        text = None
        assert type_.serialize(text) == text, type_.serialize(text)
        assert type_.deserialize(text) == text, type_.deserialize(text)

    def test_string(self):
        type_ = self.registry['string']
        text = 'This is a string'
        assert type_.serialize(text) == text, type_.serialize(text)
        assert type_.deserialize(text) == text, type_.deserialize(text)

    def test_float(self):
        type_ = self.registry['float']
        num, text = 2.1, '2.1'
        assert type_.serialize(num) == text, type_.serialize(num)
        assert type_.deserialize(text) == num, type_.deserialize(text)

        with self.assertRaises(TypeException):
            type_.deserialize_safe('banana')

    def test_boolean(self):
        type_ = self.registry['boolean']
        val, text = True, 'true'
        assert type_.serialize(val) == text, type_.serialize(val)
        assert type_.deserialize(text) == val, type_.deserialize(text)
        assert type_.deserialize_safe(None) is None, \
            type_.deserialize_safe(None)

    def test_value(self):
        type_ = self.registry['type']
        val = 'type'
        assert type_.serialize(type_) == val, type_.serialize(val)
        assert type_.deserialize(val) == type_, type_.deserialize(val)

        with self.assertRaises(TypeException):
            type_.deserialize_safe('banana')

    def test_date(self):
        type_ = self.registry['date']
        val = datetime(2015, 5, 23)
        text = val.date().isoformat()
        assert type_.serialize(val) == text, type_.serialize(val)
        assert type_.deserialize(text).isoformat() == text, \
            type_.deserialize(text)

        with self.assertRaises(TypeException):
            type_.deserialize_safe('banana')

        with self.assertRaises(TypeException):
            type_.serialize_safe('banana')

    def test_datetime(self):
        type_ = self.registry['datetime']
        val = datetime.utcnow()
        text = val.isoformat()
        assert type_.serialize(val) == text, type_.serialize(val)
        assert type_.deserialize(text).isoformat() == text, \
            type_.deserialize(text)

        with self.assertRaises(TypeException):
            type_.deserialize_safe('banana')
