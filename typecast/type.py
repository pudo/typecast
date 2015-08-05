from typesystem.util import SchemaObject, TypeException


class Type(SchemaObject):
    """ A type can be a primitive value (such as a string or a number) or a
    complex object, such as the data structure for a company or person. """
    is_entity = False
    is_value = False

    def __init__(self, registry, name, data):
        self.registry = registry
        self._parent = data.get('parent')
        super(Type, self).__init__(name, data.get('label'),
                                   abstract=data.get('abstract', False))

    @property
    def root(self):
        return self._parent is None

    @property
    def parent(self):
        if not self.root:
            return self.registry[self._parent]

    @property
    def parents(self):
        """ This includes the type itself. """
        if self.root:
            return set([self])
        return self.registry[self._parent].parents.union([self])

    @property
    def subtypes(self):
        """ This includes the type itself. """
        subtypes = set([self])
        for subtype in self.registry.values():
            if subtype._parent == self.name:
                subtypes.update(subtype.subtypes)
        return subtypes

    def matches(self, other):
        if isinstance(other, Type):
            other = other.name
        return other in [s.name for s in self.subtypes]

    def serialize(self, value):
        return value

    def deserialize(self, value):
        return value

    def serialize_safe(self, value):
        if value is None:
            return None
        try:
            obj = self.deserialize_safe(value)
            return self.serialize(obj)
        except TypeException:
            raise
        except Exception, e:
            raise TypeException(self, value, exc=e)

    def deserialize_safe(self, value):
        if value is None:
            return None
        try:
            return self.deserialize(value)
        except TypeException:
            raise
        except Exception, e:
            raise TypeException(self, value, exc=e)

    def to_freebase_type(self):
        return {
            'id': '/type/%s' % self.name,
            'name': self.label
        }

    def to_dict(self):
        data = super(Type, self).to_dict()
        data['parent'] = self._parent
        return data

    def __repr__(self):
        clazz = self.__class__.__name__
        return '<%s(%r,%r)>' % (clazz, self.name, self.label)

    def __unicode__(self):
        return self.label
