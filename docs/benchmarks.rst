.. _benchmarks:

Benchmarks
==========

BAGEL can be useful to anyone developing a benchmark, or who would like to
evaluate search tools against a particular extant benchmark. The componenets and
APIs required to make a benchmark work with BAGEL are described below. There are
also a number of :ref:`benchmarks <bundled-benchmarks>` bundled with BAGEL.

Every benchmark consists of two components:

1. A metadata document
2. A Docker container image

Each of these is described in detail below.

Metadata
--------

The metadata document describes where to find the data associated with the
benchmark and the Docker container necessary to process the output of tools run
against the benchmark. It also declares compatibility with a particular
benchmark family (see above).

An example is shown below, and each field is explained afterward.

.. literalinclude:: ../metadata/benchmarks/60pid.json
   :language: json

**name**
    The name of this particular benchmark. This should be descriptive and
    emphasize what makes this particular benchmark unique within its family.

**version**
    The benchmark version is used when reporting results so that it is possible
    to determine whether two sets of results are comparable.

**family**
    The benchmark family that the benchmark complies with, see above for more
    information on benchmark families.

**family_version**
    The version of the family implemented by this benchmark.

**image**
    A reference to the Docker image that implements the benchmark family API
    and provides any stages declared for this particular benchmark. By default,
    the image is assumed to exist in `Docker Hub <https://dockerhub.com>`_, but
    if a full path is provided, any public container registry is fine.

**data**
    Where to find the data associated with the benchmark. This object must
    implement the API described by the benchmark family. The URLs provided here
    must be publicly accessible.

**stages**
    Post-processing stages that will run after the tool has finished in order to
    process the results into a useful report. These can be arbitrary, but they
    must be declared in the benchmark metadata. Each stage must be implemented
    as an executable command on the user's ``PATH`` within the benchmark
    container. See :ref:`stages` for more information.

.. NOTE::
   The files passed to the first stage of a benchmark container will be in the
   format documented by the benchmark family for the ``tool_result``.

Docker Image
------------

The benchmark container provides facilities for collecting the results from a
tool container and producing any relevant analysis, figures, and reports the
benchmark developer wishes to provide to benchmark users.
