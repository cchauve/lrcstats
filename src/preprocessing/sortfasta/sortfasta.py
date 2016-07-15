import sys, getopt
from operator import itemgetter

def getReads(inputPath):
	with open(inputPath, 'r') as file:
		reads = []
		sequence = ""
		readNum = -1
		for line in file:
			if line[0] == '>':
				if sequence != "":
					reads.append( (readNum, sequence) )
				line = line.split('_')
				readNum = int(line[1])
			else:
				sequence += line.rstrip('\n')
	return reads

def writeFasta(outputPrefix, reads):
	outputPath = "%s.fasta" % (outputPrefix)
	with open(outputPath, 'w') as file:
		for read in reads:
			header = ">%d\n" % (read[0])
			file.write(header)	
			sequence = "%s\n" % (read[1])
			file.write(sequence)
				 

helpMessage = "Sort FASTA files based on read number."
usageMessage = "[-h help] [-i input FASTA file] [-o output prefix]"

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
	if opt == '-h':
		print helpMessage
		print usageMessage
		sys.exit()
	elif opt == '-i':
		inputPath = arg
	elif opt == '-o':
		outputPrefix = arg

if inputPath is None and outputPrefix is None:
	print usageMessage


reads = getReads(inputPath)
reads = sorted(reads, key=itemgetter(0))
writeFasta(outputPrefix, reads)
