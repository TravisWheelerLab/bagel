#!/usr/bin/env sh

set -e

PROFILE="${1:-docker}"
WORKDIR="${2:-work}"
DATASET="${3:-$PWD/fixtures}"

nextflow \
    -C transmark-nextflow.config \
    run transmark-workflow.nf \
    --dna_file="$DATASET/queries_dna.sto" \
    --protein_file="$DATASET/queries_protein.sto" \
    --target_file="$DATASET/targets.fa" \
    -profile "$PROFILE" \
    -work-dir "$WORKDIR"
