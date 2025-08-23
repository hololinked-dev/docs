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

### skaffold

To develop the documentation with skaffold within a kubernetes cluster, create a `skaffold.env` file specifying the docker registry. For example, if you are using Docker Hub, it should look like this:

```bash
SKAFFOLD_DEFAULT_REPO=docker.io/<your-docker-username>
```

You need to sparse checkout the [vps-kubernetes-cluster repository](https://github.com/hololinked-dev/vps-kubernetes-cluster), which will be already available as a submodule in this repo in the `deployment\vps-kubernetes-cluster` directory. Instructions are available in the shell script `deployment/sparse-checkout.sh`. Sparse checkout is optional but the submodule must be available locally for the skaffold to work.

Once the ingress and apps helm chart is available locally, run:

```bash
skaffold dev --module dev-python-docs
```
