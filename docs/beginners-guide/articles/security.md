# Authentication Schemes

Sophisticated security schemes are currently available only for HTTP. MQTT supports username-password and TLS client certificate authentication. More protocols will be supported in the future. This documentation currently discusses only HTTP security schemes, please check MQTT API reference and MQTT broker provider documentation for MQTT authentication. 

### Basic Security Scheme

HTTP Basic authentication with username and password is supported with bcrypt and argon2 hashing schemes. Import the specific flavour and provide the instantiated scheme to the HTTP server:

=== "Server"

    ```py title="Basic Security" linenums="1" hl_lines="4 5 11"
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

=== "Authenticating with 3rd Party Clients"

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

=== "Authenticating with ObjectProxy"

    ```py title="Usage" linenums="1"
    from hololinked.client import ClientFactory
    from hololinked.client.security import BasicSecurity

    client = ClientFactory.http(
        url="http://localhost:9000/my-thing/resources/wot-td",
        security=BasicSecurity(
            username=os.getenv("USERNAME", "admin"),
            password=os.getenv("PASSWORD", "adminpass"),
            base64_encoding=True
        )
    )
    ```

### API Key Security Scheme

Use API keys when there is a requirement to keep track of different clients and expire their access after a definite period. API keys are not tied to any user databases or a fine grained authorization system currently, unlike those used in a platform like github or gitlab. They perform only authentication and are locally stored in your machine in your home folder. 

Before your application uses an API key security, one needs to create it, mostly outside the scope of the server code.

```py title="API Key Creation" linenums="1"
from hololinked.server.security import APIKeySecurity

apikey_security = APIKeySecurity(name="xxx-lab-PC")
apikey_security.create(print_value=True)
```

```
API key created and saved successfully, your key is: wotdat-<id>.<value>, 
please store it securely as it cannot be retrieved later.
# wotdat is a prefix to mean "web of things device access token"
```

Once created, store this key securely and provide it to your client application, as you will not be able to see it again once the terminal session ends. Start the 
server with the API key security scheme, using the same name used during creation:

```py title="API Key Server" linenums="1" hl_lines="4 8"
from hololinked.server.security import APIKeySecurity
from hololinked.core import Thing

apikey_security = APIKeySecurity(name="xxx-lab-PC")
thing = Thing(id="secure-thing")
thing.run_with_http_server(
    port=9000,
    security_scheme=apikey_security
)
```

=== "Authenticating with 3rd Party Clients"

    To use the API key in a HTTP request, pass it in the `x-api-key` header:

    ```py title="Usage" linenums="1"
    import requests

    response = requests.get(
        "http://localhost:9000/secure-thing/some-property",
        headers={"x-api-key": os.getenv("APIKEY", "default-api-key")}
    )
    print(response.json())
    ```

=== "Authenticating with ObjectProxy"

    ```py title="Usage" linenums="1" hl_lines="6"
    from hololinked.client import ClientFactory
    from hololinked.client.security import APIKeySecurity

    client = ClientFactory.http(
        url="http://localhost:9000/my-thing/resources/wot-td",
        security_scheme=APIKeySecurity(value=os.getenv("APIKEY", "default-api-key"))
    )
    ```

### OIDC Security Scheme

For frontend web applications that can support an authorization flow where a user in involved, one can use OIDC or OAuth2 flows to authenticate with the server. In this case, the HTTP server provided by `hololinked` is only a resource server and not an authorization server. The authorization server must be separately taken care by an authentication provider, like Keycloak or Google.

Insantiate the `OIDCSecurityScheme` and supply your authorization server configuration:

```python title="OIDC Security Scheme" linenums="1" hl_lines="1-4 8"
oidc_security = OIDCSecurityScheme(
    issuer=https://example.com,
    audience='device-server'
)
thing = Thing(id="secure-thing")
thing.run_with_http_server(
    port=9000,
    security_scheme=oidc_security
)
```

The security scheme is called OIDC security scheme as it only validates logged in user sessions, the roles/scopes of the token issued and optionally, the audience. It might be erroneous to call it an OAuth flow as the token is not used to fetch information from a third party application about the user. 

Implement the login flow on the client and supply the JWT bearer token in the Authorization header. There are no full fledged OIDC token mediation implemented within `hololinked` as the user must be involved in some form or other. 


