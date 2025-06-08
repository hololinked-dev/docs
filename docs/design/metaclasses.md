# Metaclasses

The `Metaclass` allow customization of `Thing` subclass creation, modify class attributes, and enforce certain behaviors across multiple `Thing` classes. It is mainly intended for grouping class definition for same hardware types.

default metaclass implements:

- creation of descriptor registries at class level (so that registries can also be used without instances)
- `__post_init__` method to allow for code that should run post initialization of the class

Subclassing metaclasses can implement:

- mandate existence of certain properties, actions, or events according to the hardware type
- also constrain the type of the properties, payload schema of actions, or events
- default code to run when an instance is created






