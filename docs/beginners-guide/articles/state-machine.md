[API Reference](../../api-reference/state-machine/state-machine.md)

Often, certain operations are not allowed during certain conditions, for example,
one cannot turn ON a motor twice in a row, or a measurement device cannot modify a setting change if a measurement is ongoing.

To implement these contraints, a state machine may be used to prevent property writes or
action invokations in certain states (events are not supported). A `StateMachine` is a class-level
attribute which accepts a finite list of states and the allowed properties and actions
in these states:

```py title="Definition" linenums="1"
--8<-- "docs/beginners-guide/code/fsm/def.py:1:1"
--8<-- "docs/beginners-guide/code/fsm/def.py:13:15"
--8<-- "docs/beginners-guide/code/fsm/def.py:30:33"
--8<-- "docs/beginners-guide/code/fsm/def.py:37:38"
```

Specify the machine conditions as keyword arguments to the `state_machine` with properties and actions
in a list:

```py title="Specify Properties and Actions" linenums="1"
--8<-- "docs/beginners-guide/code/fsm/def.py:1:2"
--8<-- "docs/beginners-guide/code/fsm/def.py:12:38"
```

One needs to set the `StateMachine` state to indicate state changes:

```py title="set_state()" linenums="1"
--8<-- "docs/beginners-guide/code/fsm/def.py:13:15"
--8<-- "docs/beginners-guide/code/fsm/def.py:54:63"
```

One can also sepcify the allowed state of a property or action directly
on the corresponding objects:

```py title="Specify State Directly on Object" linenums="1"
--8<-- "docs/beginners-guide/code/fsm/def.py:13:15"
--8<-- "docs/beginners-guide/code/fsm/def.py:64:74"
```

## State Change Events

State machines also push state change event when the state changes:

```py title="Definition" linenums="1" hl_lines="7"
--8<-- "docs/beginners-guide/code/fsm/def.py:13:16"
--8<-- "docs/beginners-guide/code/fsm/def.py:41:48"
```

One can suppress state change events by setting:

```python title="suppress state change event"
self.state_machine.set_state('STATE', push_event=False)
```

```python title="subscription" linenums="1"
def state_change_cb(event):
    print(f"State changed to {event.data}")

client.observe_property(name="state", callbacks=state_change_cb)
```

> One can supply multiple callbacks which may called in series or concurrently - see [Events](events.md#subscription).

## State Change Callbacks

One can also supply callbacks which are executed when entering and exiting certain states,
irrespective of where or when the state change occured:

```py title="enter and exit callbacks" linenums="1" hl_lines="21"
--8<-- "docs/beginners-guide/code/fsm/def.py:13:15"
--8<-- "docs/beginners-guide/code/fsm/def.py:75:"
```

The state name and the list of callbacks are supplied as a dictionary to the `on_enter` and `on_exit` arguments.
These callbacks are executed after the state change is effected, and are mostly useful when there are state changes at multiple places in the code which need to trigger the same side-effects.
