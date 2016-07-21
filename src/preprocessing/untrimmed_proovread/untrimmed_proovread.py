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
				if number in cReads:
					reads[number][sequence_k].append(sequence)
					reads[number][slice_k].append(slice)
				else:
					sequences = [ sequence ]
					slices = [ slice ]
					reads[number] = { sequence_k : sequences, slice_k : slices } 
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
	with open(uReadPath, 'r') as file:
		for line in file:
			# "@" indicates we're reading the header line of a read
			if line[0] == "@":
				# The fastaReadNumberIndex_g'th group of integers in the header line is the read number
				number = int( re.findall('(\d+)', line)[fastaReadNumberIndex_g] )	
				justReadHeader = True	
			# The sequence line follows right after the header line in FASTQ files
			elif justReadHeader:
				sequence = line.rstrip()
				# To save space, only add the uncorrected sequence if the read
				# exists in the dict
				if number in reads:
					reads[number][uncorrected_k] = sequence
				justReadHeader = False
	return reads

def makeUntrimmed(reads)
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
		untrimmedSequence = fillTrimmedGaps(read)
		untrimmedReads[number] = untrimmedSequence
	return untrimmedReads

def writeUntrimmedFile(reads, outputPath):
	'''
	Write the new untrimmed reads into a FASTA file.
	Input
	- (dict) reads: given the read number, return the untrimmed sequence
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
			

helpMessage = "Convert proovread trimmed reads into untrimmed reads."
usageMessage = "[-h help and usage] [-c corrected reads path] [-u uncorrected reads path] [-o output path] [-p simulator used was PBSim]"

options = "hc:u:o:"

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

# Global variable to indicate which group of integers in the FASTA header files
# indicates the read number
if usedPbsim:
	fastaReadNumberIndex_g = 1 
else:
	fastaReadNumberIndex_g = 0	

# Global variables to index cRead dictionaries
trimmed_g = "TRIMMED SEQUENCES"
slices_g = "SLICES" 
uncorrected_g = "UNCORRECTED SEQUENCE"

# Collect the corrected reads from the proovread FASTA file
reads = getCorrectedReads(cReadPath)

# Collect the original uncorrected reads from the SimLoRD FASTQ file
reads = getUncorrectedReads(uReadPath, reads)

# Convert trimmed reads into untrimmed reads
cReads = makeUntrimmed(reads)

# Write the FASTA file
writeUntrimmedFile(cReads, outputPath)
