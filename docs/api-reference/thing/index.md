

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


