import sys, getopt

if __name__ == "__main__":
	helpMessage = "Process FASTA files such that sequences for each sample are contained in one line."
	usageMessage = "Usage: %s [-h help and usage] [-i long reads FASTA inputPath] [-o output path]" % (sys.argv[0])
	options = "hi:o:"

	try:
		opts, args = getopt.getopt(sys.argv[1:], options)
	except getopt.GetoptError:
		print "Error: unable to read command line arguments."
		sys.exit(2)

	if (len(sys.argv) == 1):
                print usageMessage
                sys.exit()

	inputPath = None
	outputPath = None

        for opt, arg in opts:
		# Help message
                if opt == '-h':
			print helpMessage
                        print usageMessage
                        sys.exit()
		# Get long reads FASTA inputPath
                elif opt == '-i':
                        inputPath = arg
		elif opt == '-o':
			outputPath = arg

	optsIncomplete = False

        if inputPath is None or inputPath is '':
                print "Please provide the sample long read FASTQ inputPath."
		optsIncomplete = True
	if outputPath is None or outputPath is '':
		print "Please provide an output path."
		optsIncomplete = True
	if optsIncomplete:
		print usageMessage
		sys.exit(2)

	with open(inputPath, 'r') as inputFile:
		with open(outputPath, 'w') as outputFile:
			sequence = ''
			for line in inputFile:
				if line is not '' and line[0] is '>':
					if sequence is not '':
						outputFile.write(sequence)
						outputFile.write('\n')
					outputFile.write(line)
					sequence = ''
				else:
					line = line.rstrip('\n')
					sequence = sequence + line
