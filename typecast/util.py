import dateutil.parser

from normality import normalize


def date_parse(text):
    try:
        return dateutil.parser.parse(text)
    except (TypeError, ValueError, AttributeError):
        return None


def bool_parse(text):
    return normalize(text) in ['t', 'yes', 'y', '1', 'true', 'aye']


class TypeException(Exception):

    def __init__(self, type_, value, message=None, exc=None):
        self.type = type_
        self.value = value
        self.exc = exc
        if message is None:
            if hasattr(exc, 'message'):
                message = exc.message
            elif exc is not None:
                message = unicode(exc)
        self.message = message
