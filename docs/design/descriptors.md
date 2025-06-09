# Descriptors for Interaction Affordances

Interaction affordaces are implemented with descriptor protocol. Descriptor protocols are the machinery behind:

- `@property` decorators, validated object attributes (`param`, `traitlets`, `attrs` etc.)
- python bound methods, `@classmethod`, `@staticmethod`
- ORMs

Accessing an interaction affordace gives the following behaviour:

| Affordance | Class Level Access      | Instance Level Access |
|------------|-------------------------|-----------------------|
| Properties | `Property` object       | `Property` value      |
| Actions    | unbound `Action` object | bound `Action`        |
| Events     | `Event` object          | event publisher       |

This allows using the same affordance in different contexts, such as:
- Accessing a property at the class level to get metadata like default value, schema, claim it as being observable etc.
- But access at the instance level to get the current value.
- class can autogenerate Thing models, whereas protocols can add forms to autogenerate Thing Descriptions.

## Property Descriptors

API possibilities:

- Directly typed properties and untyped properties for beginners who understand data types (`String`, `Boolean`, `List`, `Binary`). See list of available types [here](../howto/code/properties/typed.py).
- JSON schema and pydantic models for advanced users who want to define complex data structures
- Optional setters and getters, reducing boilerplate code when setters and getters are not needed
- Setter and getters can be used to custom validate and custom transform data before setting it on the object
- Observers can be notified when the value is set, allowing for reactive programming
- generate Thing Model fragment

Sequence of access:

1. Check if the property is constant or read-only, if so, dont validate or allow setting the value.
2. If the property is settable, validate the value against the type or schema.
3. Set the value either in the object's `__dict__` or a custom setter method if provided. 
4. If the property needs to be stored in a database, call the database setter method (allow configuration management for devices).
5. Call local observers (`param.depends`) and push change events if the property is observable.

## Action Descriptors

API possibilities:

- defining parameter schema using type annotations (reducing coding effort), JSON schema, or pydantic models
- defining return type using type annotations, JSON schema, or pydantic models
- docstring becomes the action description
- Execution control:
    - synchronous - by default queued one after another
        - object is not manipulated simultaneously by multiple actions or threads
        - prevents incompatible physical actions from running at the same time on the same device
        - maximizes thread safety
    - threaded actions
        - not queued, runs when called
        - allows multiple actions to run simultaneously
        - suitable for long running actions
    - async
        - create an asyncio task in the current event loop
        - OR, multiple async actions from multiple `Things` can be run in parallel
- classmethod can become actions
- generate Thing Model fragment

Sequence of access:

1. Validate payload against the action schema
2. Bind the class or instance according to whether the action is a class method or instance method
3. Schedule the action according to the action type (sync, async, threaded), spread the payload as keyword arguments if necessary and return the result

## Event Descriptors

API possibilities:

- defining event schema using JSON schema or pydantic models
- pub-sub model
- generate Thing Model fragment

Sequence of access:

1. Serialize the event payload
2. Simply push the payload to the publishing socket











