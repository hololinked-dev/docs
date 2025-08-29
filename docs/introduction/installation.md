# Installation

From pip:

    pip install hololinked

From conda:

    conda install -c conda-forge hololinked

One may also clone it from github & install directly (in develop mode):

    git clone https://github.com/VigneshVSV/hololinked.git
    cd hololinked
    pip install -e .

One could setup a virtual environment from the included `hololinked.yml` file:

    conda env create -f hololinked.yml
    conda activate hololinked
    pip install -e .

With `uv`:

    uv venv hololinked
    source venv/bin/activate # for Linux/Mac
    .venv\Scripts\activate # for Windows
    uv sync
