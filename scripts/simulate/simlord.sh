#!/bin/bash

# output directory
outputDir=
# reads4coverage script included in the LRCstats repository
reads4coverage=
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

mkdir -p $outputDir
# find the required number of reads for the desired depth of coverage and average read length of the empirical PacBio
# long reads FASTQ file
reads=$(python $reads4coverage -c $cov -i $fastq -r $ref)
# simulate long reads
$simlord -n $reads -sf $fastq -rr $ref $outputPrefix
# Construct MAF alignment file from SimLoRD-outputted SAM file
sam=${outputPrefix}.fastq.sam
maf=${sam}
python $sam2maf -r $ref -s $sam -o $maf
