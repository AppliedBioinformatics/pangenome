#!/usr/bin/env python2 
 
# Modules need: 'Bio', 'sys'
# Written by: Philipp Bayer
# Email: philipp.bayer@uwa.edu.au
# Last modification date: 19/02/2018
 
import sys
from Bio import SeqIO
 
out_paired_1 = sys.argv[1] + "_R1.fastq"
out_paired_2 = sys.argv[1] + "_R2.fastq"
out_unpaired = sys.argv[1] + "_unpaired.fastq"
 
out_paired_1 = open(out_paired_1, "w")
out_paired_2 = open(out_paired_2, "w")
out_unpaired = open(out_unpaired, "w")
 
read_dict = {} # { key: read name, value: {"R1":SeqRecord, "R2":SeqRecord} }
 
for l in SeqIO.parse(sys.argv[1], "fastq"):
    short = l.id.replace('/1','').replace('/2','')
    if short not in read_dict:
        read_dict[short] = {"R1":False, "R2":False}
 
    if "/1" in l.id:
        read_dict[short]["R1"] = l
    else:
        read_dict[short]["R2"] = l
 
    # do we have a proper pair?
    if read_dict[short]["R2"] and read_dict[short]["R1"]:
        out_paired_1.write(read_dict[short]["R1"].format("fastq"))
        out_paired_2.write(read_dict[short]["R2"].format("fastq"))
        # we will never see this again, save some memory
        del read_dict[short]
 
# now write out the remaining singles
for r in read_dict:
    r1 = read_dict[r]["R1"]
    r2 = read_dict[r]["R2"]
    if r1:
        out_unpaired.write(r1.format("fastq"))
    if r2:
        out_unpaired.write(r2.format("fastq"))
 
