# Authentication Schemes

Security schemes are currently available only for HTTP.

### Basic Security Scheme

HTTP Basic authentication with username and password is supported with bcrypt and argon2 hashing schemes. To enable basic authentication, one needs to set the `security_scheme` attribute of the (HTTP-)server:

=== "Server"

    ```py title="Definition" linenums="1"
    from hololinked.server.security import BcryptSecurityScheme, Argon2SecurityScheme

    security = BcryptSecurityScheme(
        username=os.getenv("USERNAME", "admin"),
        password=os.getenv("PASSWORD", "adminpass"),
        base64_encoding=True  # Optional but recommended to avoid human readability
    )
    thing = Thing(id="secure-thing")
    thing.run_with_http_server(
        port=9000,
        security_scheme=security
    )
    ```

=== "3rd Party Clients"

    ```py title="Usage" linenums="1"
    import requests
    from base64 import b64encode
    from requests.auth import HTTPBasicAuth

    response = requests.get(
        "http://localhost:9000/secure-thing/some-property",
        headers=dict(
            Authorization=f"Basic {b64encode(bytes(f'{os.getenv("USERNAME", "admin")}:{os.getenv("PASSWORD", "adminpass")}', "utf-8")).decode('utf-8')}"
        ),
    )
    print(response.json())
    ```

=== "ObjectProxy"

    ```py title="Usage" linenums="1"
    from hololinked.client import ClientFactory
    from hololinked.client.security import HTTPBasicSecurityScheme

    client = ClientFactory.http(
        url="http://localhost:9000/my-thing/resources/wot-td",
        security_scheme=HTTPBasicSecurityScheme(
            username=os.getenv("USERNAME", "admin"),
            password=os.getenv("PASSWORD", "adminpass"),
            base64_encoding=True
        )
    )
    ```

### API Key Security Scheme

Use API keys when there is a requirement to keep track of different 
clients and expire their access after a definite period. API keys are not tied to any user database or authorizations, 
currently, unlike those used in a platform like github or gitlab. They perform only authentication. 

Before your application uses an API key security, one needs to create it, mostly outside the scope of the server code.

```py title="API Key Creation" linenums="1"
from hololinked.server.security import APIKeySecurity

apikey_security = APIKeySecurity(name="xxx-lab-PC")
apikey_security.create(print_value=True)
```

```
API key created and saved successfully, your key is: wotdat-<id>.<value>, please store it securely as it cannot be retrieved later.
# wotdat is a prefix to mean "web of things device access token"
```

Once created, store this key securely as you will not be able to see it again once the terminal session ends. Start the 
server with the API key security scheme, using the same name used during creation:

```py title="API Key Server" linenums="1"
from hololinked.server.security import APIKeySecurity
from hololinked.core import Thing

apikey_security = APIKeySecurity(name="xxx-lab-PC")
thing = Thing(id="secure-thing")
thing.run_with_http_server(
    port=9000,
    security_scheme=apikey_security
)
```

=== "3rd Party Clients"

    To use the API key in a HTTP request, pass it in the `x-api-key` header:

    ```py title="Usage" linenums="1"
    import requests

    response = requests.get(
        "http://localhost:9000/secure-thing/some-property",
        headers={"x-api-key": os.getenv("APIKEY", "default-api-key")}
    )
    print(response.json())
    ```

=== "ObjectProxy"

    ```py title="Usage" linenums="1"
    from hololinked.client import ClientFactory
    from hololinked.client.security import APIKeySecurity

    client = ClientFactory.http(
        url="http://localhost:9000/my-thing/resources/wot-td",
        security_scheme=APIKeySecurity(value=os.getenv("APIKEY", "default-api-key"))
    )
    ```

### OIDC Security Scheme

Coming soon. See issue [#87](https://github.com/hololinked-dev/hololinked/issues/87) 
