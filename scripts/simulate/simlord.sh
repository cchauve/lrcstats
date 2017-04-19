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
sam2maf=${lrcstats}/src/preprocessing/sam2maf/sam2maf.py

mkdir -p ${outputDir}
# find the required number of reads for the desired depth of coverage and average read length of the empirical PacBio
# long reads FASTQ file
reads=$(python ${reads4coverage} -c ${cov} -i ${fastq} -r ${ref})
# simulate long reads
${simlord} -n ${reads} -sf ${fastq} -rr ${ref} ${outputPrefix}
# Construct MAF alignment file from SimLoRD-outputted SAM file
sam=${outputPrefix}.fastq.sam
maf=${sam}
python ${sam2maf} -r ${ref} -s ${sam} -o ${maf}
