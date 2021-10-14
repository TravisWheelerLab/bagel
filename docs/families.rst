.. _families:

Families
========

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

.. literalinclude:: ../metadata/families/transmark.json
   :language: json

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
