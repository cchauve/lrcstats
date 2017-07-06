#!/usr/bin/env python
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
				if 'ref' in tokens[1]:
					read = tokens[6]
				else:
					reference = tokens[6]
					alignment = (reference,read)
					alignments.append(alignment)
	return alignments
								
def findNumberOfBases(alignments):
	numBases = 0
	for alignment in alignments:
		read = alignment[1]
		in_corr_seg = False
		for i in range( len(read) ):
			if read[i].isupper():
				in_corr_seg = True
			elif read[i].islower():
				in_corr_seg = False
			if in_corr_seg:
				numBases += 1	 
	return numBases

def findTotalIdentity(alignments):
	totalIdentity = 0
	for alignment in alignments:
		reference = alignment[0]		
		read = alignment[1]
		for i in range(len(read)):
			refBase = reference[i]
			readBase = read[i]
			if refBase == readBase:
				totalIdentity += 1
	return totalIdentity

def findAccuracy(alignments):
	identity = findTotalIdentity(alignments)
	numBases = findNumberOfBases(alignments)
	return identity/numBases

helpMessage = ""
usageMessage = "[-h help and usage] [-e <name of experiment>] [-c <cLR MAF>] [-o <output prefix>]" 

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

if clrPath == None or outputPrefix == None or experimentName == None:
	print(helpMessage)
	print(usageMessage)
	sys.exit(1)

outputPath = "%s.tsv" % (outputPrefix)

clrs = getAlignments(clrPath)
clrAccuracy = findAccuracy(clrs)
'''
ulrs = getAlignments(ulrPath)
ulrAccuracy = findAccuracy(ulrs)
gain = findGain(ulrs,clrs)
'''

with open(outputPath,'w') as output:
	output.write( "Statistics for mapping-based evaluation for experiment %s\n" % (experimentName) )
	output.write( "cLR Accuracy\n" )
	output.write( "%f\n" % (clrAccuracy) ) 
