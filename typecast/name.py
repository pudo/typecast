import six
from datetime import datetime, date
from decimal import Decimal


TESTS = ((six.text_type, 'string'),
         (bool, 'bool'),
         (int, 'integer'),
         (float, 'float'),
         (date, 'date'),
         (datetime, 'datetime'),
         (Decimal, 'decimal'))


def name(value):
    """ Given a value, get an appropriate string title for the type that can
    be used to re-cast the value later. """
    if value is None:
        return 'any'
    for (test, name) in TESTS:
        if isinstance(value, test):
            return name
    return 'string'
