import sys, getopt, re

def getReads(inputPath):
	'''
	Input
	- (string) inputPath: specifies the path to the Jabba or Proovread long reads
	Returns
	- dict of reads: (read number) are the keys, string (sequence) outputs
	'''
	reads = {}
	# Find the read numbers and corresponding sequences
	with open(inputPath, 'r') as inputFile:
		for line in inputFile:
			if line != '' and line[0] == '>':
				number = int( re.findall('(\d+)', line)[readNumberIndex] )		
			else:
				sequence = line.rstrip()
				if number in reads:
					reads[number] += " " + sequence
				else:
					reads[number] = sequence
	return reads

def writeFile(reads, outputPath):
	'''
	Inputs
	- ( list of tuples of int and string ) reads: list of read numbers and sequences to
							be written into file
	- (string) outputPath: specifies where to write processed reads 
	Outputs
	- None
	'''
	with open(outputPath, 'w') as outputFile:
		for number in reads:
			sequence = reads[number]
			header = ">%d\n" % (number)
			outputFile.write(header)
			sequence = "%s\n" % (sequence) 
			outputFile.write(sequence)

helpMessage = "Process Jabba or Proovread FASTA long reads files so that trimmed portions of the same read are concatenated (but separated by spaces) into one single sequence."
usageMessage = "Usage: %s [-h help and usage] [-i Jabba or Proovread input path] [-o output path] [-p PBSim data]" % (sys.argv[0])
options = "hi:o:p"

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
isPbsim = False	

for opt, arg in opts:
	# Help message
	if opt == '-h':
		print helpMessage
		print usageMessage
		sys.exit()
	elif opt == '-i':
		inputPath = arg
	elif opt == '-o':
		outputPath = arg
	elif opt == '-p':
		isPbsim = True	

optsIncomplete = False

if inputPath is None or inputPath is '':
	print "Please provide the input path."
	optsIncomplete = True
if outputPath is None or outputPath is '':
	print "Please provide an output path."
	optsIncomplete = True
if optsIncomplete:
	print usageMessage
	sys.exit(2)

# the second group of integers in PBSim reads is the read number
if isPbsim:
	readNumberIndex = 1
# The first group of integers in SimLoRD reads is the read number
else:
	readNumberIndex = 0

reads = getReads(inputPath)
writeFile(reads, outputPath)
