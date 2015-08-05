from typecast.util import TypeException


class Converter(object):
    """ A type converter for a primitive value (such as a string or a
    number). """

    def __init__(self, registry):
        self.registry = registry

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

    def __repr__(self):
        clazz = self.__class__.__name__
        return '<%s(%r)>' % (clazz, self.name, self.label)

    def __unicode__(self):
        return self.__class__.__name__.lower()
