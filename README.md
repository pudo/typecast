# typesystem

An abstract type system, inspired by Freebase. ``typesystem`` can be
used to describe a type hierarchy of classes with attributes and
inheritance.

This was factored out of ``nomenklatura`` to become re-usable. See the [MQL
documentation](https://developers.google.com/freebase/mql/ch02#id2944699)
for the intended functionality.

## Example usage

``typesystem`` is used to manage and enforce type hierarchies that are generated dynamically (from a schema definition file). A Python snippet using the library could look like this:

```python
import typesystem

types = typesystem.load_yaml('example.yaml')
person = types.Person

# Attribute inheritance:
assert person.attributes.type.qname == 'Object:type'

for attribute in person.attributes:
    print attribute.name, attribute.type
```

### Schema definition

```yaml
types:
    Object:
        label: "Object"
        abstract: true
        attributes:
            type:
                label: "Type"
                type: type
                phrase: "is a"
            label:
                label: "Label"
                type: string
                phrase: "is called"

    Person:
        label: "Person"
        parent: Object
        attributes:
            email:
                label: "E-Mail"
                type: string
            gender:
                label: "Gender"
                type: string
            birth_date:
                label: "Birth date"
                type: date
            death_date:
                label: "Death date"
                type: date
            mother:
                label: "Biological mother"
                type: Person
```

## Value data types

The type system currently defines the following core value data types (primitives): ``string``, ``integer``, ``float``, ``boolean``, ``date``, ``datetime`` and ``type``.


## Tests

```bash
pip install nose coverage
nosetests --with-coverage --cover-package=typesystem --cover-erase
```
