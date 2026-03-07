# MQTT

[API Reference](../../../api-reference/protocols/mqtt/index.md)

MQTT does not support request reply pattern in the current implementation of this package,
although the original v5 specification of the protocol might allow it. Consider using a second protocol like HTTP if your device can support it, for the time being. Contributions are welcome. 

## SSL context

To use MQTT over SSL/TLS, one could create an SSL context as follows:

```python linenums="1" title="Use SSL"
import ssl, os

ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
ssl_context.load_verify_locations(cafile="ca.crt")
ssl_context.check_hostname = True
ssl_context.verify_mode = ssl.CERT_REQUIRED
ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2

mqtt_server = MQTTServer(
    host='mqtt.example.com',
    port=8883,
    ssl_context=ssl_context,
)
Oscilloscope(id='oscilloscope').run(servers=[mqtt_server])
```

Note that since MQTT has broker-based architecture and all publishers are clients to the broker,
the SSL context here is created with purpose `ssl.Purpose.SERVER_AUTH`. The certificate (say `ca.crt` above) must be pre-generated while deploying the MQTT broker.

## Overiding Topic Name and QoS

Not supported yet, see issue [here](https://github.com/hololinked-dev/hololinked/issues/134)