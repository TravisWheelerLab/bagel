# BAGEL

**B**enchmarking the **A**nnotation of **G**enomic **EL**ements

BAGEL (Benchmarking the Annotation of Genomic ELements) is a benchmark harness
produced during the PSSS codeathon in late September, 2021. The harness consists
of a “runner” application that manages the task of running one or more
competitor tools against underlying benchmark data and accumulates results in a
post-processing analysis stage.

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


## Development

The runner is implemented as a Python project. We use Pipenv to manage
dependencies. To install dependencies in a new virtual environment, run `pipenv
sync --dev`. If you change the dependencies in `Pipfile`, run
`./tool/update-deps.sh` to update the necessary lock files. Other common tasks
are described below:

  * Check types: `./tool/check-types.sh`
  * Format code: `./tool/run-format.sh`
  * Run linter: `./tool/check-lints.sh`
  * Run tests: `./tool/check-tests.sh`
  * Update documentation: `./tool/update-docs.sh`

Please run the scripts above before submitting a pull request.

## TODO

  * Handle data references (like s3 URIs) cleanly
  * Fan out to multiple tools with Nextflow
  * Implement collect_results step
  * Find a way to embed or access NF scripts from Python
  * Since we're a real Python package, support YAML, maybe TOML
