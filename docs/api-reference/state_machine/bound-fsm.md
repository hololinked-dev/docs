

::: hololinked.core.state_machine.BoundFSM
    options:
        members:
            - set_state
            - get_state
            - contains_object
  

## Attributes

### `current_state`
`str` <br /> 
`instance-attribute`, `writable` <br />
read and write current state of the state machine

### `initial_state`
`str` <br />
`instance-attribute`, `read-only` <br />
initial state of the state machine

### `states`
`List[str]` <br />
`instance-attribute`, `read-only` <br />
list of allowed states

### `on_enter`
`typing.Dict` <br />
`instance-attribute`, `read-only` <br />
callbacks to execute when a certain state is entered

### `on_exit`
`str` <br />
`instance-attribute`, `read-only` <br />
callbacks to execute when a certain state is exited

### `machine`
`typing.Dict[str, List[Callable | Property]]` <br />
`instance-attribute`, `read-only` <br />
state machine definition, i.e. list of allowed properties and actions for each state