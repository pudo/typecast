from typesystem.util import SchemaObject


class Attribute(SchemaObject):
    """ An attribute is a named property that a node in the graph
    may have assinged to it. """

    def __init__(self, parent, name, data):
        super(Attribute, self).__init__(name, data.get('label'))
        self.qname = '%s:%s' % (parent.name, name)
        self._parent = parent
        self._type = data.get('type')
        self.phrase = data.get('phrase', self.label)
        self.many = data.get('many', False)

    @property
    def type(self):
        return self._parent.registry[self._type]

    def to_dict(self):
        return {
            'name': self.name,
            'qname': self.qname,
            'label': self.label,
            'phrase': self.phrase,
            'many': self.many,
            'type': self.type.to_index_dict()
        }

    def to_index_dict(self):
        return self.name

    def __repr__(self):
        return '<Attribute(%r,%r)>' % (self.name, self.type)

    def __eq__(self, other):
        if hasattr(other, 'name'):
            return self.qname == other.qname
        return self.qname == other

    def __unicode__(self):
        return self.qname
