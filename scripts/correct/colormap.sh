#!/bin/bash

# CoLoRMap executable
colormap=
# uncorrected long reads file
long=
# merged short reads file
short=
# output directory
outputDir=
# output prefix
outputPrefix=
# number of threads to use
threads=

mkdir -p ${outputDir}
${colormap} ${long} ${short} ${outputDir} ${outputPrefix} ${threads}
