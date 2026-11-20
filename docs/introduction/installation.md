# Installation

From pip:

```sh
pip install hololinked
```

From conda:

```sh
pip install aiomqtt
conda install -c conda-forge hololinked
```

One may also clone it from github & install directly (in develop mode):

```sh
git clone https://github.com/hololinked-dev/hololinked.git
cd hololinked
pip install -e .
```

With `uv`:

```sh
git clone https://github.com/hololinked-dev/hololinked.git
cd hololinked
uv venv
source .venv/bin/activate # for Linux/Mac
.venv\Scripts\activate # for Windows
uv sync
```

The `docs` submodule is not needed to install or develop hololinked, and is not checked out by default. To check it out:

```sh
git submodule update --init --checkout docs
```
