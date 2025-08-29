---
title: Introduction
description: hololinked introduces SCADA & IoT systems to beginners
---

# hololinked - Pythonic Object-Oriented Supervisory Control & Data Acquisition / Internet of Things

`hololinked` is a beginner-friendly pythonic tool suited for instrumentation control and data acquisition over network (IoT & SCADA).

As a novice, you have a requirement to control and capture data from your hardware, say in your electronics or science lab, and you want to show the data in a dashboard, provide a PyQt GUI, run automated scripts, scan routines or jupyter notebooks, `hololinked` can help. Even for isolated desktop applications or a small setup without networking, one can still separate the concerns of the tools that interact with the hardware & the hardware itself.

If you are a web developer or an industry professional looking for a web standards compatible (high-speed) IoT runtime, `hololinked` can be a decent choice. By conforming to [W3C Web of Things](https://www.w3.org/WoT/), one can expect a consistent API and flexible bidirectional message flow to interact with your devices, irrespective of the underlying protocol. Currently HTTP & ZMQ are supported. See [Use Cases Table](#use-cases-table).

This implementation is based on RPC.

<div align="left">

<a href="https://github.com/hololinked-dev/docs">
    <img src="https://img.shields.io/github/actions/workflow/status/hololinked-dev/docs/ci.yaml?label=Build%20And%20Publish%20Docs" alt="Documentation Status">
</a>
<a href="https://pypi.org/project/hololinked/">
    <img src="https://img.shields.io/pypi/v/hololinked?label=pypi%20package" alt="PyPI">
</a>
<a href="https://anaconda.org/conda-forge/hololinked">
    <img src="https://anaconda.org/conda-forge/hololinked/badges/version.svg" alt="Anaconda">
</a>
<a href="https://codecov.io/github/hololinked-dev/hololinked">
    <img src="https://codecov.io/github/hololinked-dev/hololinked/graph/badge.svg?token=5DI4XJ2KX9" alt="codecov">
</a>
<a href="https://anaconda.org/conda-forge/hololinked">
    <img src="https://img.shields.io/conda/d/conda-forge/hololinked" alt="Conda Downloads">
</a>
<a href="https://pypistats.org/packages/hololinked">
    <img src="https://img.shields.io/pypi/dm/hololinked?label=pypi%20downloads" alt="PyPI - Downloads">
</a>
<a href="https://doi.org/10.5281/zenodo.12802841">
    <img src="https://zenodo.org/badge/DOI/10.5281/zenodo.15155942.svg" alt="DOI">
</a>
<a href="https://discord.com/invite/kEz87zqQXh">
    <img src="https://img.shields.io/discord/1265289049783140464?label=Discord%20Members&amp;logo=discord" alt="Discord">
</a>
<a href="mailto:info@hololinked.dev">
    <img src="https://img.shields.io/badge/email-brown" alt="email">
</a>

</div>

---

## High Level Overview

Each device, or **Thing**, is modeled in software with:

- **Properties**: Validated, get-set attributes for settings, captured/computed data, or network-accessible values.

  - _Oscilloscope_: time resolution, time range, channel data
  - _Camera_: frame rate, exposure time, captured image
  - _DC Power Supply_: current voltage, voltage range, max allowed current

- **Actions**: Methods that command the hardware to perform operations.

  - _Oscilloscope_: connect/disconnect hardware
  - _Camera_: start/stop measurement or video capture
  - _DC Power Supply_: execute control routines (e.g., closed-loop control)

- **Events**: Asynchronous messages or data streams to clients (e.g., alarms, measured values).
  - _Camera_: streams images as events
  - _DC Power Supply_: raises alarms on over-current or over-voltage

This separation is independent of:

- The network protocol used for communication (HTTP, MQTT, ZMQ etc.)
- Data serialization or binary representation (JSON, MessagePack)
- Security or access control mechanisms (JWT, Basic Auth)

The `Thing` object represents the physical device and is modeled as a class, encapsulating its properties, actions, and events as its attributes & methods. Additionally, **state machines** can constrain property and action execution:

- _Oscilloscope_: Cannot start a new measurement while one is ongoing
- _Camera_: Cannot change exposure time while capturing video

---

> **Ready to get started?**  
> See the [Beginner's Guide](#beginner-guide) or [How-To](#how-to) section for code and the [Examples](#examples) section for hardware-specific implementations.
