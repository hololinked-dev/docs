Events
======

Events are pushed to the client through a publish-subscribe mechanism. The clients subscribe to an event and receive
data whenever a ``push()`` method is called on the event:

.. literalinclude:: ../code/events/definition.py
    :language: python
    :linenos:
    :lines: 2-34, 64-

On the client suppplied along with package, one can subscribe to it using both the friendly name and the attribute name:

.. literalinclude:: ../code/events/event_client.py
    :language: python
    :linenos:
    :lines: 1-13

One can also supply multiple callbacks which may called in series or threaded:

.. literalinclude:: ../code/events/event_client.py
    :language: python
    :linenos:
    :lines: 15-

HTTP client:

.. literalinclude:: ../code/events/subscription.js
    :language: javascript
    :linenos:
    

Schema may be supplied for validation of the event data on the client:

.. literalinclude:: ../code/events/definition.py
    :language: python
    :linenos:
    :lines: 6, 49-62

There is no separate validation on the server side. 

.. code-block:: javascript

    // node-wot client
    energy_meter.subscribeEvent("data_point_event", async(data) => {
        const value = await data.value()
        console.log("event : ", value)            
    }).then((subscription) => {
        console.debug("subscribed to data point event")
    })

.. list-table:: Thing Description for Events
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
     - Server sent events can be cancelled by the client directly 