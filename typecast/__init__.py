from copy import deepcopy

from typecast.value import String, Boolean, Integer, Float, Decimal
from typecast.date import DateTime, Date
from typecast.converter import ConverterError  # noqa
from typecast.name import name  # noqa

CONVERTERS = [String, Boolean, Integer, Float, Decimal, DateTime, Date]

TYPES = {
    'any': String,
    'string': String,
    'text': String,
    'integer': Integer,
    'number': Float,
    'float': Float,
    'double': Float,
    'decimal': Decimal,
    'date': Date,
    'datetime': DateTime,
    'date-time': DateTime,
    'boolean': Boolean,
    'bool': Boolean
}


def _field_options(field, opts):
    if isinstance(field, dict):
        _extra = opts
        opts = deepcopy(field)
        opts.update(_extra)
        field = opts.get('type')
    return field, opts


def converter(type_name):
    """ Get a given converter by name, or raise an exception. """
    converter = TYPES.get(type_name)
    if converter is None:
        raise ConverterError('Unknown converter: %r' % type_name)
    return converter()


def cast(type_name, value, **opts):
    """ Convert a given (string) ``value`` to the type indicated by
    ``type_name``. If ``None`` is passed in, it will always be returned.

    Optional arguments can include ``true_values`` and ``false_values`` to
    describe boolean types, and ``format`` for dates. """
    type_name, opts = _field_options(type_name, opts)
    return converter(type_name).cast(value, **opts)


def stringify(type_name, value, **opts):
    """ Generate a string representation of the data in ``value`` based on the
    converter specified by ``type_name``. This is guaranteed to yield a form
    which can easily be parsed by ``cast()``. """
    type_name, opts = _field_options(type_name, opts)
    return converter(type_name).stringify(value, **opts)


def instances():
    """ Yield a set of possible configurations for the various types. This can
    be used to perform type-guessing by checking the applicability of each
    converter against a set of sample data. """
    for converter in CONVERTERS:
        for inst in converter.instances():
            yield inst
