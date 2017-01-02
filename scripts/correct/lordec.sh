#!/bin/bash

# path to LoRDEC executable
lordec=
# output directory for LoRDEC
outputDir=
# paths to paired end short reads files
short1=
short2=
# path to uncorrected long reads file
long=
# output file path
output=
# number of threads
threads=
# max number of trials
trials=
# solid kmer abundance threshold
solid=
# kmer size
kmer=
# maximum error rate
errorRate=
# maximum number of branches to explore
branch=
# number of paths to try from a k-mer
trials=

set -e
mkdir -p ${outputDir}

cd ${outputDir}
${lordec} -T ${threads} --trials ${trials} --branch ${branch} --errorrate ${errorRate} -2 ${short1} ${short2} -k ${kmer} -s ${solid} -i ${long} -o ${output} 
