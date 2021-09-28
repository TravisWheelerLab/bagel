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
psss-benchmark needle.fa haystack.fa
```

## Workflow

There is a generic Nextflow script, defined in `workflow.nf` that can run these
Docker images.

## Example

There is a pretend search tool called `mock-search` with a container defined as
a basic example.

There is also trivial sample data (compatible with the mock tool) in the `data/`
directory.

## TODO

  * Decide on data formats for the inputs
  * Handle data references (like s3 URIs) cleanly
  * Make Mock Search output the right format

