# Benchmark Harness

This document provides an introduction to the benchmark harness produced during
the PSSS codeathon. The harness is intended to consist of a 'runner' script that
manages the task of running one or more competitor tools against underlying
benchmark data and accumulates results in a post-processing analysis stage. This
runner utilizes Nextflow to optionally manage fan-out of computation to
available cluster/cloud resources, though alternative workflow systems may be
enabled in the future. 

The current form of the harness is a pilot project completed during (and shortly
after) the PSSS codeathon; future effort will lead to improved functionality,
generalization, and documentation. For now, interested readers may be aided by
this [architecture document](harness_architecture_draft.pdf).  As the project is
in active development, current documentation of specific usage and API are
fairly light. If you're thinking of using this framework and the existing
documentation isn't sufficient for your needs, file a github issue to get
further guidance. 

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

## Adding a Tool

Adding a tool requires two pieces that should be relatively straightforward to
create. These are described below. The only thing required to run a benchmark is
the metadata, since the Docker image will be fetched from its registry.

### Docker Image

A [Docker](http://docker.com) image that is compatible with the container API
for the benchmark the tool is intended to run against (see
[Container APIs](#Container-APIs) above for a description of the API for
each benchmark).

### Metadata File

Finally, a metadata file must be provided to give the runner some information
about the tool, such as which benchmarks it is intended to work with. The
metadata file must be provided in JSON format. It consists of a single "object"
with the keys described below.

**name:** the name of the tool in question. This needn't have any relation to
*the name of the executable, it should be whatever people will recognize most
*easily.

**version:** the version of the tool encapsulated by the container image. This
*should reflect whatever versioning scheme the tool's authors use. For example,
something like `1.5.0`.

**benchmarks:** an array of benchmark names that the tool is intended to be run
*against. For example, `["transmark"]`.

**image-location:** a string containing the full path to the Docker image
associated with the tool (described above), hosted on a public container
registry such as [Docker Hub](http://dockerhub.com) (which will be assumed by
default).

An example metadata file might look like this:

```json
{
    "name": "mock-search",
    "version": "1.0.0",
    "benchmarks": ["transmark"],
    "image": "traviswheelerlab/bagel-mock-search:1.0.0"
}
```

## Adding a Benchmark

TODO: Flesh this out in a big way...

```json
{
  "family": "transmark",
  "name": "60% ID",
  "version": "1.0.0",
  "files": {
    "queries_dna.sto": "https://osf.io/...",
    "queries_protein.sto": "https://osf.io/...",
    "targets.fa": "https://osf.io/..."
  }
}
```

## TODO

  * Handle data references (like s3 URIs) cleanly
  * Fan out to multiple tools with Nextflow
  * Implement collect_results step
  * Find a way to embed or access NF scripts from Python
