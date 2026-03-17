# Installation

From pip:

```sh
pip install hololinked
```

From conda:

```sh
conda install -c conda-forge hololinked
```

One may also clone it from github & install directly (in develop mode):

```sh
git clone --no-recurse-submodules https://github.com/hololinked-dev/hololinked.git
# the submodules can be quite hefty and are not necessary
cd hololinked
pip install -e .
```

With `uv`:

```sh
git clone --no-recurse-submodules https://github.com/hololinked-dev/hololinked.git
cd hololinked
uv venv
source .venv/bin/activate # for Linux/Mac
.venv\Scripts\activate # for Windows
uv sync
```
