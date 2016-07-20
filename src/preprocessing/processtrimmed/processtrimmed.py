import sys, getopt, re

helpMessage = "Process proovread files such that trimmed portions of the same read are concatenated (but separated by spaces) into one single sequence."
usageMessage = "Usage: %s [-h help and usage] [-i proovread input path] [-o output path] [-p PBSim data]" % (sys.argv[0])
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
	print "Please provide the input proovread path."
	optsIncomplete = True
if outputPath is None or outputPath is '':
	print "Please provide an output path."
	optsIncomplete = True
if optsIncomplete:
	print usageMessage
	sys.exit(2)

if isPbsim:
	readNumberIndex = 1
else:
	readNumberIndex = 0

with open(inputPath, 'r') as inputFile:
	with open(outputPath, 'w') as outputFile:
		lastRead = 0 
		sequence = ''
		for line in inputFile:
			if line is not '' and line[0] is '>':
				# Find the read number from the FASTA header line
				currentRead = int( re.findall('(\d+)', line)[readNumberIndex] )		
				if currentRead != lastRead:
					# If we are at a new read, write the sequence into file
					if sequence is not '':
						outputFile.write(sequence)
						outputFile.write('\n')

					header = '>%s\n' % (currentRead)
					outputFile.write(header)
					lastRead = currentRead
					sequence = ''
			else:
				if sequence is '':
					sequence = line.rstrip()
				else:
					sequence = sequence + " " + line.rstrip()
		# Write the last sequence into file
		outputFile.write(sequence)
		outputFile.write('\n')
