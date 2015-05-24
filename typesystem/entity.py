from typesystem.registry import Registry
from typesystem.attribute import Attribute
from typesystem.type import Type


class EntityType(Type):
    """ An entity type defines a node in the graph to be a member of a
    particular class of thing, e.g. a company or a person. """

    def __init__(self, registry, name, data, entity_loader):
        super(EntityType, self).__init__(registry, name, data)
        self._attr_data = data.get('attributes', {})
        self._attributes = None
        self._entity_loader = entity_loader

    @property
    def attributes(self):
        if self._attributes is None:
            self._attributes = Registry(Attribute)
            if not self.root:
                items = self.parent.attributes.items()
                self._attributes.update(items)
            for name, data in self._attr_data.items():
                self._attributes[name] = Attribute(self, name, data)
        return self._attributes

    def serialize(self, entity):
        return entity.id if hasattr(entity, 'id') else entity

    def deserialize(self, value):
        return value if hasattr(value, 'id') else self._entity_loader(value)

    def to_dict(self):
        data = super(EntityType, self).to_dict()
        data['attributes'] = self.attributes
        return data
