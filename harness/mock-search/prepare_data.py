#!/usr/bin/env python3

from sys import argv
from os import mkdir
from subprocess import run

DNA_PATH=argv[1]
PROTEIN_PATH=argv[2]
TARGET_PATH=argv[3]

mkdir('spread')

# Convert each MSA to a single FASTA file
# that will be run as a single job.
with open(DNA_PATH, 'r') as dna_file:
    pairs = []
    for index, line in enumerate(dna_file.readlines()):
        line = line.strip()
        if line.startswith('#') or len(line) == 0:
            continue
        pairs.append([line[0], line[1]])
        if line == '//':
            with open('query.fa', 'w') as spread_file:
                for name, seq in pairs:
                    spread_file.write(f'>{name}\n')
                    spread_file.write(f'{seq}')
            run(['tar', 'czf', f'spread/{index}.tar.gz', 'query.fa'])
            run(['rm', f'query.fa'])
            pairs.clear()
        else:
            pairs.append(line.split())

# We don't need to manipulate the target
# input data so just bundle it up.
run(['tar', 'czf', 'shared.tar.gz', TARGET_PATH], capture_output=True)
