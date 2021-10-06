#!/usr/bin/env sh

set -e

# Update dependencies. Run this whenever a dependency changes.

pipenv lock
pipenv sync
pip freeze --exclude bagel > requirements.txt
