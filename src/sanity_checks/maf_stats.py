from __future__ import division
import getopt
import sys
import numpy as np

import matplotlib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt

def getAlignedBases(read):
	'''
	Given a read alignment, returns the number of non-'-' chars. 
	'''
	bases = 0
	for char in read:
		if char != "-":
			bases += 1
	return bases

def getIdentity(ref, read):
	'''
	Given a reference and read alignment, returns the number of identical bases
	between the two.
	'''
	assert len(ref) == len(read)
	length = len(ref)

	totalIdentity = 0

	for i in range(length):
		if ref[i] == read[i]:
			totalIdentity += 1
	return totalIdentity			

def makeLengthIdentityScatterPlot(accuracyRates, lengths, datasetName, outputPrefix):
        '''
	Creates a scatter plot where the x-axis is length and y-axis is the identity of th read
        '''

        fig, axes = plt.subplots()
        axes.scatter(lengths, accuracyRates)

        # Add labels
        axes.set_ylabel("Identity of Read")
        axes.set_xlabel("Length of Read")
        axes.set_title("Length vs Identity of Dataset %s" % (datasetName))

        savePath = "%s_length_identity_scatter.png" % (outputPrefix) 
        fig.savefig(savePath, bbox_inches='tight')

helpMessage = "Output a file with statistics about MAF file."
usageMessage = "Usage: %s [-h help and usage] [-i MAF input prefix] [-o output prefix] [-n dataset name]" % (sys.argv[0])
options = "hi:o:n:"

try:
	opts, args = getopt.getopt(sys.argv[1:], options)
except getopt.GetoptError:
	print "Error: unable to read command line arguments."
	sys.exit(2)

if len(sys.argv) == 1:
	print usageMessage
	sys.exit(2)

inputPath = None 
outputPrefix = None
datasetName = None 

for opt, arg in opts:
	if opt == '-h':
		print helpMessage
		print usageMessage
		sys.exit()
	elif opt == '-i':
		inputPath = arg

optsIncomplete = False

if inputPath is None:
	optsIncomplete = True
	print("Please provide the path to the MAF file.")

if optsIncomplete:
	print usageMessage
	sys.exit(2)

alignedReads = 0
totalLength = 0
totalIdentity = 0

accuracyRates = []
lengths = []

ref = None
read = None

with open(inputPath,'r') as input:
	for line in input:
		if len(line.rstrip()) > 0:
			line = line.split()
			if line[0] == "a":
				ref = None
				read = None
			elif line[0] == "s" and line[1] == "ref":
				ref = line[6]
			else:
				read = line[6]

				alignedReads += 1	

				totalLength += len(read)

				length = getAlignedBases(read)
				totalAlignedBases += length
				lengths.append(length)

				identity = getIdentity(ref, read)
				totalIdentity += identity
				accuracyRate = identity/length
				accuracyRates.append(accuracyRate)

#makeLengthIdentityScatterPlot(accuracyRates, lengths, datasetName, outputPrefix) 

errorRate = (totalIdentity-totalLength)/totalLength
print( "Error Rate = %d\n" % (errorRate) )
