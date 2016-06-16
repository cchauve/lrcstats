import getopt, sys, math

def findMeanReadLength(longReadPath):
	'''
	Find the total mean length of the long reads in longReadPath
	'''
	totalLength = 0
	numReads = 0
	with open(longReadPath, 'r') as file:
		for line in file:
			if line is not '' and line[0] in 'ATGCatgc':
				totalLength = totalLength + len(line)	
				numReads = numReads + 1
	meanLength = None

	if numReads != 0:
		meanLength = totalLength/numReads
	else:
		print "ERROR: File contains no DNA sequences"
		sys.exit(2)
	
	return meanLength


def findRefLength(refPath):
	'''
	Find the length of the reference sequence.
	'''
	refLength = 0
	with open(refPath, 'r') as file:
		for line in file:
			if line is not '' and line[0] in 'ATGCatgc':
				refLength = refLength + len(line)
	return refLength

if __name__ == "__main__":
	helpMessage = "Outputs the integral number of reads necessary to achieve a required coverage given the mean length of the long reads contained in a FASTQ file and the length of reference sequence given in a FASTA file."
	usageMessage = "Usage: %s [-h help and usage] [-c coverage] [-i long reads FASTQ path] [-r reference genome path]" % (sys.argv[0])
	options = "hc:i:r:"

	try:
		opts, args = getopt.getopt(sys.argv[1:], options)
	except getopt.GetoptError:
		sys.exit(2)

	if (len(sys.argv) == 1):
                print usageMessage
                sys.exit()

        longReadPath = None
	coverage = None
	refPath = None
	verbose = True

        for opt, arg in opts:
		# Help message
                if opt == '-h':
			print helpMessage
                        print usageMessage
                        sys.exit()
		# Get required coverage
		elif opt == '-c':
			coverage = int(arg)	
		# Get long reads FASTQ path
                elif opt == '-i':
                        longReadPath = arg
		# Get reference FASTA path
                elif opt == '-r':
                        refPath = arg

	optionsIncomplete = False

        if longReadPath is None:
                print "Please provide the sample long read FASTQ path."
		optionsIncomplete = True
	if coverage is None:
		print "Please input the required coverage."
		optionsIncomplete = True
	if refPath is None:
		print "Please input the length of the reference genome."
		optionsIncomplete = True

	if optionsIncomplete:
		print usageMessage
                sys.exit(2)

	meanReadLength = findMeanReadLength(longReadPath)
	refLength = findRefLength(refPath)

	numReads = int( math.ceil( (coverage*refLength)/meanReadLength ) )

	print numReads 
