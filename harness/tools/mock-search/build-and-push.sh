#!/usr/bin/env sh

set -e

docker build -t traviswheelerlab/bagel-mock-search:1.0.0 .
docker push traviswheelerlab/bagel-mock-search:1.0.0

