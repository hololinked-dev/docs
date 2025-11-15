# MQTT

## SSL context

To use MQTT over SSL/TLS, one needs to create an SSL context as follows:

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
the SSL context here is created with purpose `ssl.Purpose.SERVER_AUTH`.
