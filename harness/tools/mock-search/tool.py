#!/usr/bin/env python3

from sys import argv


# Usage: ./tool.py <targets> <queries>


def load(file):
    pairs = []

    name = ''
    seq = ''

    for line in file:
        line = line.strip()

        if line == '':
            continue

        if line[0] == '>':
            if name:
                pairs.append((name, seq))
            name = line[1:]
            seq = ''
        else:
            seq += line
        
    if seq:
        pairs.append((name, seq))

    return pairs


def find(haystack, needle):
    size = 5
    for index in range(len(haystack) - size):
        if needle[0:size] == haystack[index:index + size]:
            yield index


if __name__ == '__main__':
    with open(argv[1], 'r') as haystack_file:
        haystacks = load(haystack_file)

    with open(argv[2], 'r') as needle_file:
        needles = load(needle_file)
    
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
