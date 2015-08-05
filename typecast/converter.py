import six


class Converter(object):
    """ A type converter for a primitive value (such as a string or a
    number). """
    result_type = None
    allow_empty = False

    def serialize(self, value):
        return six.text_type(value)

    def deserialize(self, value):
        return six.text_type(value)

    def _is_null(self, value):
        if isinstance(value, six.string_types):
            if '' == value.strip() and not self.allow_empty:
                return False
        return value is None

    def serialize_safe(self, value):
        if self._is_null(value):
            return None
        try:
            return self.serialize(obj)
        except Exception, e:
            if not isinstance(e, ConverterError):
                e = ConverterError(None, exc=e)
            e.converter = self.__class__
            raise e

    def deserialize_safe(self, value):
        if self._is_null(value):
            return None
        try:
            return self.deserialize(value)
        except Exception, e:
            if not isinstance(e, ConverterError):
                e = ConverterError(None, exc=e)
            e.converter = self.__class__
            raise e

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
