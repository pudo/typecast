from typecast.value import String, Boolean, Integer, Float, Decimal
from typecast.date import DateTime, Date
from typecast.converter import ConverterError  # noqa

CONVERTERS = [String, Boolean, Integer, Float, Decimal, DateTime, Date]

TYPES = {
    'string': String,
    'text': String,
    'number': Integer,
    'integer': Integer,
    'float': Float,
    'double': Float,
    'decimal': Decimal,
    'date': Date,
    'datetime': DateTime,
    'boolean': Boolean,
    'bool': Boolean
}


def cast(type_name, value, **opts):
    """ Convert a given (string) ``value`` to the type indicated by
    ``type_name``. If ``None`` is passed in, it will always be returned.

    Optional arguments can include ``true_values`` and ``false_values`` to
    describe boolean types, and ``format`` for dates. """
    converter = TYPES.get(type_name)
    if converter is None:
        return value
    return converter.cast(value, **opts)


def stringify(type_name, value, **opts):
    """ Generate a string representation of the data in ``value`` based on the
    converter specified by ``type_name``. This is guaranteed to yield a form
    which can easily be parsed by ``cast()``. """
    converter = TYPES.get(type_name)
    if converter is None:
        return value
    return converter.stringify(value, **opts)
