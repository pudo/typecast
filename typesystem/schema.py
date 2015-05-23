

class Schema(dict):
    """ A simple proxy object so you can request. """

    def __init__(self, cls):
        self.cls = cls
        self._qualified = None

    @property
    def qualified(self):
        if self._qualified is None:
            self._qualified = {}
            for type_ in self:
                for attr in type_.attributes:
                    self._qualified[attr.qname] = attr
        return self._qualified

    def get(self, name):
        if isinstance(name, self.cls):
            return name
        return self[name]

    def __getattr__(self, name):
        return self.__getitem__(name)

    def to_dict(self):
        return self
