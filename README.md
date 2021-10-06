# PSSS Team3 Project Notes - challenging annotation


## Context

This project was one of four that collectively formed the [Petabyte-scale sequence search metagenomics benchmarking codeathon](https://datascience.nih.gov/news/petabyte-scale-sequence-search-metagenomics-benchmarking-codeathon). As the name suggests, a general motivating principle for all groups was the desire to support assessment of methods that search within massive modern sequence databases. The sibling projects were:
* [Find a long sequence in a metagenome](https://github.com/NCBI-Codeathons/bothie)
* [Contig containment](https://github.com/NCBI-Codeathons/psss-team2)
* [Elastic-BLAST](https://github.com/NCBI-Codeathons/psss-team4)

Our motivating principle is that a well-designed and standard benchmark can stoke development of new methods. It achieves this by providing clear optimization targets that are easy to test with, and that are interpretable by the community due to their consistency.


## Benchmarks for sequences that are hard to annotate

Development of sequence [annotation](https://en.wikipedia.org/wiki/DNA_annotation) methods involves  natural performance tradeoffs: methods that increase speed often do so at a cost to sensitivity. While petabyte-scale search naturally emphasizes speed above all else, our group's focus was on ensuring that tool developers and users can understand the sensitivity tradeoffs that come with methods for increasing speed. We achieve this by creating benchmarks that support evaluation of methods for annotation of difficult-to-label (meta-)genomic sequence. A benchmark includes both the actual data used in tool evaluation and supporting scripts used to perform (run) evaluation and produce summary statistics/figures. Specifically, we sought to: 
* Develop a small number of example benchmark datasets (and corresponding analysis scripts) representing situations in which accurate annotation is difficult. 
* Develop a general test harness that makes it relatively easy for benchmark users (e.g. developers of the tools being assessed) to run tests on large-scale cluster/cloud resources without needing to write code to control those resources. By developing the harness in a general way, we sought to simplify the development of future benchmarks.


## A general benchmark harness

During (and shortly after) this codeathon, we developed a pilot implementation of a harness for running benchmarks across multiple platforms (local, cluster, cloud) in a consistent and straightforward manner. This harness depends on the Nextflow scripting language; once a benchmark is created, a new tool may be tested in the benchmark's harness by creating a simple docker image that links the tool up to the harness' API.  See [harness](harness) directory for details.

## Benchmark datasets

Choices for benchmarks are endless. Given the time contraints caused by the duration of the codeathon, we settled on three benchmarks that would be (i) relatively simple to generate, (ii) probably useful for developers wishing to develop tools that annotate hard-to-label inputs, and (iii) lay the groundwork for other benchmarks. We capture each in folders within this repository (if links are not working, they will be live shortly):
* [protein domains embedded within DNA decoys](benchmarks/transmark)
* [annotating read that resist assembly](benchmarks/unassembled)
* [incomplete protein domains (abbreviated contigs)](benchmarks/subsequences)


## Inside baseball

During the codeathon, we captured some [wiki pages](https://github.com/NCBI-Codeathons/psss-team3-hard-annotation/wiki) with guidelines and tutorials. Two that may help in setting up Docker and/or cloud environments are: 
[AWS with Nextflow](wiki/AWS-with-NextFlow) and [Nextflow with Docker](wiki/Nextflow-and-Docker-guides)
