#!/usr/bin/env nextflow

needle = Channel.value( params.needle )
haystack = Channel.fromPath( params.haystack )

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

