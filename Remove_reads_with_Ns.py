#! /usr/bin/env python

from argparse import ArgumentParser
import sys
from Bio import SeqIO
from itertools import izip

N_COUNT_CUTOFF = 1

parser = ArgumentParser(description='Removes reads with N in their sequence. Creates two new files ending in "Ns_removed". Writes removal statistics to STDOUT at the end.')
parser.add_argument('R1', help='Path to R1 file')
parser.add_argument('R2', help='Path to R2 file')
parser.add_argument('--cutoff', default=N_COUNT_CUTOFF, help='Minimum count of Ns that lead to removal of read. Default: %s'%N_COUNT_CUTOFF)

args = parser.parse_args()

removed_pairs = 0
kept_pairs = 0

r1_out = open(args.R1 + '_Ns_removed', 'w')
r2_out = open(args.R2 + '_Ns_removed', 'w')

for read_a, read_b in izip(SeqIO.parse(args.R1, 'fastq'), SeqIO.parse(args.R2, 'fastq')):
    if str(read_a.seq).upper().count('N') >= args.cutoff:
        removed_pairs += 1
        continue
    elif str(read_b.seq).upper().count('N') >= args.cutoff:
        removed_pairs += 1
        continue
    r1_out.write(read_a.format('fastq'))
    r2_out.write(read_b.format('fastq'))
    kept_pairs += 1

sys.stderr.write('Removed %s pairs and kept %s pairs.\n'%(removed_pairs, kept_pairs))
