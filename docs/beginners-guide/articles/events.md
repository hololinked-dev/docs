Events
======

[API Reference](../../../api-reference/events/index.md)

Events are pushed to the client through a publish-subscribe mechanism. Call ``push()`` method on the event to 
publish data to clients:

```py title="Definition" linenums="1" hl_lines="17-21"
--8<-- "docs/howto/code/events/definition.py:5:25"
```

One can subscribe to the event using the attribute name:

```py title="Subscription" linenums="1" hl_lines="9-10"
--8<-- "docs/howto/code/events/event_client.py:1:10"
```
    

One can also supply multiple callbacks which may called in series or threaded:

=== "Sequential"

    ```py title="Providing Callbacks" linenums="1" hl_lines="9"
    --8<-- "docs/howto/code/events/event_client.py:13:22"
    ```

=== "Threaded"

    ```py title="Providing Callbacks" linenums="1" hl_lines="9-10"
    --8<-- "docs/howto/code/events/event_client.py:13:18"
    --8<-- "docs/howto/code/events/event_client.py:24:"
    ```

Schema may be supplied for the validation of the event data on the client:

```py title="" linenums="1" hl_lines="13"
--8<-- "docs/howto/code/events/definition.py:6:6"
--8<-- "docs/howto/code/events/definition.py:50:62"
``` 
    
There is no separate validation on the server side. 


<!-- .. list-table:: Thing Description for Events
   :header-rows: 1

   * - Key
     - Supported
     - Comment
   * - subscription
     - ✖
     -
   * - data
     - ✔
     - payload schema for the event
   * - dataResponse
     - ✖
     - schema for response message after arrival of an event, will be supported in future
   * - cancellation
     - ✖
     - Server sent events can be cancelled by the client directly  -->