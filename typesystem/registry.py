

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

    def to_dict(self):
        return dict(self.items())


class TypeRegistry(Registry):

    def __init__(self):
        from typesystem.type import Type
        self.cls = Type

    @property
    def qualified(self):
        _qualified = {}
        for type_ in self.values():
            if hasattr(type_, 'attributes'):
                for attr in type_.attributes.values():
                    _qualified[attr.qname] = attr
        return _qualified
