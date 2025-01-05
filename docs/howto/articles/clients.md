# Connecting to Things with Clients

One can always use native protocol-specific clients to access the resources exposed by the server. For example, 
when using a HTTP server, it is possible to use web browser provided clients like ``XMLHttpRequest`` and ``EventSource`` object. 
However, it is also recommended to abstract the operations to be performed on each property, action & event:

# Using `hololinked.client`

If one is not interested in HTTP because web development is not necessary, or one is not knowledgable to write a HTTP interface, 
one may use the ZMQ transport. Objects can be locally exposed only to other processes 
within the same computer using inter-process communication or use TCP for simplicity. Moreover, for certain applications, 
for example, oscilloscope traces consisting of millions of data points, or, camera images or video streaming with raw pixel density 
& no compression, the ZMQ transport may significantly speed up the data transfer rate. To achieve this, one may use a different serializer 
like MessagePack or pickle instead of JSON.

Start the ``Thing`` with/without HTTP server as follows to support multiple protocols:

.. literalinclude:: code/thing_without_http_server.py
    :language: python
    :linenos: 
    :lines: 10-13, 68-87

Then, import the ``ObjectProxy`` and specify the ZMQ transport method and ``instance_name`` to connect to the server and 
the object it serves: 

.. literalinclude:: code/zmq_client.py
    :language: python
    :linenos: 
    :lines: 1-9

The exposed properties, actions and events then become available on the client. One can use get-set on properties and method 
calls on actions similar to how its done natively on the object instance as seen above. To subscribe to events, provide a callback 
which is executed once an event arrives:

.. literalinclude:: code/zmq_client.py 
    :language: python 
    :linenos: 
    :lines: 24-30

One would be using such logic in a PyQt graphical interface, python dashboard apps or custom scripts. To use multiple ZMQ transports:

.. literalinclude:: code/thing_without_http_server.py 
    :language: python
    :linenos: 
    :lines: 81, 90-93

Irrespective of client's request origin, requests are always queued before executing. 

If one needs type definitions for the client because the client does not know the server to which it is connected, one 
can import the server script ``Thing`` and set it as the type of the client as a quick-hack. 

.. literalinclude:: code/zmq_client.py 
    :language: python 
    :linenos: 
    :lines: 15-20

The serializers on the ZMQ client and server must match for connection to proceed without faults. 
JSON is the default, and currently the only supported serializer for HTTP applications.  

Using ``node-wot`` HTTP(s) client
---------------------------------

``node-wot`` is an interoperable Javascript server & client implementation provided by the 
`Web of Things Working Group <https://www.w3.org/WoT/>`_. One can implement both servers and 
clients for hardware with this tool, therefore, if one requires a different coding style and language compared to 
python, one can try ``node-wot``. 

For this package, ``node-wot`` can serve as a HTTP(s) client with predefined features. It supports many protocols apart from HTTP(s), 
however the overarching general purpose of this tool is to be able to interact with hardware with a web standard compatible JSON(-LD) 
specification called as the `Thing Description <https://www.w3.org/TR/wot-thing-description11/>`_. Among other things, the said JSON specifcation 
describes the hardware's available properties, actions and events, along with security definitions to access them.

``node-wot`` can consume such a specification to allow interoperability irrespective of protocol implementation and application domain. 
Further, the Thing Description provides human- and machine-readable documentation of the hardware within the specification itself, 
enhancing developer experience. |br| 
Here, we stick to HTTP(s) client usage of ``node-wot``. For example, consider the ``serial_number`` property defined previously, 
the following JSON, which is a part of the Thing Description, can describe the property:

.. literalinclude:: code/node-wot/properties.json 
    :language: JSON
    :linenos:

The ``type`` field refers to the JSON type of the property value. It can contain other JSON compatible types including 
``object`` or ``array``. The ``forms`` field indicate how to interact with the property. 
For read and write property (value of ``op`` field), the suggested default HTTP methods are GET and PUT respectively
specfied under ``htv:methodName``. ``forms`` may be described as - "make a HTTP request to a submission target 
specified by a URL (href) with a certain HTTP method to perform a certain operation", like a form in a web page where a certain input is 
submitted to the server. 

Similarly, ``connect`` action may be described as follows: 

.. literalinclude:: code/node-wot/actions.json 
    :language: JSON
    :linenos:

Here, again the ``forms`` indicate how to invoke the action & the content type for the payload required to invoke the action. 
In case of this package, since actions are object methods, the payload are the arguments of the method. One has to explicitly 
specify the payload schema otherwise payloads cannot be sent:

.. code-block:: python

    connect_args = {
        "type": "object",
        "properties": {
            "trigger_mode": {"type": "integer"},
            "integration_time": {"type": "number"}
        },
        "additionalProperties": False
    }

    class OceanOpticsSpectrometer(Thing):

        @action(input_schema=connect_args)
        def connect(self, trigger_mode, integration_time):
            self.device = Spectrometer.from_serial_number(self.serial_number)
            if trigger_mode:
                self.device.trigger_mode(trigger_mode)
            if integration_time:
                self.device.integration_time_micros(integration_time)

The response is described in the ``output`` field of the action's description (``output_schema`` in the action decorator) and 
may be omitted if it is python's ``None``. In general, the request and response contents are JSON (i.e having the same ``contentType``)
and therefore specified only once in the form in this case. Since, currently, only JSON serializer is supported for HTTP protocol in this package, 
another content type is not possible. However, in the general Thing Description itself, it is possible to separate 
the request and response content types if necessary.

Regarding events, consider the ``measurement_event`` event:

.. literalinclude:: code/node-wot/events.json 
    :language: JSON
    :linenos:

The ``op`` ``subscribeevent`` dictates that the event may be subscribed using the ``subprotocol`` SSE/HTTP SSE. The ``data`` field 
specifies the payload schema of the event. The payload specification are always validated against the received data by ``node-wot``. 

It might be already understandable that from such a JSON specification, it is clear how to interact with the specified property, 
action or event. The ``node-wot`` HTTP(s) client consumes such a specification to provide these interactions for the developer. 
Therefore, they are also called `interaction affordances` in the Web of Things terminology - "what interactions are provided (or afforded) 
by the server or the Thing to the client". Properties are called Property Affordance, Actions - Action Affordance and Events - Event Affordance. 
The payloads are called Data Schema indicating that they stick to JSON schema specification.

To use the node-wot client on the browser:

.. literalinclude:: code/node-wot/intro.js
    :language: javascript
    :linenos: 
    :lines: 1-17, 39

First, the thing description must be fetched and consumed. Servient is the main object that allows both ``node-wot`` clients and servers
to co-exist. Once consumed, the properties, actions and events may be accessed as follows:

.. literalinclude:: code/node-wot/intro.js
    :language: javascript
    :linenos: 
    :lines: 8-9, 17-



