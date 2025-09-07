# Installation

From pip:

    pip install hololinked

From conda:

    conda install -c conda-forge hololinked

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
uv venv hololinked
source venv/bin/activate # for Linux/Mac
.venv\Scripts\activate # for Windows
uv sync
```
