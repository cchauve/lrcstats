from __future__ import division
import os
import sys
import getopt
import re

import matplotlib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt

def findErrorRatesAndLengths(inputPath):
	'''
	Returns a matrix containing the error rates and lengths of reads.
	'''
	lengths = []
	errorRates = []
	readLengthIndex = 1 
	errorIndex = 3
	with open(inputPath, 'r') as file:
		for line in file:
			if len(line) > 0 and line[0:5] == "@Read":
				length = int( re.findall('(\d+)', line)[readLengthIndex] )		
				print length
				errors = int( re.findall('(\d+)', line)[errorIndex] )		
				errorRate = errors/length	
				lengths.append(length)
				errorRates.append(errorRate)
	return lengths, errorRates

def makeErrorRateScatterPlot(lengths, errorRates, testName, outputPath):
        '''
	Creates a scatter plot where the x-axis is length and y-axis is error rate
        '''

        fig, axes = plt.subplots()
        axes.scatter(lengths, errorRates)

        # Add labels
        axes.set_ylabel("Error Rate of Read")
        axes.set_xlabel("Length of read")
        axes.set_title("Error Rate of %s" % (testName))

        savePath = "%s/%s_error_rate_scatter.png" % (outputPath, testName) 
        fig.savefig(savePath, bbox_inches='tight')

def breezy(outputPath):
	#species = ['ecoli', 'yeast', 'fly']
	species = ['yeast']
	coverages = ['10', '20', '50', '75']
	
	for specie in species:
		for coverage in coverages:
			print "Analyzing %s coverage %s" % (specie, coverage)
			inputPath = "/global/scratch/seanla/Data/%s/simlord/long-d%s/%s-long-d%s.fastq" % (specie, coverage, specie, coverage)
			test = "%s-long-d%s" % (specie, coverage)
			lengths, errorRates = findErrorRatesAndLengths(inputPath)
			makeErrorRateScatterPlot(lengths, errorRates, test, outputPath)

helpMessage = "Create a chart visualizing the error rate distribution of simulated PacBio reads binned on length."
usageMessage = "Usage: %s [-h help and usage] [-i input file] [-o output dir] [-t test name] [-b Breezy paths]" % (sys.argv[0])
options = "hi:o:t:b"

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
testName = None
doBuiltInPaths = False

for opt, arg in opts:
	if opt == '-h':
		print helpMessage
		print usageMessage
		sys.exit()
	elif opt == '-i':
		inputPath = arg
	elif opt == '-o':
		outputPath = arg
	elif opt == '-t':
		testName = arg
	elif opt == '-b':
		doBuiltInPaths = True

optsIncomplete = False

if inputPath is None and not doBuiltInPaths:
	optsIncomplete = True
	print "Please provide an input path."
if outputPath is None:
	optsIncomplete = True
	print "Please provide an output dir."
if testName is None and not doBuiltInPaths:
	optsIncomplete = True
	print "Please provide a test name."

if optsIncomplete:
	print usageMessage
	sys.exit(2)

if doBuiltInPaths:
	breezy(outputPath)
else:	
	lengths, errorRates = findErrorRatesAndLengths(inputPath)
	makeErrorRateScatterPlot(lengths, errorRates, testName, outputPath)
