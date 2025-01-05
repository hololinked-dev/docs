# Expose Python Classes

### Subclass from Thing

Normally, the hardware is interfaced with a computer through Ethernet, USB etc. or any OS supported method, 
and one would write a class to encapsulate its properties and commands. Exposing this class to other processes 
and/or to the network provides access to the hardware for multiple use cases in a client-server model. Such remotely visible 
Python objects are to be made by subclassing from `Thing`: 

```py title="Base Class - Spectrometer Example" linenums="1" hl_lines="8"
--8<-- "docs/howto/code/thing_inheritance.py"
```

`id` is a unique name recognising the instantiated object. It allows multiple 
hardware of the same type to be connected to the same computer without overlapping the exposed interface. It is therefore a 
mandatory argument to be supplied to the `Thing` parent. Non-experts may use strings composed of 
characters, numbers, forward slashes etc., which looks like a part of a browser URL, but the general definition is 
that `id` should be a URI compatible string:

```py title="ID" linenums="1" hl_lines="2"
--8<-- "docs/howto/code/thing_basic_example.py:114:118"
```
### Properties

For attributes (like serial number above), if one requires them to be exposed on the network, one should use "properties" defined in `hololinked.server.properties` to "type define" the attributes of the object (in a python sense): 

```py title="Properties" linenums="1" hl_lines="13"
--8<-- "docs/howto/code/thing_basic_example.py:2:3"
--8<-- "docs/howto/code/thing_basic_example.py:7:19"
```

Apart from [predefined attributes](properties/index.md#predefined-typed-properties) like `String`, `Number`, `List` etc., it is possible to create custom properties with [pydantic or JSON schema](properties/index.md#schema-constrained-property). 
Only properties defined in `hololinked.server.properties` or subclass of `Property` object (note the captial 'P') can be exposed to the network, not normal python attributes or python's own `property`.

### Actions

For methods to be exposed on the network, one can use the `action` decorator: 

```py title="Actions" linenums="1" hl_lines="12"
--8<-- "docs/howto/code/thing_basic_example.py:2:2"
--8<-- "docs/howto/code/thing_basic_example.py:7:11"
--8<-- "docs/howto/code/thing_basic_example.py:16:22"
--8<-- "docs/howto/code/thing_basic_example.py:24:31"
```

Properties usually model settings, captured data etc. which have a read-write 
operation (also read-only, read-write-delete operations) and a specific type. Actions are supposed to model activities in the physical world, like executing a control routine, start/stop measurement etc. Both properties and actions are symmetric, they can invoked from within the object and externally by a client and expected to behave similarly (except while using a state machine).

Actions can take arbitrary signature.

### Serve the Object

To start a server, say a HTTP server, one can call the `run_with_http_server` method after instantiating the `Thing`:

```py title="HTTP Server" linenums="1"
--8<-- "docs/howto/code/thing_basic_example.py:114:119"
```

The exposed properties, actions and events (discussed below) are independent of protocol implementation, therefore,
one can start one or multiple protocols to serve the thing:

```py title="Another Protocol - ZMQ" linenums="1"
--8<-- "docs/howto/code/thing_basic_example.py:114:114"
--8<-- "docs/howto/code/thing_basic_example.py:123:126"
```

Further, all requests are queued as the domain of operation under the hood is remote procedure calls (RPC) 
mediated completely by ZMQ. Therefore, only one request is executed at a time as 
the hardware normally responds to only one operation at a time (unless one is using some hardware protocol like modbus to talk to the hardware). 
Further, it is also expected that the internal state of the python object is not inadvertently affected by 
running multiple requests at once to different properties or actions. This can be overcome on need basis manually through threading
or async methods. If a single request or operation takes 5-10ms, one can still run 100s of operations per second. 

### Overloaded Properties 

To overload the get-set of properties to directly apply property values onto devices, one may supply a custom getter & setter method:

```py title="Property Get Set Overload" linenums="1"
--8<-- "docs/howto/code/thing_basic_example.py:8:12"
--8<-- "docs/howto/code/thing_basic_example.py:37:52"
```  

In non expert terms, when a custom get-set method is not provided, 
properties look like class attributes however their data containers are instantiated at object instance level by default. 
For example, the [`serial_number`](#__codelineno-2-9) property defined 
previously as `String`, whenever set/written, will be complied to a string and assigned as an attribute to each instance 
of the `OceanOpticsSpectrometer` class. This is done with an internally generated name. It is not necessary to know this 
internally generated name as the property value can be accessed again in any python logic, say, <br>
[`self.device = Spectrometer.from_serial_number(self.serial_number)`](#__codelineno-3-17)
<br>

However, to avoid generating such an internal data container and instead apply the value on the device, one may supply 
custom get-set methods using the fget and fset argument. This is generally useful as the hardware is a better source 
of truth about the value of a property. Further, the write value of a property may not always correspond to a read 
value due to hardware limitations. Say, the write value of `integration_time` requested by the user is `1000.2`, however, the device adjusted it to `1000.0` automatically. 

### Push Events

Events are to be used to asynchronously push data to clients. For example, one can supply clients with the 
measured data using events:

```py title="Events" linenums="1" hl_lines="19"
--8<-- "docs/howto/code/thing_basic_example.py:2:2"
--8<-- "docs/howto/code/thing_basic_example.py:7:11"
--8<-- "docs/howto/code/thing_basic_example.py:71:85"
```

Data may also be polled by the client repeatedly but events save network time or allow sending data which cannot be timed,
like alarm messages. Arbitrary payloads are supported, as long as the data is serializable.   

To start the capture method, to receive the events, one may thread it as follows:

```py title="Events" linenums="1" hl_lines="8"
--8<-- "docs/howto/code/thing_basic_example.py:7:12"
--8<-- "docs/howto/code/thing_basic_example.py:86:100"
```

