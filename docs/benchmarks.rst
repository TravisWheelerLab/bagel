.. _benchmarks:

Benchmarks
==========

BAGEL can be useful to anyone developing a benchmark, or who would like to
evaluate search tools against a particular extant benchmark. The componenets and
APIs required to make a benchmark work with BAGEL are described below. There are
also a number of :ref:`benchmarks <bundled-benchmarks>` bundled with BAGEL.

Benchmark Families
------------------

BAGEL benchmarks are divided into "families" based on the data they provide and
the output they expect to receive back from tools. Therefore, each family has a
slightly different API that must be implemented by the benchmark developer,
although they all follow the same :ref:`basic pattern <overview>`.

The API required by a particular benchmark family is described by a metadata
document associated with the family.  A benchmark that claims to belong to a
particular family must support this API (BAGEL allows benchmark developers to
validate this automatically).

The metadata schema for a benchmark family is described below, along with
example values for the `Transmark <bundled-transmark>` benchmark family.

.. include:: ../metadata/families/transmark.json
   :code: json

**name**
    The name of the family. This should be suggestive of its API, if possible,
    but it is ultimately arbitrary.
**version**
    The API version. This allows the API to evolve over time. Benchmarks and
    tools pin themselves to a particular API version. The version should not
    change often.
**benchmark_data**
    A benchmark that implements this family must provide a piece of data that
    corresponds to each item in this list. Note that the metadata doesn't place
    any direct restrictions on the shape or kind of the data (such as the file
    format), so these must be documented.
**tool_results**
    The results expected from a tool that is compatible with this family. Each
    tool must produce a result for each element in the list. Again, this doesn't
    place any direct restrictions on the format of the results, which must be
    documented.

.. NOTE::
   The data and results file formats are not included in the metadata and must
   be documented alongside the benchmark family. For example, the Transmark
   family expects that ``queries_dna`` and ``queries_protein`` will be Stockholm
   files that contain multiple sequence alignments (MSAs).

Benchmark Architecture
----------------------

Every benchmark consists of two components:

1. A metadata document
2. A Docker container image

Each of these is described in detail below.

Metadata
++++++++

The metadata document describes where to find the data associated with the
benchmark and the Docker container necessary to process the output of tools run
against the benchmark. It also declares compatibility with a particular
benchmark family (see above).

An example is shown below, and each field is explained afterward.

.. include:: ../metadata/benchmarks/60pid.json
   :code: json

**family**
    The benchmark family that the benchmark complies with, see above for more
    information on benchmark families.
**family_version**
    The version of the family implemented by this benchmark.
**name**
    The name of this particular benchmark. This should be descriptive and
    emphasize what makes this particular benchmark unique within its family.
**version**
    The benchmark version is used when reporting results so that it is possible
    to determine whether two sets of results are comparable.
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
    container.

Container
+++++++++

The benchmark container provides facilities for collecting the results from a
tool container and producing any relevant analysis, figures, and reports the
benchmark developer wishes to provide to benchmark users.
