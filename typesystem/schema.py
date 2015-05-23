from collections import MutableMapping


class Schema(MutableMapping):
    """ A simple proxy object so you can request
    ``types.Company`` or ``attributes.label``. """

    def __init__(self, cls, items=None):
        self.cls = cls
        self._items = items or {}

    def __getitem__(self, name):
        return self._items.get(name)

    def __setitem__(self, name, obj):
        self._items[name] = obj

    def __delitem__(self, name):
        del self._items[name]

    def get(self, name):
        if isinstance(name, self.cls):
            return name
        return self[name]

    def __iter__(self):
        return iter(self._items.values())

    def items(self):
        return self._items.items()

    def __len__(self):
        return len(self._items)

    def __contains__(self, name):
        return name in self._items

    def __getattr__(self, name):
        return self.__getitem__(name)

    def to_dict(self):
        return self._items
