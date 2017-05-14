import sys
import getopt
import re
from operator import itemgetter

def getReads(inputPath):
	'''
	Inputs
	- string inputPath: specifies the path to the input FASTA file
	Returns
	- list of tuples reads: first element in tuple is int read number,
				second element is string DNA sequence
	'''
	with open(inputPath, 'r') as file:
		reads = []
		sequence = ""
		readNum = -1
		header = ""
		for line in file:
			if line[0] == '>':
				if sequence != "":
					reads.append( (readNum, sequence, header) )
				header = line
				readNum = int( re.findall('(\d+)', line)[readNumberIndex] )
				sequence = ""
			else:
				sequence += line.rstrip('\n')
		reads.append( (readNum, sequence, header) )
	return reads

def writeFasta(outputPath, reads):
	'''
	Inputs
	- string outputPath: specifies the write path to the output
			     FASTA file
	- list of tuples reads: first element in tuple is int read number,
				second element is string DNA sequence
	Returns
	- None
	'''
	with open(outputPath, 'w') as file:
		for read in reads:
			header = "%s" % (read[2])
			file.write(header)	
			sequence = "%s\n" % (read[1])
			file.write(sequence)
				 

helpMessage = "Sort FASTA files based on read number."
usageMessage = "[-h help] [-i input FASTA file] [-o output prefix]"

options = "hn:i:o:"

try:
	opts, args = getopt.getopt(sys.argv[1:], options)
except getopt.GetoptError:
	print "Error: unable to read command line arguments."
	sys.exit(2)

if len(sys.argv) == 1:
	print usageMessage
	sys.exit()

inputPath = None
outputPath = None
readNumberIndex = 1

for opt, arg in opts:
	if opt == '-h':
		print helpMessage
		print usageMessage
		sys.exit()
	elif opt == '-i':
		inputPath = arg
	elif opt == '-o':
		outputPath = arg
	elif opt == '-n':
		readNumberIndex = int(arg)

optsIncomplete = False

if inputPath is None:
	print "Please provide the path to the input FASTA file."
	optsIncomplete = True
if outputPath is None:
	print "Please provide the path to the output FASTA file."
	optsIncomplete = True

if optsIncomplete:
	print usageMessage
	sys.exit(2)

reads = getReads(inputPath)
# Sort reads based on read number
reads = sorted(reads, key=itemgetter(0))
writeFasta(outputPath, reads)
