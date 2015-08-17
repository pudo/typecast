import six


class Converter(object):
    """ A type converter for a primitive value (such as a string or a
    number). """
    result_type = None

    def __init__(self):
        self.opts = {}

    def _stringify(self, value, **opts):
        return six.text_type(value)

    def _cast(self, value, **opts):
        return six.text_type(value)

    def _is_null(self, value):
        """ Check if an incoming value is ``None`` or the empty string. """
        if isinstance(value, six.string_types):
            if '' == value.strip():
                return True
        return value is None

    def test(self, value):
        try:
            out = self.cast(value)
            return 0 if out is None else 1
        except ConverterError:
            return -1

    def cast(self, value, **opts):
        """ Convert the given value to the target type, or return ``None`` if
        the value is empty. If an error occurs, raise a ``ConverterError``. """
        if isinstance(value, self.result_type):
            return value
        if self._is_null(value):
            return None
        try:
            opts_ = self.opts.copy()
            opts_.update(opts)
            return self._cast(value, **opts_)
        except Exception as e:
            if not isinstance(e, ConverterError):
                e = ConverterError(None, exc=e)
            e.converter = self.__class__
            raise e

    def stringify(self, value, **opts):
        """ Inverse of conversion: generate a string representation of the data
        that is guaranteed to be parseable by this library. """
        if self._is_null(value):
            return None
        try:
            opts_ = self.opts.copy()
            opts_.update(opts)
            return self._stringify(value, **opts_)
        except Exception as e:
            if not isinstance(e, ConverterError):
                e = ConverterError(None, exc=e)
            e.converter = self.__class__
            raise e

    @classmethod
    def instances(cls):
        yield cls()

    def __eq__(self, other):
        return self.__class__ == other.__class__

    def __hash__(self):
        return hash(self.__class__)

    def __repr__(self):
        return '<%s()>' % self.__class__.__name__

    def __unicode__(self):
        return self.__class__.__name__.lower()


class ConverterError(TypeError):
    """ An exception wrapper for all errors occuring in the process of
    conversion. This can also be caught as a ``TypeError``. """

    def __init__(self, message, exc=None, converter=None):
        self.converter = converter
        self.exc = exc
        if message is None:
            if hasattr(exc, 'message'):
                message = exc.message
            elif exc is not None:
                message = six.text_type(exc)
        self.message = message
