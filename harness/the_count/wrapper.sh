#!/usr/bin/env sh

set -e

if [ $# != 2 ]
then
  echo "usage: wrapper.sh <needle.fa> <haystack.fa>"
  exit
fi

OUTPUT="test.fa"

the_count "$2" "$1" $OUTPUT

# do something with the $OUTPUT file to convert
# it to do correct format for downstream analysis

