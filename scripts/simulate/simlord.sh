#!/bin/bash

# path to lrcstats repo directory
lrcstats=
# output directory
outputDir=
# desired depth of coverage for simulated long reads
cov=
# empirical PacBio long reads FASTQ file for sample length distribution
fastq=
# reference genome
ref=
# SimLoRD executable
simlord=
# Output prefix for SimLoRD
outputPrefix=

reads4coverage=${lrcstats}/src/preprocessing/reads4coveragy.py

mkdir -p ${outputDir}
# find the required number of reads for the desired depth of coverage and average read length of the empirical PacBio
# long reads FASTQ file
reads=$(python ${reads4coverage} -c ${cov} -i ${fastq} -r ${ref})
# simulate long reads
${simlord} -n ${reads} -sf ${fastq} -rr ${ref} ${outputPrefix}
