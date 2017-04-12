#!/bin/bash

# path to karect executable
karect=
# output directory
outputDir=
# path to paired end short reads files
short1=
short2=
# number of threads
threads=

set -e
mkdir -p ${outputDir}
# correct short reads
${karect} -correct -inputfile=${short1} -inputfile=${short2} -resultdir=${outputDir} -tempdir=${outputDir} -celltype=haploid -matchtype=hamming -threads=${threads}
