#!/usr/bin/env python3

from sys import argv
from subprocess import run


# Usage: ./tool.py <targets> <queries>


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


if __name__ == '__main__':

    with open('query.fa', 'r') as needle_file:
        needles = load(needle_file)

    with open('shared.fa', 'r') as haystack_file:
        haystacks = load(haystack_file)

    for (nn, ns) in needles:
        for (hn, hs) in haystacks:
            for index in find(hs, ns):
                e_value = 1.0
                score = 2.0
                start = index
                stop = index + len(ns) - 1
                target = hn
                query = nn
                print(f'{e_value}\t{score}\t{start}\t{stop}\t{target}\t{query}')
