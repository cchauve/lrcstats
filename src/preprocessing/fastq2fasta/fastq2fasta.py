import sys, getopt

helpMessage = "Convert FASTQ files to FASTA format."
usageMessage = "Usage: %s [-h help and usage] [-i FASTQ file path] [-o output prefix]" % (sys.argv[0])
options = "hi:o:"

try:
	opts, args = getopt.getopt(sys.argv[1:], options)
except getopt.GetoptError:
	print "Error: unable to read command line arguments."
	sys.exit(2)

if len(sys.argv) == 1:
	print usageMessage
	sys.exit()

inputPath = None
outputPrefix = None

for opt, arg in opts:
	# Help message
	if opt == '-h':
		print helpMessage
        	print usageMessage
        	sys.exit()
	elif opt == '-i':
		inputPath = arg
	elif opt == '-o':
		outputPrefix = arg

outputPath = "%s.fasta" % (outputPrefix)

# Flag to determine if we're reading a new sample from the FASTQ file
newSample = False
sequence = ''

with open(inputPath, 'r') as inputFile:
	with open(outputPath, 'w') as outputFile:
		for line in inputFile:
			# @ denotes we are reading the sequence identifier line
			if len(line) > 0 and line[0] is '@':
				newSample = True
				header = ">%s" % (line[1:])
			# This conditional only happens immediately after the sequence identifier line
			elif newSample:
				outputFile.write(header)
				outputFile.write(line)
				newSample = False
