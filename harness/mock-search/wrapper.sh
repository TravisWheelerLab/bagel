#!/usr/bin/env sh

set -e

# Our tool accepts its arguments in the wrong order, so we have a wrapper script
# that swaps them. This script could also add flags, convert data formats, etc.
tool.py "$2" "$1"

