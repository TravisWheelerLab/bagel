#!/usr/bin/env sh

set -e

# TODO: write usage instructions

PROFILE="${1:-gscc}"
WORKDIR="${2:-work}"
QUEUE="${3:-nextflow-queue}"
CONTAINER="${4:-traviswheelerlab/psss-harness:latest}"
DATASET="${5:-$PWD/fixtures/transmark}"

nextflow \
    -C transmark-nextflow.config \
    run transmark-workflow.nf \
    --dna_file="$DATASET/queries_dna.sto" \
    --protein_file="$DATASET/queries_protein.sto" \
    --target_file="$DATASET/targets.fa" \
    -process.queue="$QUEUE" \
    -process.container="$CONTAINER" \
    -profile "$PROFILE" \
    -work-dir "$WORKDIR"
