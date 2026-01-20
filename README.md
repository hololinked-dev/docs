# hololinked docs

Documentation in material mkdocs for [hololinked](https://github.com/hololinked-dev/hololinked).

To build the documentation, while setting up a local development environment with `uv` (`pip install uv`), run:

```bash
uv venv
source .venv/bin/activate # or venv\Scripts\activate on Windows
uv sync --no-install-project
mkdocs build
```

or

```bash
mkdocs serve
```

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/hololinked-dev/docs/ci.yaml?label=Build%20And%20Publish%20Website)

> This project is always looking for contributors to improve the documentation in a **hand-written** fashion.
> Hop into our [Discord](https://discord.com/invite/kEz87zqQXh) to discuss upfront if needed and make a PR with your changes.
> Contributions can include proof reading, language improvements, adding new sections, examples or tutorials, etc.

### skaffold

To develop the documentation with skaffold within a kubernetes cluster, create a `skaffold.env` file specifying the docker registry. For example, if you are using Docker Hub, it should look like this:

```bash
SKAFFOLD_DEFAULT_REPO=docker.io/<your-docker-username>
```

Please get in touch with me [by email](mailto:info@hololinked.dev) or on [discord](https://discord.com/invite/kEz87zqQXh) for cluster credentials.

```bash
skaffold dev --module dev-python-docs
```

Or use your own cluster if you have one set up. To test if the image is building

```bash
skaffold build --module dev-python-docs
```

### Docker

To build, tag, and publish the Docker image from your local machine, run:

```sh
set -e
docker build -t hololinked-docs .
docker tag hololinked-docs:latest ghcr.io/hololinked-dev/hololinked-docs:latest
docker push ghcr.io/hololinked-dev/hololinked-docs:latest
echo "Docker image built and pushed successfully."
```
