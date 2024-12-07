---
title: Introduction
description: hololinked introduces SCADA & IoT systems to beginners
---

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
- properties are validated get-set attributes of the class which may be used to model settings, hold captured/computed data or generic network accessible quantities. For example 
    <ul style="list-style-type: square;"> 
        <li>an oscilloscope can have properties like time resolution, time range, data attributes for each channel etc.</li>
        <li>a camera can have properties like frame rate, exposure time, captured image</li>
        <li>the current voltage, voltage range, maximum allowed current can be properties of a DC power supply</li>
    </ul>
- actions are methods that command the hardware to perform some operation or run arbitray python logic
    <ul style="list-style-type: square;"> 
        <li>connect/disconnect hardware from computer or raspberry pi</li>
        <li>DC power supply should execute a closed loop control routine</li>
        <li>oscillscope should start/stop measurement</li>
    </ul>
- events can asynchronously communicate/push arbitrary data to a client, like alarm messages, streaming measured quantities etc.
    <ul style="list-style-type: square;"> 
        <li>camera may stream the images as events</li>
        <li>DC power supply may raise an alarm when the current value exceeds the allowed value</li>
    </ul>
- Additionally, a state machine may constrain property and action execution
    <ul style="list-style-type: square;"> 
        <li>camera may not change the exposure time while capturing video</li>
        <li>oscilloscope should not start a fresh measurement when a measurement is already ongoing</li>
    </ul>
