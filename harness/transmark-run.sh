#!/usr/bin/env sh

set -e

PROFILE="${1:-docker}"
WORKDIR="${2:-work}"
QUEUE="${3:-nextflow-queue}"
CONTAINER="${4:-traviswheelerlab/psss-harness}"
DATASET="${5:-$PWD/fixtures}"

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
