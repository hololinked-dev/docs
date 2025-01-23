

::: hololinked.core.Thing
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
`instance-attribute`, `read-only` <br />

### `actions`
`instance-attribute`, `read-only` <br />

### `events`
`instance-attribute`, `read-only` <br />


### `sub_things`
`typing.Dict[str, Thing]` <br /> 
`instance-attribute` <br />
other `Thing`'s that are composed within this `Thing`.
<!-- {{ sub_things_docstring() }} -->

### `logger` 
`logging.Logger` <br />
{{ thing_logger_doc() }}

### `state`
`str` | `Enum`, `instance-attribute`, `writable` <br />
{{ thing_FSM_state_doc() }}
