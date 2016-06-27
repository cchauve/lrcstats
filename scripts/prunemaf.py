import sys, getopt, re

if __name__ == "__main__":
	helpMessage = "Outputs MAF file such that it contains only the corrected long reads (cLR) reads present in the inputted FASTA file."
	usageMessage = "Usage: %s [-h help and usage] [-f cLR FASTA file path] [-m maf file path] [-o output prefix] [-p Pbsim reads]" % (sys.argv[0])
	options = "hf:m:o:p"

	try:
		opts, args = getopt.getopt(sys.argv[1:], options)
	except getopt.GetoptError:
		print "Error: unable to read command line arguments."
		sys.exit(2)

	if len(sys.argv) == 1:
                print usageMessage
                sys.exit(2)

	fastaPath = None
	mafPath = None
	outputPrefix = None
	isPbsim = False

        for opt, arg in opts:
		# Help message
                if opt == '-h':
			print helpMessage
                        print usageMessage
                        sys.exit()
                elif opt == '-f':
                        fastaPath = arg
                elif opt == '-m':
                        mafPath = arg
		elif opt == '-o':
			outputPrefix = arg
		elif opt == '-p':
			isPbsim = True

	optsIncomplete = False

	if fastaPath is None:
		print "Please provide the path for the FASTA file."
		optsIncomplete = True
	if mafPath is None:
		print "Please provide the path for the MAF file."
		optsIncomplete = True
	if outputPrefix is None:
		print "Please provide the output path prefix."
		optsIncomplete = True	
	if optsIncomplete:
		print usage
		sys.exit(2)

	outputPath = "%s.maf" % (outputPrefix)

	reads = []
	
	if isPbsim:
		readNumberIndex = 1
	else:
		readNumberIndex = 0

	with open(fastaPath, 'r') as fasta:
		with open(mafPath, 'r') as maf:
			with open(outputPath, 'w') as output:
				for line in fasta:
					if line is not '' and line[0] is '>':
						# Find the read number from the FASTA header line
						reads.append( int( re.findall('(\d+)', line)[readNumberIndex] ) )
				for line in maf:
					tokens = line.rstrip().split()

					# Store the reference line
					if len( tokens ) > 1 and tokens[1] == 'ref':
						ref = line
					elif len( tokens ) > 1:
						readNumber = int( re.findall('(\d+)', tokens[1])[readNumberIndex] )
						# If the current read has been corrected by the program
						# then keep it
						if readNumber in reads:
							output.write('a\n')
							output.write(ref)
							output.write(line) 
							output.write('\n')




















