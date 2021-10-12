Terminology
===========

The terms described below are used throughout the BAGEL codebase and
documentation. They are defined here for convenience.

**Benchmark**
    A sequence dataset (real or synthetic), along with a Docker container that
    provides programs or scripts for interpreting the results of running tools
    against the dataset.
**Benchmark Container**
    A Docker container that provides programs or scripts for interpreting the
    results of running tools against the benchmark dataset.
**Benchmark Developer**
    An individual or group who develops and / or maintains a benchmark.
**Benchmark Tester**
    An individual or group who create the tool container that allows a
    particular tool to run against one or more benchmarks.
**Tool (Search Tool)**
    A computer program used for sequence search. The purpose of BAGEL is to help
    assess the performance of different tools.
**Tool Container**
    A Docker container capable of running a tool against one or more benchmarks.
    The container image must include programs or scripts for translating data
    provided in the common format used by the benchmark into the format reuqired
    by the tool, and must provide output in the format expected by the
    benchmark. This API is determined by the benchmark family the tool container
    is designed to support.
