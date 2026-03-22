# Serializers

To promote interoperability, safety and ease of integration with web applications, the default content type for all properties, actions and events is the JSON data format - `application/json`.
The default included implementation relies on `C++` (`msgspec`), therefore one need not worry about the performance for a large number of use cases, including lists of 1000 to 10000 floats
and large nested dictionaries or objects.

### Changing the Default Serializer

One would use the `Serializers` singleton to set the desired serialization on the specific property, action or event to overcome the default setting on an individual basis:

```py linenums="1" title="Change Serializer for Specific Properties, Actions or Events" hl_lines="4 10 14"
from hololinked.serializers import Serializers

# Using a pickle serializer for a list property
Serializers.register_for_object(OceanOpticsSpectrometer.spectrum, Serializers.pickle)
# pickle is not recommended, use message pack if possible
# from hololinked.config import global_config
# global_config.ALLOW_PICKLE = True  # default False

# Using message pack for an action or event
Serializers.register_for_object(
    objekt=OceanOpticsSpectrometer.update_background_intensity,
    serializer=Serializers.msgpack
)
Serializers.register_for_object(
    objekt=OceanOpticsSpectrometer.intensity_measurement_event,
    serializer=Serializers.msgpack
)

OceanOpticsSpectrometer(id="spectro1").run_with_http_server()
```

i.e., other properties, actions or events will still use the default (JSON) serialization. By referring the property, action or event at the class level, the data format change will be reflected for all instances. To overload the content type per `Thing` instance, specify the `thing_id` as well:

```py linenums="1" title="Overload per Thing instance" hl_lines="13 15"
from hololinked.serializers import Serializers

spectrometer = OceanOpticsSpectrometer(id='spectro1')

# all instances of OceanOpticsSpectrometer class will use msgpack for spectrum property
Serializers.register_for_object(
    objekt=OceanOpticsSpectrometer.spectrum,
    serializer=Serializers.msgpack
)

# This specific instance will use pickle for spectrum property, 
# other instances will use msgpack
Serializers.register_for_object_per_thing_instance(
    thing_id=spectrometer.id,
    objekt=OceanOpticsSpectrometer.spectrum.name, # accepts only string name
    serializer=Serializers.pickle
)

spectrometer.run(...)
```

To overload the default serializer for the entire `Thing` **instance** altogether: 

```py linenums="1" title="default serializer for thing instance" hl_lines="6-8"
from hololinked.serializers import Serializers

spectrometer = OceanOpticsSpectrometer(id='spectro1')

# instance will use msgpack for all properties, actions and events
Serializers.register_for_thing_instance(
    thing_id=spectrometer.id,
    serializer=Serializers.msgpack
)

# specific property will use pickle, other properties, actions 
# and events will use msgpack
Serializers.register_for_object_per_thing_instance(
    thing_id=spectrometer.id,
    objekt=OceanOpticsSpectrometer.spectrum.name, # accepts only string name
    serializer=Serializers.pickle
)

spectrometer.run(...)
```

The order of priority is as follows (from highest to lowest):

1. Per-Thing-instance overloads for specific properties, actions or events.
2. Per-Thing-instance overloads for the entire Thing instance.
3. Per-Thing-class overloads for specific properties, actions or events.
4. Fallback to the default serializer. It is possible to change the default serializer, see API reference.

The singleton behaviour of `Serializers` ensures that all registrations are available across all protocol servers within the same process.

### Built-in Serializers

The following serializers are supported out of the box:

- `Serializers.json`: Default JSON serializer using `msgspec` library
- `Serializers.msgpack`: MessagePack serializer using `msgspec` library
- `Serializers.pickle`: Python's built-in pickle serializer (not recommended for untrusted clients or servers)
- `Serializers.text`: Plain text serializer for string data

### Custom Serializers

One can create custom serializers by subclassing the `BaseSerializer` and implementing `dumps`, `loads`, and `content_type` methods.
Then, register the custom serializer for a specific property, action or event using the `Serializers` singleton as shown above.

```python linenums="1" title="Custom Serializer" hl_lines="8 10-11 17-18 24-25 29"
from hololinked.serializers import BaseSerializer, Serializers

import imageio
import io
import numpy


class PNGImageSerializer(BaseSerializer):

    @classmethod
    def dumps(cls, image: numpy.ndarray) -> bytes:
        # Implement serialization logic here
        buffer = io.BytesIO()
        imageio.imwrite(buffer, image, format='png')
        return buffer.getvalue()

    @classmethod
    def loads(cls, png: bytes) -> numpy.ndarray:
        # Implement deserialization logic here
        buffer = io.BytesIO(png)
        image = imageio.imread(buffer, format='png')
        return image

    @property
    def content_type(self) -> str:
        return "image/png"

# register the serializer first
Serializers.register(PNGImageSerializer)
# overload the serializer for a specific property/action/event
Serializers.register_for_object(
    objekt=IDSCamera.image,
    serializer=Serializers.PNGImageSerializer
    # use the same name for the serializer as the class name,
    # or a name provided in the register method
)

IDSCamera(id='nearfield').run_with_http_server()
```

All three methods (`dumps`, `loads`, and `content_type`) must be implemented for the custom serializer to work correctly,
otherwise an error will be raised at runtime.
