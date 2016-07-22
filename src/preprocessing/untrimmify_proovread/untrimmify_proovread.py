import sys, getopt, re

def getCorrectedReads(cReadPath):
	'''
	Collect the corrected reads from the proovread FASTA file.
	Input
	- (string) cReadPath: specifies the path to the proovread corrected reads FASTA file
	Returns
	- (dict) reads: given the read number, find its trimmed sequence(s) and slice(s)
	'''
	with open(cReadPath, 'r') as file:
		reads = {}
		for line in file:
			# ">" means we're reading the header line of a read
			if line[0] == ">":
				# The fastaReadNumberIndex_g'th group of integers in the header line is the read number
				
				number = int( re.findall('(\d+)', line)[fastaReadNumberIndex_g] )	

				# If the number of space-separated elements in the header is more than
				# two, we done goofed.
				line = line.split()
				assert len(line) == 2

				# Find the perl style substring slice 
				substr = line[1]
				substr = re.findall('(\d+)', substr)
				start = int(substr[0])
				length = int(substr[1])
				slice = (start, length)
			else:
				sequence = line.rstrip() 
				# Add the read to the dictionary; if it already exists, then append the
				# trimmed read sequence and slice to the list
				if number in reads:
					reads[number][trimmed_g].append(sequence)
					reads[number][slices_g].append(slice)
				else:
					sequences = [ sequence ]
					slices = [ slice ]
					reads[number] = { trimmed_g : sequences, slices_g : slices } 
	return reads

def getUncorrectedReads(uReadPath, reads):
	'''
	Collect the uncorrected reads from the SimLoRD FASTQ file.
	Input
	- (string) uReadPath: specifies the path to the SimLoRD uncorrected reads FASTQ file
	- (dict) reads: given the read number, find its trimmed sequence(s) and slice(s)
	Returns
	- (dict) reads: given the read number, find its trimmed sequence(s), uncorrected sequence and slice(s)
	'''
	# Keeps track of which line we are at
	i = 0
	with open(uReadPath, 'r') as file:
		for line in file:
			# If the line number is a multiple of 4, then we are reading the header line
			if i % 4 == 0:
				# The fastaReadNumberIndex_g'th group of integers in the header line is the read number
				number = int( re.findall('(\d+)', line)[fastaReadNumberIndex_g] )	
			# Otherwise, the line after the header line is the sequence line
			elif i % 4 == 1:
				sequence = line.rstrip()
				# To save space, only add the uncorrected sequence if the read
				# exists in the dict
				if number in reads:
					reads[number][uncorrected_g] = sequence
			i += 1
	return reads

def fillTrimmedGaps(read):
	'''
	Fill the gaps of the trimmed reads using slice information and the uncorrected sequence.
	Input
	- (dict) read: returns its trimmed sequence(s), uncorrected sequence and slice(s)
	Returns
	- (string) untrimmedSequence: the untrimmed sequence
	'''
	slices = read[slices_g]

	try:
		uncorrectedRead = read[uncorrected_g]
	except:
		raise

	trimmedReads = read[trimmed_g]

	start = 0
	uncorrectedSegmentSlices = []	

	# Find the slice info for the trimmed off, uncorrected segments from the uLR 
	for i in range( len(slices) + 1 ):
		if i != len(slices):
			slice = slices[i]
			stop = slice[0]
			index = (start, stop)
			start = stop + slice[1]
		else:
			index = (start, len(uncorrectedRead) )
		uncorrectedSegmentSlices.append( index )

	numberOfSlices = len(uncorrectedSegmentSlices)
	numberOfTrimmedReads = len(trimmedReads)
	assert numberOfSlices == numberOfTrimmedReads + 1

	untrimmedSequence = ""
	# Fill the gaps of the trimmed sequences with the uncorrected segments
	for i in range( numberOfSlices ):
		slice = uncorrectedSegmentSlices[i]
		start = slice[0]
		stop = slice[1]
		uncorrectedSegment = uncorrectedRead[start:stop].lower()
		if i != numberOfTrimmedReads:
			trimmedRead = trimmedReads[i]
			untrimmedSequence += uncorrectedSegment + trimmedRead
		else:
			untrimmedSequence += uncorrectedSegment

	return untrimmedSequence

def makeUntrimmed(reads):
	'''
	Using the substring information provided by the proovread files and the uncorrected reads,
	fill in the gaps of the trimmed corrected reads to make them untrimmed.
	Input
	- (dict) reads: given the read number, find its trimmed sequence(s), uncorrected sequence and slice(s)
	Returns
	- (dict) untrimmedReads: given the read number, find the untrimmed sequence
	'''
	untrimmedReads = {}
	for number in reads:
		read = reads[number]
		try:
			untrimmedSequence = fillTrimmedGaps(read)
		except:
			print "Error: no uncorrected sequence available."
			print "Read number is %d" % (number)
		untrimmedReads[number] = untrimmedSequence
	return untrimmedReads

def writeUntrimmedFile(reads, outputPath):
	'''
	Write the new untrimmed reads into a FASTA file.
	Input
	- (dict) reads: given the read number, returns the untrimmed sequence
	- (string) outputPath: Specifies the path to the FASTA file
	Returns
	- None
	'''
	with open(outputPath, 'w') as file:
		for number in reads:
			sequence = reads[number]
			header = ">%s\n" % (number)
			file.write(header)
			sequence = "%s\n" % (sequence)	
			file.write(sequence)

def writeTestFasta(reads, slices, path):
	'''
	Generate a test FASTA file given the reads at path.
	'''
	assert len(slices) == len(reads)
	with open(path,'w') as file:
		for i in range( len(reads) ):
			slice = slices[i]
			header = ">1.%d SUBSTR:%d,%d\n" % (i, slice[0], slice[1])
			file.write(header)
			seq = reads[i]
			sequence = "%s\n" % (seq)
			file.write(sequence)

def writeTestFastq(read, path):
	'''
	Generate a test FASTQ file given the read at path.
	'''
	with open(path,'w') as file:
		identifier = "@read1\n"
		file.write(identifier)
		readLine = "%s\n" % (read)
		file.write(readLine)
		file.write("+\n")
		quality = ""
		for i in range( len(read) ):
			quality += "~"
		quality += "\n"
		file.write(quality)
			
def test():
	'''
	Generate test files and test the program.
	'''
	uncorrectedRead = "CGCTTAGGTACGCTAGTATGCGTTCTTCCTTCCAGAGGTATGT"
	actualUntrimmedRead = "cgcttAGGTAcgctaGTATGcgttcttcctTCCAGAGGTAtgt"
	trimmedReads = [ "AGGTA", "GTATG", "TCCAGAGGTA" ]
	perlSlices = [ (5,5), (15,5), (30,10) ]
	cReadPath = "test.fasta"
	uReadPath = "test.fastq"

	# Write the test files
	writeTestFasta(trimmedReads, perlSlices, cReadPath)
	writeTestFastq(uncorrectedRead, uReadPath)

	# Collect the corrected reads from the proovread FASTA file
	reads = getCorrectedReads(cReadPath)

	# Collect the original uncorrected reads from the SimLoRD FASTQ file
	reads = getUncorrectedReads(uReadPath, reads)

	# Convert trimmed reads into untrimmed reads
	reads = makeUntrimmed(reads)

	for number in reads:
		untrimmedRead = reads[number]

	if untrimmedRead == actualUntrimmedRead:
		print "Test passed."
	else:
		print "Test failed."
		print "Actual: %s" % (actualUntrimmedRead)
		print "Found:  %s" % (untrimmedRead)

helpMessage = "Convert proovread trimmed reads into untrimmed reads."
usageMessage = "[-h help and usage] [-c corrected reads path] [-u uncorrected reads path] [-o output path] [-p simulator used was PBSim]"

options = "hc:u:o:t"

try:
	opts, args = getopt.getopt(sys.argv[1:], options)
except getopt.GetoptError:
	print "Error: unable to read command line arguments."
	sys.exit(2)

if len(sys.argv) == 1:
	print usageMessage
	sys.exit()

cReadPath = None
uReadPath = None
outputPath = None
usedPbsim = False
doTest = False

for opt, arg in opts:
	if opt == '-h':
		print helpMessage
		print usageMessage
		sys.exit()
	elif opt == '-c':
		cReadPath = arg
	elif opt == '-u':
		uReadPath = arg
	elif opt == '-o':
		outputPath = arg
	elif opt == '-p':
		usedPbsim = True
	elif opt == '-t':
		doTest = True

# Global variable to indicate which group of integers in the FASTA header files
# indicates the read number
if not usedPbsim:
	fastaReadNumberIndex_g = 0 
else:
	fastaReadNumberIndex_g = 1	


# Global variables to index the read dictionary
trimmed_g = "TRIMMED SEQUENCES"
slices_g = "SLICES" 
uncorrected_g = "UNCORRECTED SEQUENCE"

if doTest:
	test()
	sys.exit()

# Collect the corrected reads from the proovread FASTA file
reads = getCorrectedReads(cReadPath)

# Collect the original uncorrected reads from the SimLoRD FASTQ file
reads = getUncorrectedReads(uReadPath, reads)

# Convert trimmed reads into untrimmed reads
reads = makeUntrimmed(reads)

# Write the FASTA file
writeUntrimmedFile(reads, outputPath)
