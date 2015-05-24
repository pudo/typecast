

class Registry(dict):
    """ A simple proxy object so you can request. """

    def __init__(self, cls):
        self.cls = cls

    def get(self, name):
        if isinstance(name, self.cls):
            return name
        return self[name]

    def __getattr__(self, name):
        if name in self:
            return self[name]

    def __iter__(self):
        return iter(self.values())

    def to_dict(self):
        return self


class TypeRegistry(Registry):

    def __init__(self):
        from typesystem.type import Type
        self.cls = Type

    @property
    def qualified(self):
        _qualified = {}
        for type_ in self.values():
            for attr in type_.attributes.values():
                _qualified[attr.qname] = attr
        return _qualified
