inputFileName = '/global/scratch/seanla/Data/ecoli/longd5/ecoli-d5_0001.fastq'
outputFileName = '/global/scratch/seanla/Data/ecoli/longd5/ecoli-d5_0001-100reads.fastq'

numReads = 100
numLines = 4*numReads

with open(inputFileName,'r') as inputFile:
	lines = [next(inputFile) for x in xrange(numLines)]

with open(outputFileName,'w') as outputFile:
	for line in lines:
		outputFile.write(line)
