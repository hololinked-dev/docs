

::: hololinked.core.thing.Thing
    options:
        members:
            - __init__
            - run_with_http_server
            - run_with_zmq_server
            - run
            - ping
            - exit
            - get_thing_model
        

## Attributes

### `id`
`str` <br/> 
`instance-attribute`, `writable` <br />
{{ thing_id_docstring() }}

### `properties` 
`PropertiesRegistry` <br />
`instance-attribute`, `read-only` <br />
container for the property descriptors of the object

### `actions`
`ActionsRegistry` <br />
`instance-attribute`, `read-only` <br />
container for the action descriptors of the object

### `events`
`EventsRegistry` <br /> 
`instance-attribute`, `read-only` <br />
container for the event descriptors of the objec.

### `state`
`str`, `instance-attribute`, `writable` <br />
{{ thing_FSM_state_doc() }}

### `sub_things`
`typing.Dict[str, Thing]` <br /> 
`instance-attribute` <br />
other `Thing`'s that are composed within this `Thing`.
<!-- {{ sub_things_docstring() }} -->

### `logger` 
`logging.Logger` <br />
{{ thing_logger_doc() }}

### `state_machine`
`StateMachine | None` <br />
`class-attribute`, `writable` <br />
the `StateMachine`, `None` when the `Thing` has none. Accessed on an instance it returns a [`BoundFSM`](../state-machine/bound-fsm.md).

### `state_change_event`
`Event` <br />
`class-attribute`, `read-only` <br />
change event pushed whenever `state` changes. Generated automatically because `state` is an
observable `Property`.

### `event_bus`
`EventBus` <br />
`instance-attribute`, `read-only` <br />
the bus this object's events are published through, owned by the
[`EventLoop`](../eventloop/eventloop.md).

### `thing_model`
`ThingModel` <br />
`instance-attribute`, `read-only` <br />
the Thing Model of this object, equivalent to calling `get_thing_model()` with default arguments.


