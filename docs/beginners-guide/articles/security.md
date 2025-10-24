# Authentication Schemes

### Basic Security Scheme

HTTP Basic authentication with username and password is supported with bcrypt and argon2 hashing schemes. To enable basic authentication, one needs to set the `security_scheme` attribute of the `Thing` class:

```py title="Definition" linenums="1"
from hololinked.server.security import BcryptSecurityScheme

security = BcryptSecurityScheme(
    username=os.getenv("USERNAME", "admin"),
    password=os.getenv("PASSWORD", "adminpass"),
    base64_encoding=True # Optional
)
thing = Thing(id="secure-thing")
thing.run_with_http_server(
    port=9000,
    security_scheme=security
)
```

### API Key Security Scheme

Unimplemented, coming soon. See issue [#111](https://github.com/hololinked-dev/hololinked/issues/111) if you want to implement it.

### OAuth2 Security Scheme

Unimplemented, coming soon. See issue [#87](https://github.com/hololinked-dev/hololinked/issues/87) if you want to implement it.
