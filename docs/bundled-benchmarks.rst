.. _bundled-benchmarks:

Bundled Benchmarks
==================

There are several benchmarks bundled with BAGEL. Additional benchmarks may be
added to the core BAGEL package through pull requests.

Transmark 60% ID
----------------

.. list-table::
   :align: left
   :stub-columns: 1

   * - Name
     - 60% ID
   * - Family
     - :ref:`Transmark <bundled-transmark>`

Metadata
++++++++

The 60% ID (60pid) benchmark implements the Transmark family API. It also
implements two stages of its own to process the results of the tool running
against it.

These are implemented as commands within the benchmark container.  That is,
there are executable programs called ``post_process`` and ``collect_results`` on
the user's ``PATH`` within the container.

.. include:: ../metadata/benchmarks/60pid.json
   :code: json

``post_process``
    This command accepts as input a chunk of output from the tool under
    benchmark (``tool_results``) in the format documented alongside the family.
    It lists no inputs because it can be assumed to accept the tool output
    format defined by the benchmark family.
``collect_results``
    This process accepts the (potentially numerous) outputs from the
    ``post_process`` command and uses them to produce a report for the user,
    which is stored in a file called ``report.tar.gz``.

