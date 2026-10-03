# Server

::: hololinked.server
    options:
        show_root_heading: false
        members: false

## Entry points

`run()` and `stop()` knows no protocol in particular — they take already-constructed servers and
drive their lifecycle. Use them when you build servers yourself; `Thing.run(access_points=...)` is
the shorthand that calls `run()`.

::: hololinked.server.run
    options:
        show_root_heading: true
        heading_level: 3

::: hololinked.server.stop
    options:
        show_root_heading: true
        heading_level: 3

::: hololinked.server.parse_params
    options:
        show_root_heading: true
        heading_level: 3
