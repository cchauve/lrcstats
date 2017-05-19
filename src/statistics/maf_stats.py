from __future__ import division
import sys
import getopt

def getAlignments(mafPath):
	reference = ""
	read = ""
	alignments = []
	with open(mafPath,'r') as maf:
		for line in maf:
			tokens = line.split()
			if len(tokens) > 0 and tokens[0] == 's':
				if tokens[1] == 'ref':
					reference = tokens[5]
				else:
					read = tokens[5]
					size = tokens[3]
					alignment = (reference,read,size)
					alignments.append(alignment)
	return alignments
								
def findNumberOfBases(alignments):
	numBases = 0
	for alignment in alignments:
		read = alignments[1]
		numBases += len(read)
	return numBases

def findTotalIdentity(alignments):
	totalIdentity = 0
	for alignment in alignments:
		reference = alignments[0]		
		read = alignments[1]
		for i in range(len(read)):
			refBase = reference[i]
			readBase = read[i]
			if refBase == readBase:
				totalIdentity += 1
	return totalIdentity

def findGain(ulrs,clrs):
	numCorr = findNumberOfBases(clrs)
	numUncorr = findNumberOfBases(ulrs)
	corrIdentity = findTotalIdentity(clrs)
	uncorrIdentity = findTotalIdentity(ulrs)
	corrError = numCorr - corrIdentity
	uncorrError = numUncorr - uncorrIdentity
	uncorrErrorRate = uncorrError / numUncorr
	corrErrorRate = corrError / numCorr
	gain = abs( uncorrErrorRate - corrErrorRate )/uncorrErrorRate
	return gain

def findAccuracy(alignments):
	identity = findTotalIdentity(alignments)
	numBases = findNumberOfBases(alignments)
	return identity/numBases

helpMessage = ""
usageMessage = "[-h help and usage] [-e <name of experiment> [-c <cLR MAF] [-u uLR MAF] [-o <output prefix>]" 

options = "hc:u:o:e:"

try:
	opts, args = getopt.getopt(sys.argv[1:],options)
except getopt.GetoptError:
	print("Error: unable to read command line arguments.")
	sys.exit(1)

if len(sys.argv) == 1:
	print(usageMessage)
	sys.exit()

refPath = None
clrPath = None
ulrPath = None
outputPrefix = None
experimentName = None

for opt, arg in opts:
	if opt == '-h':
		print(helpMessage)
		print(usageMessage)
		sys.exit()
	elif opt == '-c':
		clrPath = arg
	elif opt == '-u':
		ulrPath = arg
	elif opt == '-o':
		outputPrefix = arg
	elif opt == '-e':
		experimentName = arg	

if ulrPath == None or clrPath == None or outputPath == None or experimentName == None:
	print(helpMessage)
	print(usageMessage)
	sys.exit(1)

outputPath = "%s.tsv" % (outputPrefix)

clrs = getAlignments(clrPath)
ulrs = getAlignments(ulrPath)

gain = findGain(ulrs,clrs)
clrAccuracy = findAccuracy(clrs)
ulrAccuracy = findAccuracy(ulrs)

with open(outputPath,'w') as output:
	output.write( "Statistics for mapping-based evaluation for experiment %s\n" % (experimentName) )
	output.write( "uLR Accuracy	cLR Accuracy	Gain\n" )
	output.write( "%f	%f	%f" % (ulrAccuracy,clrAccuracy,gain) ) 
