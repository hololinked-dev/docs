# Authentication Schemes

Security schemes restrict access to the Thing instance, and are currently available only for HTTP.

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
    from requests.auth import HTTPBasicAuth

    response = requests.get(
        "http://localhost:9000/properties/some_property",
        auth=HTTPBasicAuth("admin", "adminpass")
    )
    print(response.json())
    ```

=== "ObjectProxy"

    ```py title="Usage" linenums="1"
    from hololinked.client import ClientFactory
    from hololinked.client.security import HTTPBasicSecurityScheme

    client = ClientFactory.http(
        "http://localhost:9000/my-thing/resources/wot-td",
        security_scheme=HTTPBasicSecurityScheme(
            username="admin",
            password="adminpass",
            base64_encoding=True
        )
    )
    ```

### API Key Security Scheme

Unimplemented, coming soon. See issue [#111](https://github.com/hololinked-dev/hololinked/issues/111).

### OAuth2 Security Scheme

Unimplemented, coming soon. See issue [#87](https://github.com/hololinked-dev/hololinked/issues/87).
