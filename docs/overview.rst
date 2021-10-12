Overview
========

BAGEL is a framework that makes it easier to run DNA / RNA and protein search
tools against multiple benchmarks and compare results easily.

A person who wishes to benchmark a particular search tool creates a Docker image
that encapsulates the tool itself and abides by a particular "API". This API is
defined by a benchmark family (essentially, a standard for benchmarks that
provide similar data and generate similar results). The container can then run
against any benchmark in that family.

When run, the container is provided with data in a family-determined input
format and it provides its results in a family-determined output format. The
results are then collected and processed by a container provided alongside the
benchmark dataset and a human-consumable report is produced.

.. image:: _static/overview-diagram.png
