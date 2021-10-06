#!/usr/bin/env sh

set -e

SHARED_PATH="$1"
SPREAD_PATH="$2"

tar xf "$SHARED_PATH"
tar xf "$SPREAD_PATH"

sleep 10
tool.py shared.fa query.fa
