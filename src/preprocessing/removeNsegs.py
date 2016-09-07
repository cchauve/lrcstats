import getopt
import sys

helpMessage = "Given a single sequence FASTA file, remove all 'N' segments in the sequence."
usageMessage = "Usage: %s [-h help and usage] [-i input FASTA file] [-o output path]" % (sys.argv[0])
options = "hi:o:"

try:
	opts, args = getopt.getopt(sys.argv[1:], options)
except getopt.GetoptError:
	sys.exit(1)

if len(sys.argv) == 1:
	print usageMessage
	sys.exit(1)

inputPath = None
outputPath = None

for opt, arg in opts:
	if opt == '-h':
		print helpMessage
		print usageMessage
		sys.exit()
	elif opt == '-i':
		inputPath = arg
	elif opt == '-o':
		outputPath = arg

optsIncomplete = False

if inputPath is None:
	print("Please provide an input FASTA file.")
	optsIncomplete = True
if outputPath is None:
	print("Please provide an output path.")
	optsIncomplete = True

if optsIncomplete:
	print(usageMessage)
	sys.exit(1)

header = None
oldSequence = ""

with open(inputPath,'r') as file:
	for line in file:
		if len(line) > 0 and line[0] == ">":
			header = line
		else:
			oldSequence += line.rstrip()

newSequence = oldSequence.replace("N","")

with open(outputPath,'w') as file:
	file.write(header)
	sequence = "%s\n" % (newSequence)
	file.write(sequence)
