import os
import unittest
from datetime import datetime

from typesystem import load_yaml, TypeException

FIXTURE = os.path.join(os.path.dirname(__file__), 'fixture_system.yaml')


class EntityTypesUnitTest(unittest.TestCase):

    def setUp(self):
        self.registry = load_yaml(FIXTURE)

    def test_registry(self):
        registry = self.registry.keys()
        assert len(registry) == 9, registry
        assert 'Object' in registry, registry
        assert 'Person' in registry, registry

    def test_attributes(self):
        obj = self.registry['Object']
        assert len(obj.attributes) == 2, obj.attributes
        label = obj.attributes.label
        assert label.name == 'label', label
        assert label.qname == 'Object:label', label
        assert label._type == 'string', label
        assert label.type.name == 'string', label
