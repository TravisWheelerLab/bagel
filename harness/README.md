# Benchmark Harness

This document provides an introduction to the benchmark harness produced during the PSSS codeathon. The harness is intended to consist of a 'runner' script that manages the task of running one or more competitor tools against underlying benchmark data and accumulates results in a post-processing analysis stage. This runner utilizes Nextflow to optionally manage fan-out of computation to available cluster/cloud resources, though alternative workflow systems may be enabled in the future. 

The current form of the harness is a pilot project completed during (and shortly after) the PSSS codeathon; future effort will lead to improved functionality, generalization, and documentation. For now, interested readers may be aided by this [architecture document](harness_architecture_draft.pdf).  As the project is in active development, current documentation of specific usage and API are fairly light. If you're thinking of using this framework and the existing documentation isn't sufficient for your needs, file a github issue to get further guidance. 



A person wishing to benchmark a particular search tool creates a Docker image
that encapsulates the tool itself and abides by a particular "API". The
container is then run and provided with data in a generic input format. It
provides its results in a generic output format which are then collected.




## Container API

Each benchmark dataset has a slightly different API based on its purpose and the
goals of the tools that ought to run against it.

### Transmark

The container must have an executable in the user's `PATH` called
`prepare_data`. This executable must have three parameters, a set of MSAs in
Stockholm format for DNA and protein (two files) to search for, and a collection
of sequences to search within, in FASTA format.

For example, the command below must "work":

```
prepare_data queries_dna.sto queries_protein.sto targets.fa
```

The executable must output two outputs. One, a file called `shared.tar.gz`
should contain files that need to be provided to every job when the work is
fanned out. This might include an index or a trained model. The other is a
directory of `tar.gz` files, each representing a piece of the overall
computation, split up any way the author sees fit.

The container must also have an executable in the user's `PATH` called
`run_tool`. This executable must have two parameters. The first is a `tar.gz`
file containing the shared files provided by the `prepare_data` program
described above. The second is a `tar.gz` file containing a single "spread" file
produced by `prepare_data`.

This executable must output tab-delimited rows (zero or more) in the following
order:

  * E-value
  * score
  * hit start
  * hit stop
  * target name
  * query name

## Runner API

A runner is just something that knows how to run a benchmark container
(described above) with appropriate input and collect the output. Our initial
runner will be implemented as a Nextflow workflow, but there is no reason that
there couldn't be others. For very simple cases, even a shell script would
suffice.

The default runner, a Nextflow script, is defined in `transmark-workflow.nf`.

## Example

There is a pretend search tool called `mock-search` with a container defined as
a basic example.

There is also trivial sample data (compatible with the mock tool) in the
`fixtures/` directory.

You can run the Mock Search example using Docker like this:

```
./transmark-run.sh
```

This script also takes parameters that allow it to be run in other environments.

## TODO

  * Handle data references (like s3 URIs) cleanly
