#!/usr/bin/env nextflow

dna_file = Channel.value( params.dna_file )
protein_file = Channel.value( params.protein_file )
target_file = Channel.value( params.target_file )

process prepare_data {
    input:
    path dna_file from dna_file
    path protein_file from protein_file
    path target_file from target_file

    output:
    path "shared.tar.gz" into shared_data
    path "spread/*.tar.gz" into spread_data

    """
    prepare_data ${dna_file} ${protein_file} ${target_file}
    """
}

process run_tool {
    input:
    path shared_file from shared_data
    path spread_file from spread_data.flatMap()

    output:
    stdout into results

    """
    run_tool ${shared_file} ${spread_file}
    """
}

results.view { "$it" }
