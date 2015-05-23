from typesystem.util import SchemaObject
from typesystem.schema import Schema
from typesystem.attribute import Attribute


class Type(SchemaObject):
    """ A type defines a node in the graph to be a member of a
    particular class of thing, e.g. a company or a person. """

    def __init__(self, name, data):
        super(Type, self).__init__(name, data.get('label'),
                                   abstract=data.get('abstract', False))
        self._parent = data.get('parent')
        self._attr_data = data.get('attributes', {})
        self._attributes = None

    @property
    def root(self):
        return self._parent is None

    @property
    def parent(self):
        from nomenklatura.schema import types
        return types[self._parent]

    @property
    def parents(self):
        """ This includes the type itself. """
        from nomenklatura.schema import types
        if self.root:
            return set([self])
        return types[self._parent].parents.union([self])

    @property
    def subtypes(self):
        """ This includes the type itself. """
        from nomenklatura.schema import types
        subtypes = set([self])
        for subtype in types:
            if subtype._parent == self.name:
                subtypes.update(subtype.subtypes)
        return subtypes

    def matches(self, other):
        if isinstance(other, Type):
            other = other.name
        return other in [s.name for s in self.subtypes]

    @property
    def attributes(self):
        if self._attributes is None:
            self._attributes = Schema(Attribute)
            if not self.root:
                items = self.parent.attributes.items()
                self._attributes._items.update(items)
            for name, data in self._attr_data.items():
                self._attributes._items[name] = Attribute(self, name, data)
        return self._attributes

    def to_dict(self):
        data = {
            'name': self.name,
            'label': self.label,
            'parent': self._parent,
            'abstract': self.abstract,
            'attributes': self.attributes
        }
        return data

    def to_index_dict(self):
        return self.name

    def to_freebase_type(self):
        return {
            'id': '/types/%s' % self.name,
            'name': self.label
        }

    def __repr__(self):
        return '<Type(%r,%r)>' % (self.name, self.label)

    def __unicode__(self):
        return self.label
