.. _bundled-families:

Bundled Families
================

The benchmark families described below are bundled with BAGEL. While it is
certainly possible for users to define their own families, using the bundled
families, when possible, means that new benchmarks can be compared against older
ones more easily. It also reuse of existing tool containers.

.. _bundled-transmark:

Transmark
---------

The Transmark family is the initial family implemented in BAGEL. Its API is
described here. Note that a benchmark needn't come from the Transmark tool to be
considered part of the Transmark family, it just needs to share the same API.

.. literalinclude:: ../metadata/families/transmark.json
   :language: json

Input and output formats are described below.

.. list-table::
   :align: left
   :stub-columns: 1

   * - ``queries_dna``
     - Stockholm format (``*.sto``) containing DNA MSAs
   * - ``queries_protein``
     - Stockholm format (``*.sto``) containing protein MSAs
   * - ``targets``
     - FASTA format (``*.fa``) containing target sequences

The output format (``matches``) is tab-separated values (TSV) with the following
columns:

* E-value
* score
* hit start
* hit stop
* target name
* query name
