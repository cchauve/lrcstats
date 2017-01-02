#!/bin/bash

# path to brownie executable
brownie=
# paths to karect-corrected paired end short reads files
short1=
short2=
# output directory for brownie
outputDir=
# kmer length
kmer=

# construct de Bruijn graph out of short reads
${brownie} graphCorrection -k ${kmer} -p ${outputDir} ${short1} ${short2}
