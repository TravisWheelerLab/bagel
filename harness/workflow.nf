#!/usr/bin/env nextflow

needle = Channel.value( params.needle )

# This would normally be a queue channel
haystack = Channel.value( params.haystack )

process run_tool {
    input:
    path needle from needle
    path haystack from haystack

    output:
    stdout into results

    """
    psss-benchmark ${needle} ${haystack}
    """
}

results.view { "results: $it" }

