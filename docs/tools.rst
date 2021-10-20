.. _tools:

Tools
=====

BAGEL is useful to anyone who would like to evaluate the performance of a
particular search tools, or compare a collection of search tools against one
another.

A tool requires two pieces that should be relatively straightforward to create.
These are described below. The only thing required to run a tool against a
benchmark is the metadata, since the Docker image will be fetched from its
registry.

Metadata
--------

A metadata document must be provided to give the runner some information about
the tool, such as which benchmarks it is intended to work with. The metadata
file must be provided in JSON format. It consists of a single "object" with the
keys described below.

An example metadata file might look like this:

.. literalinclude:: ../tools/mock-search/metadata.json
   :language: json

**name**
    The name of the tool in question. This needn't have any relation to the name
    of the executable, it should be whatever people will recognize most easily.

**version**
    The version of the tool encapsulated by the container image. This should
    reflect whatever versioning scheme the tool's authors use. For example,
    something like ``1.5.0``.

**benchmarks**
    An array of benchmark families that the tool is intended to be run against.
    For example, ``["transmark"]``.

.. NOTE::
   We will eventually incorporate the benchmark family version into the tool
   metadata.

**image**
    A string containing the full path to the Docker image associated with the
    tool (described above), hosted on a public container registry such as
    `Docker Hub <https://dockerhub.com>`_ (which will be assumed by default).

**results**
    A mapping of result names, as defined by the families the tool supports, to
    filenames that will be produced by the tool's last stage.

**stages**
    Computational stages that are required to run the tool. See :ref:`stages`
    for details. The last stage listed here must produce the results described
    above.

Docker Image
------------

A `Docker <https://docker.com>`_ image that is compatible with the container API
for the benchmark family the tool is intended to run against.
