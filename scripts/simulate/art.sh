#!/bin/bash

# path of the fq2fastq.py script included in the LRCstats repository
fq2fastq=
# path to the merge files script included in the LRCstats repository
mergeFiles=
# output directory
outputDir=
# reference genome
ref=
# depth of coverage for short reads
cov=
# length of short reads to be simulated
len=
# mean size of DNA fragments for paired end reads
mean=
# standard deviation of fragment size for paired end reads
stdev=
# output prefix
outputPrefix=

mkdir -p $outputDir
$art -p -i $ref -l 100 -f $cov -m 300 -s 25 -o $outputPrefix

# change extension of ART short reads from .fq to .fastq to allow for compatibility with correction algorithms
python $fq2fastq -i $outputDir

short1=${outputPrefix}1.fastq
short2=${outputPrefix}2.fastq

# merge both paired end short read files into one 
shortMerged=${outputPrefix}-merged.fastq
$mergeFiles shuffle -1 $short1 -2 $short2 -o $shortMerged
