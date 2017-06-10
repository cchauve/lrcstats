import re
import getopt
import sys
import collections # for OrderedDict

def getFastaReads(inputPath):
	with open(inputPath, 'r') as file:
		reads = collections.OrderedDict() 
		sequence = ""
		readNum = -1
		header = ""
		for line in file:
			if line[0] == '>':
				if sequence != "" and readNum != -1:
					if readNum not in reads:
						reads[readNum] = []
					reads[readNum].append( (header,sequence) )
				header = line.rstrip('\n')
				readNum = int( re.findall('(\d+)', line)[idPosition] )
				sequence = ""
			else:
				sequence += line.rstrip('\n')
		if readNum not in reads:
			reads[readNum] = []
		reads[readNum].append( (header,sequence) )
	return reads

def getSamReads(inputPath):
	with open(inputPath) as sam:
		reads = {} 
		for read in sam:
			if len(read) > 0 and read[0] != "@":
				tokens = read.split("	")
				flag = int( tokens[1] )
				if flag != 4:
					queryName = tokens[0]
					readNumber = int(re.findall('(\d+)',queryName)[idPosition])
					reads[readNumber] = read.rstrip('\n')
	return reads

def writeOutput(fastaReads,samReads,outputPrefix):
	fastaOutput = "%s.fasta" % (outputPrefix)
	samOutput = "%s.sam" % (outputPrefix)
	with open(fastaOutput,'w') as fasta, open(samOutput,'w') as sam:
		for key in samReads:
			if key in fastaReads:
				reads = fastaReads[key]
				for subread in reads:
					header = subread[0]
					sequence = subread[1]
					fasta.write(header)
					fasta.write('\n')
					fasta.write(sequence)
					fasta.write('\n')
				alignment = samReads[key]
				sam.write(alignment)
				sam.write('\n')

helpMessage = "Given cLR FASTA and ref-uLR SAM files, outputs FASTA and SAM files containing the intersection of the set of reads contained in the original FASTA and SAM files"
usageMessage = "Usage: %s [-h help and usage] [-f cLR FASTA file path] [-s sam file path] [-p read ID position] [-o output prefix]" % (sys.argv[0])
options = "hf:s:o:p:"

try:
	opts, args = getopt.getopt(sys.argv[1:], options)
except getopt.GetoptError:
	print "Error: unable to read command line arguments."
	sys.exit(2)

if len(sys.argv) == 1:
	print usageMessage
	sys.exit(2)

fastaPath = None
samPath = None
outputPrefix = None
idPosition = 0

for opt, arg in opts:
	if opt == '-h':
		print helpMessage
		print usageMessage
		sys.exit()
	elif opt == '-f':
		fastaPath = arg
	elif opt == '-s':
		samPath = arg
	elif opt == '-o':
		outputPrefix = arg
	elif opt == '-p':
		idPosition = int(arg)

if fastaPath == None or samPath == None or outputPrefix == None:
	print helpMessage
	print usageMessage
	sys.exit()

fastaReads = getFastaReads(fastaPath)
samReads = getSamReads(samPath)
writeOutput(fastaReads,samReads,outputPrefix)
