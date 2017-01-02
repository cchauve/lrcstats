#!/bin/bash

# path to proovread executable
proovread=
# path to paired end short reads files
short1=
short2=
# path to uncorrected long reads file
long=
# output path
output=
# number of threads
threads=

${proovread} -t ${threads} --lr-qv-offset 70 -s ${short1} -s ${short2} -l ${long} -p ${output}
