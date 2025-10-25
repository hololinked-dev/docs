# Serializers

To promote interoperability and ease of integration with web applications, the default content type for all properties, actions and events is `application/json`.
Moreover, a `C++` implementation of JSON (`msgspec`) is used, therefore one need not worry about the performance for a large number of use cases, including lists of 1000 to 10000 floats
and large nested objects.

### Changing the Default Serializer

Based on application requirements, it is possible to change the serialization format on an individual basis by using the `Serializers` singleton.
Set the desired serialization on the specific property, action or event on the `Thing` subclass:

```py linenums="1"
from hololinked.serializers import Serializers

# Using a pickle serializer for a list property
Serializers.register_for_object(OceanOpticsSpectrometer.spectrum, Serializers.pickle)
# pickle is not recommended, use message pack if possible

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

Other properties, actions or events will still use the default JSON serialization.

To overload the content type for an object per thing instance:

```py linenums="1"
from hololinked.serializers import Serializers

spectrometer = OceanOpticsSpectrometer(id='spectro1')

# all instances of OceanOpticsSpectrometer class will use msgpack for spectrum property
Serializers.register_for_object(
    objekt=OceanOpticsSpectrometer.spectrum,
    serializer=Serializers.msgpack
)

# specific instance will use pickle for spectrum property, other instances will use msgpack
Serializers.register_for_object_per_thing_instance(
    thing_id=spectrometer.id,
    objekt=OceanOpticsSpectrometer.spectrum.name, # accepts only string name
    serializer=Serializers.pickle
)

spectrometer.run(...)
```

To overload the default serializer for a `Thing` **instance**:

```py linenums="1"
from hololinked.serializers import Serializers

spectrometer = OceanOpticsSpectrometer(id='spectro1')

# instance will use msgpack for all properties, actions and events
Serializers.register_for_thing_instance(
    thing_id=spectrometer.id,
    serializer=Serializers.msgpack
)

# specific property will use pickle, other properties, actions and events will use msgpack
Serializers.register_for_object_per_thing_instance(
    thing_id=spectrometer.id,
    objekt=OceanOpticsSpectrometer.spectrum.name, # accepts only string name
    serializer=Serializers.pickle
)

spectrometer.run(...)
```

per-instance overloads have higher priority than the per-thing-object registrations. The singleton behaviour of `Serializers`
ensures that all registrations are available across all protocol servers within the same process.

### Built-in Serializers

The following serializers are supported out of the box:

- `Serializers.json`: Default JSON serializer using `msgspec` library
- `Serializers.msgpack`: MessagePack serializer using `msgspec` library
- `Serializers.pickle`: Python's built-in pickle serializer (not recommended for untrusted clients or servers)
- `Serializers.text`: Plain text serializer for string data

### Custom Serializers

One can create custom serializers by subclassing the `BaseSerializer` and implementing `dumps`, `loads`, and `content_type` methods.
Then, register the custom serializer for a specific property, action or event using the `Serializers` singleton as shown above.

```python
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
