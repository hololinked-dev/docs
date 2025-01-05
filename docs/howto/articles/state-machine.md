Using Finite State Machine
--------------------------

[API Reference](../../api-reference/thing/state-machine.md)

Often, certain operations are not allowed during certain conditions, for example, 
one cannot turn ON a motor twice in a row, or one does not wish to change the 
exposure of a camera during video capture (say).

To implement these contraints, a state machine may be used to prevent property writes or 
action invokations in certain states (events are not supported). A `StateMachine` is a class-level 
attribute which accepts a finite list of states and the allowed properties and actions 
in these states:

```py title="Definition" linenums="1"
--8<-- "docs/howto/code/fsm/def.py:1:1"
--8<-- "docs/howto/code/fsm/def.py:12:15"
--8<-- "docs/howto/code/fsm/def.py:34:36"
--8<-- "docs/howto/code/fsm/def.py:40:41"
``` 
   
Specify the machine conditions as keyword arguments to the `state_machine` with properties and actions 
in a list:

```py title="Specify Properties and Actions" linenums="1"
--8<-- "docs/howto/code/fsm/def.py:1:2"
--8<-- "docs/howto/code/fsm/def.py:12:41"
```

As expected, one needs to set the `StateMachine` state to indicate state changes:

```py title="set_state()" linenums="1"
--8<-- "docs/howto/code/fsm/def.py:13:15"
--8<-- "docs/howto/code/fsm/def.py:54:63"
```

One can also sepcify the allowed state of a property or action directly
on the corresponding objects:

```py title="Specify State Alternate" linenums="1"
--8<-- "docs/howto/code/fsm/def.py:13:15"
--8<-- "docs/howto/code/fsm/def.py:64:"
```

State machines also push state change event when the state changes:

```py title="Definition" linenums="1"
```

One can suppress state change events by setting ``push_state_change_event=False``.

Lastly, one can also supply callbacks which are executed when entering and exiting certain states, 
irrespective of where or when the state change occured:

```py title="Definition" linenums="1"
```