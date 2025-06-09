# docs-v2
Documentation in material mkdocs for hololinked

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

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/hololinked-dev/docs-v2/ci.yaml?label=Build%20Docker%20Image)

### skaffold

To develop the documentation with skaffold within a kubernetes cluster, create a skaffold.env file with the following content:

```bash
SKAFFOLD_DEFAULT_REPO=docker.io/<your-docker-username>
```

Then run:

```bash
skaffold dev --module dev-python-docs
```
