# hololinked - Pythonic Object-Oriented Supervisory Control & Data Acquisition / Internet of Things

`hololinked` is a beginner-friendly server side pythonic tool suited for instrumentation control and data acquisition over network, especially with HTTP. If you have a requirement to control and capture data from your hardware/instrumentation, show the data in a browser/dashboard, provide a GUI or run automated scripts, hololinked can help. Even for isolated applications or a small lab setup without networking concepts, one can still separate the concerns of the tools that interact with the hardware & the hardware itself.

 
[![Documentation Status](https://readthedocs.org/projects/hololinked/badge/?version=latest)](https://hololinked.readthedocs.io/en/latest/?badge=latest) [![PyPI](https://img.shields.io/pypi/v/hololinked?label=pypi%20package)](https://pypi.org/project/hololinked/) [![Anaconda](https://anaconda.org/conda-forge/hololinked/badges/version.svg)](https://anaconda.org/conda-forge/hololinked)
[![codecov](https://codecov.io/gh/VigneshVSV/hololinked/graph/badge.svg?token=JF1928KTFE)](https://codecov.io/gh/VigneshVSV/hololinked) 
<br>
[![PyPI - Downloads](https://img.shields.io/pypi/dm/hololinked?label=pypi%20downloads)](https://pypistats.org/packages/hololinked)
[![Conda Downloads](https://img.shields.io/conda/d/conda-forge/hololinked)](https://anaconda.org/conda-forge/hololinked)



`hololinked` is compatible with the [Web of Things](https://www.w3.org/WoT/) recommended pattern for developing hardware/instrumentation control software. 
Each device or thing can be controlled systematically when their design in software is segregated into properties, actions and events. In object oriented terms:

- the hardware is (generally) represented by a class 
- properties are validated get-set attributes of the class which may be used to model settings, hold captured/computed data or generic network accessible quantities
- actions are methods which issue commands like connect/disconnect, execute a control routine, start/stop measurement, or run arbitray python logic
- events can asynchronously communicate/push arbitrary data to a client, like alarm messages, streaming measured quantities etc.
- Additionally, a state machine may constrain property and action execution