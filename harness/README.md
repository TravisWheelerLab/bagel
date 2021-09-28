# Benchmark Harness

A person wishing to benchmark a particular search tool creates a Docker image
that encapsulates the tool itself and abides by a particular "API". The
container is then run and provided with data in a standard format. It provides
its results in a standard output format which are then collected.

## Container API

The container must have an executable in the user's `PATH` called
`psss-benchmark`. The executable must accept two parameters, a sequence to
search for, and a collection of sequences to search.

For example, the command below must "work":

```
psss-benchmark needle.txt haystack.txt
```

## Runner API

A runner is just something that knows how to run a benchmark container
(described above) with appropriate input and collect the output. Our initial
runner will be implemented as a Nextflow workflow, but there is no reason that
there couldn't be others. For very simple cases, even a shell script would
suffice.

The default runner, a Nextflow script, is defined in `workflow.nf`.

## Example

There is a pretend search tool called `mock-search` with a container defined as
a basic example.

There is also trivial sample data (compatible with the mock tool) in the `data/`
directory.

You can run the Mock Search example using Docker like this:

```
nextflow run -params-file params.yaml -profile docker workflow.nf
```

## TODO

  * Decide on data formats for the inputs
  * Handle data references (like s3 URIs) cleanly
  * Make Mock Search output the right format
  * Add container images for a couple tools

