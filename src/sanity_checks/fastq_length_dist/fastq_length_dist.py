import getopt
import sys
import numpy as np

import matplotlib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt

def makeLengthHistogram(lengths, savePath, datasetName):
	'''
	Creates a length histogram given a list of lengths.
	
	Inputs:
	- (list of ints) lengths: lengths of the reads
	- (string) path: path to the output file
	- (string) name: name of the dataset
	'''
	fig, axes = plt.subplots()
	bins = np.linspace(0, 60000, 50)

	# Create the actual histograms.
	axes.hist(lengths, bins, alpha=0.5, label='Reads')

	axes.legend(loc='upper right')

	# Add labels
	axes.set_ylabel("Number of reads")
	axes.set_xlabel("Length of read")
	axes.set_title("Histogram of lengths of reads")

	fig.suptitle( "%s" % (datasetName) )

	fig.savefig(savePath, bbox_inches='tight')

def findLengths(inputPath):
	'''
	Given a FASTQ file, returns a list of all the reads.

	Inputs:
	- (string) inputPath: the absolute path to the FASTQ file
	
	Returns:
	(list of ints) lengths: a list of the lengths of the reads
	'''

	with open(inputPath, 'r') as file:
		lengths = []
		lineNumber = 0
		for line in file:
			if lineNumber % 4 == 1:
				seq = line
				length = len(seq)
				lengths.append(length)
			lineNumber += 1
	return lengths

helpMessage = "Create a length histogram given a FASTQ file."
usageMessage = "Usage: %s [-h help and usage] [-i FASTQ input path] [-o output path] [-n dataset name]" % (sys.argv[0])
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
outputPath = None
datasetName = None 

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
		datasetName = arg

optsIncomplete = False

if inputPath is None:
	optsIncomplete = True
	print("Please provide the path to the FASTQ file.")
if outputPath is None:
	optsIncomplete = True
	print("Please provide the path to the output file.")
if datasetName is None:
	optsIncomplete = True
	print("Please indicate the name of the dataset.")

if optsIncomplete:
	print usageMessage
	sys.exit(2)
print("Finding lengths...")
lengths = findLengths(inputPath)

print("Creating length histogram...")
makeLengthHistogram(lengths, outputPath, datasetName) 
