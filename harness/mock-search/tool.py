#!/usr/bin/env python3

from sys import argv

# Usage: ./tool.py <haystacks> <needles>

def load(file):
    pairs = []
    while True:
        try:
            name = next(file).strip()[1:]
            seq = next(file).strip()
            pairs.append((name, seq))
        except StopIteration:
            break
    return pairs


def find(haystack, needle):
    last_index = 0
    while True:
        try:
            last_index = haystack.index(needle, last_index + 1)
            yield last_index
        except ValueError:
            break


with open(argv[1], 'r') as haystack_file:
    haystacks = load(haystack_file)

with open(argv[2], 'r') as needle_file:
    needles = load(needle_file)


if __name__ == '__main__':
    for (nn, ns) in needles:
        for (hn, hs) in haystacks:
            for index in find(hs, ns):
                print(f'{nn}\t{hn}\t{index}\t{len(ns)}')

