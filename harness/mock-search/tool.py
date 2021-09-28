#!/usr/bin/env python3

from sys import argv

# Usage: ./tool.py <haystack> <needle>

with open(argv[1], 'r') as haystack_file:
    haystack = haystack_file.read().strip()

with open(argv[2], 'r') as needle_file:
    needle = needle_file.read().strip()

last_index = 0
while True:
    try:
        last_index = haystack.index(needle, last_index + 1)
        print(last_index)
    except ValueError:
        break

