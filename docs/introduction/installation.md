Installation 
============

From pip:

    pip install hololinked

From conda:

    conda install -c conda-forge hololinked

One may also clone it from github & install directly (in develop mode):

    git clone https://github.com/VigneshVSV/hololinked.git
    cd hololinked
    pip install -e .

One could setup a conda environment from the included ``hololinked.yml`` file:

    conda env create -f hololinked.yml 
    conda activate hololinked
    pip install -e .

To build & host docs locally, in top directory:

    conda activate hololinked
    cd doc
    make clean 
    make html
    python -m http.server --directory build\html

To open the docs in the default browser, one can also issue the following instead of starting a python server 

    make host-doc



