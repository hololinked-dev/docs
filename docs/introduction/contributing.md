# Contributing to hololinked

We welcome contributions to `hololinked`! All types of contributions are encouraged and valued.

> If you like the project, but just don't have time to contribute, that's fine. There are other easy ways to support the project and show your appreciation, which we would also be very happy about:
>
> - Star the project
> - Tweet about it or share in social media
> - Create examples & refer this project in your project's readme. I can add your example in my [example repository](https://github.com/VigneshVSV/hololinked-examples) if its really helpful, including use cases in more sophisticated integrations
> - Mention the project at local meetups/conferences and tell your friends/colleagues
> - [Donate](https://github.com/sponsors/VigneshVSV) to cover the costs of maintaining it

You can contribute in the following ways:

- reporting bugs and issues
- submitting code
- improving documentation
- suggesting new features
- submitting examples or implementations

For good first issues, visit repository wise:

- [hololinked](https://github.com/hololinked-dev/hololinked/issues?q=is%3Aissue%20state%3Aopen%20label%3A%22good%20first%20issue%22)
- [examples](https://github.com/hololinked-dev/examples/issues?q=is%3Aissue%20state%3Aopen%20label%3A%22good%20first%20issue%22)
- [control panel](https://github.com/hololinked-dev/thing-control-panel/issues?q=is%3Aissue%20state%3Aopen%20label%3A%22good%20first%20issue%22)
- [documentation](https://github.com/hololinked-dev/docs-v2/issues?q=is%3Aissue%20state%3Aopen%20label%3A%22good%20first%20issue%22)
- [additional/new projects](https://github.com/hololinked-dev/.github/issues)

Our [contribution guidelines](https://github.com/hololinked-dev/hololinked/blob/main/CONTRIBUTING.md) may also help. There are also [weekly office hours](https://github.com/hololinked-dev#monthly-meetings) & [discord group](https://discord.com/invite/kEz87zqQXh) (currently no participants).

> Please do note that we are only looking for code contributions that can enfore code ownership and integrating contributors that can understand the codebase, not AI automated PRs. All solutions anybody can automate can also be automated by us, so, this is not the purpose of accepting contributions. 

## Setup Development Environment

<a name="development-with-uv"></a>
One can setup a development environment with [uv](https://docs.astral.sh/uv/) as follows:

1. Install uv if you don't have it already: [uv docs](https://docs.astral.sh/uv/getting-started/installation/)
2. Create and activate a virtual environment:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install the package in development mode with all dependencies:
```bash
uv sync
# or
uv sync --no-install-project
uv pip install -e ".[dev,test]"
```

## Running Tests

To run unit and integration tests:
```bash
pytest -s -v tests
```

You might need docker daemon for running some tests (currently `test_16_protocols_mqtt`).

## Pre-commit Hooks

You can use pre-commit hooks to ensure code quality before committing changes, and be ensured that certain pipeline checks will pass.

```bash
python -m pip install pre-commit
pre-commit install
pre-commit run --all-files
```

Currently `ruff`, `bandit` and `gitleaks` are configured to run as pre-commit hooks.

Precommit hooks are optional. To skip them, use:

```bash
git commit --no-verify -m "Your commit message"
```
