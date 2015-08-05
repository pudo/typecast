# typecast

This light-weight library contains a set of type converters commonly used to
parse string-typed values into more specific types, such as numbers, booleans
or dates. A typical use case might be converting values from HTTP query strings
or CSV files.

The benefits of using this library include a well-tested handling of type
conversions, e.g. for JSON Schema or JTS. Further, a consistent system of
exceptions (catch ``ConverterError`` and all is forgiven) makes it easier
to handle data errors.

## Example usage

``typecast`` can easily be included in many applications. A Python snippet
using the library could look like this:

```python
import typecast

```

## Tests

The goal is to have a high-nineties test coverage, and to collect as many odd
fringe cases as possible.

```bash
$ make test
```
