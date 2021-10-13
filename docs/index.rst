.. BAGEL documentation master file, created by
   sphinx-quickstart on Thu Oct  7 08:15:30 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. image:: _static/bagel-logo.png
   :height: 36pt
   :align: left

BAGEL Documentation
===================

.. If you create a new page, add its name to the list below!

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   overview
   terminology
   benchmarks
   tools
   bundled-benchmarks
   bundled-families
   modules



BAGEL (Benchmarking the Annotation of Genomic ELements) is a benchmark harness
produced during the PSSS codeathon in late September, 2021. The harness consists
of a "runner" script that manages the task of running one or more competitor
tools against underlying benchmark data and accumulates results in a
post-processing analysis stage.

The default runner utilizes Nextflow to optionally manage fan-out of computation
to available cluster/cloud resources, though alternative workflow systems may be
enabled in the future. 

The current form of the harness is a pilot project completed during (and shortly
after) the PSSS codeathon; future effort will lead to improved functionality,
generalization, and documentation. For now, interested readers may be aided by
the `architecture presentation <_static/harness_architecture_draft.pdf>`_ (note
that the presentation focuses on the Transmark benchmark).

As the project is in active development, current documentation of specific usage
and API are fairly light. If you're thinking of using this framework and the
existing documentation isn't sufficient for your needs, file a `GitHub issue
<https://github.com/TravisWheelerLab/bagel/issues>`_ to get further guidance. 



Index and Search
----------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
