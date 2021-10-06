#!/usr/bin/env sh

set -e

pkg_version=$(python bagel/_version.py)

docker build \
  -t traviswheelerlab/bagel:${pkg_version} \
  .
