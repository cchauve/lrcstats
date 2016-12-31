#!/bin/bash

# path to jabba executable
jabba=
# path to de Bruijn graph file outputted by Brownie
dbGraph=
# length of MEM
mem=
# kmer size
kmer=
# output directory for Jabba
outputDir=
# path to uncorrected long reads file
long=
# number of threads
threads=

# correct long reads using Jabba
${jabba} -t ${threads} -l ${mem} -k ${kmer} -o ${outputDir} -g ${dbGraph} -fastq ${long}
