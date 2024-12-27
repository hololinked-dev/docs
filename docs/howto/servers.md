Expose Python Classes
=====================

Normally, the hardware is interfaced with a computer through Ethernet, USB etc. or any OS supported method, 
and one would write a class to encapsulate its properties and commands. Exposing this class to other processes 
and/or to the network provides access to the hardware for multiple use cases in a client-server model. Such remotely visible 
Python objects are to be made by subclassing from `Thing`: 

```py title="Base Class - Spectrometer Example" linenums="1"
--8<-- "docs/howto/code/thing_inheritance.py"
```

`id` is a unique name recognising the instantiated object. It allows multiple 
hardware of the same type to be connected to the same computer without overlapping the exposed interface. It is therefore a 
mandatory argument to be supplied to the `Thing` parent. Non-experts may use strings composed of 
characters, numbers, forward slashes etc., which looks like a part of a browser URL, but the general definition is 
that `id` should be a URI compatible string:


```py title="ID" linenums="1"
--8<-- "docs/howto/code/thing_basic_example.py:104:107"

```
For attributes (like serial number above), if one requires them to be exposed on the network, one should 
use "properties" defined in `hololinked.server.properties` to "type define" the attributes of the object (in a python sense): 

```py title="Properties" linenums="1"
--8<-- "docs/howto/code/thing_basic_example.py:2:3"
--8<-- "docs/howto/code/thing_basic_example.py:7:19"
```

Apart from [predefined attributes]() like `String`, `Number`, `List` etc., it is possible to create custom properties with [pydantic or JSON schema](). 
Only properties defined in `hololinked.server.properties` or subclass of `Property` object (note the captial 'P') can be exposed to the network, 
not normal python attributes or python's own `property`.

For methods to be exposed on the network, one can use the `action` decorator: 

```py title="Actions" linenums="1"
--8<-- "docs/howto/code/thing_basic_example.py:2:3"
--8<-- "docs/howto/code/thing_basic_example.py:7:22"
--8<-- "docs/howto/code/thing_basic_example.py:29:36"
```

Arbitrary signature is permitted:

```py title="Action with no arguments" linenums="1" 
--8<-- "docs/howto/code/thing_basic_example.py:8:11"
--8<-- "docs/howto/code/thing_basic_example.py:37:40"
```

Properties are usually supposed to model settings, captured data etc. which have a read-write 
operation (also read-only, read-write-delete) and a specific type. Actions are supposed to model 
activities in the physical world, like executing a control routine, start/stop measurement etc. 

To start a server, say a HTTP server, one can call the `run_with_http_server` method after instantiating the `Thing`:

```py title="HTTP Server" linenums="1"
--8<-- "docs/howto/code/thing_basic_example.py:104:108"
```

The exposed properties, actions and events (discussed below) are independent of protocol implementation, therefore,
one can start one or multiple protocols to serve the thing:

```py title="Multiple Protocols" linenums="1"
--8<-- "docs/howto/code/thing_basic_example.py:104:108" 
```

Further, all requests are queued as the domain of operation under the hood is remote procedure calls (RPC) 
mediated completely by ZMQ. Therefore, only one request is executed at a time as 
the hardware normally responds to only one operation at a time (unless one is using some hardware protocol like modbus). 
Further, it is also expected that the internal state of the python object is not inadvertently affected by 
running multiple requests at once to different properties or actions. This can be overcome on need basis manually through threading
or async methods. 

To overload the get-set of properties to directly apply property values onto devices, one may do the following:

```py title="Property Get Set Overload" linenums="1"
--8<-- "docs/howto/code/thing_basic_example.py:61:75"
```  

i.e. supply a `fget` and `fset` method to the Property. In non expert terms, when a custom get-set method is not provided, 
properties look like class attributes however their data containers are instantiated at object instance level by default. 
For example, the `serial_number` property defined 
previously as `String`, whenever set/written, will be complied to a string and assigned as an attribute to each instance 
of the `OceanOpticsSpectrometer` class. This is done with an internally generated name. It is not necessary to know this 
internally generated name as the property value can be accessed again in any python logic, say,
|br|
`self.device = Spectrometer.from_serial_number(self.serial_number)` 
|br|

However, to avoid generating such an internal data container and instead apply the value on the device, one may supply 
custom get-set methods using the fget and fset argument. This is generally useful as the hardware is a better source 
of truth about the value of a property. Further, the write value of a property may not always correspond to a read 
value due to hardware limitations. Say, a linear stage position property write is a command that requests a stage to move to a certain 
position, whereas the read returns the current position. If the stage could not reach the target position due to obstacles,
the write and read values differ. 

Events are to be used to asynchronously push data to clients. For example, one can supply clients with the 
measured data using events:

```py title="Events" linenums="1"
--8<-- "docs/howto/code/thing_basic_example.py:2:3"
--8<-- "docs/howto/code/thing_basic_example.py:7:11" 
--8<-- "docs/howto/code/thing_basic_example.py:16:28"
--8<-- "docs/howto/code/thing_basic_example.py:74:93" 
```

Data may also be polled by the client repeatedly but events save network time or allow sending data which cannot be timed,
like alarm messages. Arbitrary payloads are supported, as long as the data is serializable.   


