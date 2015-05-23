from typesystem.data_types import DATA_TYPES
from typesystem.util import SchemaObject


class Attribute(SchemaObject):
    """ An attribute is a named property that a node in the graph
    may have assinged to it. """

    def __init__(self, type_, name, data):
        super(Attribute, self).__init__(name, data.get('label'))
        self.qname = '%s:%s' % (type_.name, name)
        self.data_type = data.get('data_type')
        self.phrase = data.get('phrase', self.label)
        self.many = data.get('many', False)

    @property
    def converter(self):
        """ Instantiate a type converter for this attribute. """
        if self.data_type not in DATA_TYPES:
            raise TypeError('Invalid data type: %s'
                            % self.data_type)
        return DATA_TYPES[self.data_type]

    def to_dict(self):
        return {
            'name': self.name,
            'qname': self.qname,
            'label': self.label,
            'phrase': self.phrase,
            'many': self.many,
            'data_type': self.data_type
        }

    def to_index_dict(self):
        return self.name

    def __repr__(self):
        return '<Attribute(%r,%r)>' % (self.name, self.data_type)

    def __eq__(self, other):
        if hasattr(other, 'name'):
            return self.name == other.name
        return self.name == other

    def __unicode__(self):
        return self.name
