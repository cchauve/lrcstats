from __future__ import division
import sys, os, getopt
import numpy as np
import matplotlib as mpl
# agg backend is used to create plot as a .png file
mpl.use('agg')
import matplotlib.pyplot as plt
from random import randint
from math import ceil

class ReadDatum(object):
	'''
	Preprocesses and outputs general statistics for reads.
	'''
	def __init__(self, data):
		'''
		Accepts as input list of trimmed read data points obtained
		directly from the STATS file outputted by lrcstats
		'''
		data = [int(data[i]) for i in range(len(data)) if i != 0]
		self.cLength = data[0]
		self.uLength = data[1]

		self.cDel = data[2]
		self.uDel = data[3]
		self.cIns = data[4]
		self.uIns = data[5]
		self.cSub = data[6]
		self.uSub = data[7]

	def getCorrLength(self):
		'''
		Returns the length of the corrected long read.
		'''
		return self.cLength

	def getCorrErrorRate(self):
		'''
		Returns the error rate of the corrected trimmed long read,
		which is defined as the number of mutations divided by
		the length of the read.
		'''
		return (self.cDel + self.cIns + self.cSub)/self.cLength

	def getUncorrLength(self):
		'''
		Returns the length of the corresponding uncorrected long read.
		'''
		return self.uLength

	def getUncorrErrorRate(self):
		'''
		Returns the error rate of the corresponding long read,
		which is defined as the number of mutations divided by
		the length of the read.
		'''
		try:
			return (self.uDel + self.uIns + self.uSub)/self.uLength
		except:
			print "uLength is 0"
			sys.exit(2)

	def getUncorrErrors(self):
		'''
		Returns the number of erroreneous bases in the uncorrected
		long read.
		'''
		return self.uDel + self.uIns + self.uSub

class TrimmedDatum(ReadDatum):
	'''
	Similar to ReadDatum object, but also outputs statistics related
	specifically for trimmed reads.
	'''
	def __init__(self,data):
		'''
		Accepts as input list of trimmed read data points obtained
		directly from the STATS file outputted by lrcstats
		'''
		ReadDatum.__init__(self,data)

	def getDelProportion(self):
		'''
		Returns the proportion between the number of deletions
		in corrected reads.	
		'''
		return self.cDel/self.uDel

	def getInsProportion(self):
		'''
		Returns the proportion between the number of insertions
		in corrected trimmed reads.	
		'''
		return self.cIns/self.uIns

	def getSubProportion(self):
		'''
		Returns the proportion between the number of substitutions
		in corrected trimmed reads.	
		'''
		return self.cSub/self.uSub


class UntrimmedDatum(ReadDatum):
	'''
	Similar to ReadDatum object, but also outputs statistics related
	specifically for trimmed reads.
	'''
	def __init__(self, data):
		'''
		Accepts as input list of untrimmed read data points obtained
		directly from the STATS file outputted by lrcstats
		'''
		ReadDatum.__init__(self, data)
		data = [int(data[i]) for i in range(len(data)) if i != 0]

		self.correctedTruePos = data[8]
		self.correctedFalsePos = data[9]
		self.uncorrectedTruePos = data[10]
		self.uncorrectedFalsePos = data[11]

	def getCorrTruePositives(self):
		'''
		Corrected true positives are defined as bases that
		have been corrected and are equivalent to its respective
		base in the referene alignment (not reference sequence)
		'''
		return self.correctedTruePos

	def getCorrFalsePositives(self):
		'''
		Corrected false positives are defined as bases that
		have been corrected and are NOT equivalent to its
		respective base in the reference alignment (not reference
		sequence)
		'''
		return self.uncorrectedTruePos

	def getCorrSegmentErrorRate(self):
		'''
		Returns the error rate over only those segments
		in the corrected long read which have been
		corrected. 
		'''
		return (self.correctedFalsePos)/(self.correctedTruePos + self.correctedFalsePos)
	
	# These methods apply to the uncorrected segments of corrected long reads

	def getUncorrTruePositives(self):
		'''
		Uncorrected true positives are defined as bases
		that have NOT been corrected and are equivalent
		to its respective base in the reference alignment.
		'''
		return self.uncorrectedTruePos

	def getUncorrFalsePositives(self):
		'''
		Uncorrected false positives are defined as bases that
		have NOT been corrected and are NOT equivalent to its
		respective base in the reference alignment.
		'''
		return self.uncorrectedFalsePos

	def getUncorrSegmentErrorRate(self):
		'''
		Returns the error rate over only those segments of
		the corrected long read which have not been
		corrected.
		'''
		return (self.uncorrectedFalsePos)/(self.uncorrectedTruePos + self.uncorrectedFalsePos)

def retrieveRawData(dataPath):
	'''
	Accepts the path to the STATS file outputted by lrcstats.
	Returns two lists of UntrimmedDatum and ReadDatum objects,
	respectively.
	'''
	rawData = []
	with open(dataPath, 'r') as file:
		for line in file:
			rawData.append(line)

	TrimmedData = []
	UntrimmedData = []

	for datum in rawData:
		datum = datum.split()

		if datum[0] == 'u':
			datum = UntrimmedDatum(datum)
			UntrimmedData.append(datum)
		elif datum[0] == 't':
			datum = ReadDatum(datum)
			TrimmedData.append(datum)

	return (TrimmedData, UntrimmedData)

def makeErrorRateBoxPlot(data, testPrefix):
	'''
	Creates an error rate frequency box plot and saves on disk.

	Accepts a list of either ReadDatum or UntrimmedDatum objects and
	a prefix designating the name of file and save location.
	Returns nothing.
	'''
	corrErrorRates = []
	uncorrErrorRates = []

	# Collect the data from the stats list
	for datum in data:
		corrErrorRate = datum.getCorrErrorRate()
		corrErrorRates.append(corrErrorRate)
		uncorrErrorRate = datum.getUncorrErrorRate()
		uncorrErrorRates.append(uncorrErrorRate)

	data = [corrErrorRates, uncorrErrorRates]

	# Create a figure instance
	fig = plt.figure(1, figsize=(9,6))

	# Create an axes instance
	axes = fig.add_subplot(111)

	# Custom x-axis labels
	labels = ['Corrected Reads', 'Uncorrected Read']
	axes.set_xticklabels(labels)

	# Keep only the bottom and left axes
	axes.get_xaxis().tick_bottom()
	axes.get_yaxis().tick_left()

	# Create the boxplot	
	bp = axes.boxplot(data) 

	# Save the figure
	savePath = "%s_error_rate_boxplot.png" % (testPrefix)
	fig.savefig(savePath, bbox_inches='tight')

def findMeanAndStdev(errorRates):
	'''
	Accepts a list of tuples of read length and error rate. 

	Returns a list of means and standard deviations of the error rates of the reads
	whose lengths fall between intervals starting from 0 to g_maxReadLength of size
	g_binNumber. 
	'''
	length = len(errorRates)
	errorRates = np.array(errorRates).reshape( length, 2 )
	bins = np.linspace(0, g_maxReadLength, g_binNumber) 

	# Digitize returns the indices of the elements that belong to bin i
	# i.e. implicitly describes which length/error rate tuple falls in which bin
	digitized = np.digitize(errorRates[:,0], bins)
	# For each bin, find the mean error rate
	means = [ np.mean( errorRates[digitized == i, 1], dtype=np.float64 ) for i in range( 1, len(bins) ) ]

	# For each bn, find the standard deviation of the error rates
	stdevs = [ np.std( errorRates[digitized == i, 1], dtype=np.float64 ) for i in range( 1, len(bins) ) ]

	return means, stdevs

def makeErrorRateBarGraph(data, testPrefix):
	'''
	Creates an error rate bar graph and saves at the location given
	by testPrefix.
	Standard deviations are represented by error bars.
	The extension of the file is .png

	Accepts a list of either ReadDatum or UntrimmedDatum objects and
	a prefix designating the name of file and save location.
	Returns nothing.
	'''
	corrErrorRates = [] 
	uncorrErrorRates = [] 

	# Collect the data from the stats list
	for read in data:
		corrLength = read.getCorrLength()
		corrErrorRate = read.getCorrErrorRate()
		corrDataPoint = (corrLength,corrErrorRate)
		corrErrorRates.append(corrDataPoint)

		uncorrLength = read.getUncorrLength()
		uncorrErrorRate = read.getUncorrErrorRate()
		uncorrDataPoint = (uncorrLength,uncorrErrorRate)
		uncorrErrorRates.append(uncorrDataPoint)

	# Find mean, stdev
	corrMean, corrStdev = findMeanAndStdev(corrErrorRates)
	uncorrMean, uncorrStdev = findMeanAndStdev(uncorrErrorRates)

	# Remove last element in ind so that its length matches the length of the means
	ind = np.linspace(0, g_maxReadLength, g_binNumber)
	ind = np.delete(ind, -1)

	fig, axes = plt.subplots()

	# Set size of graph
	length = 40
	height = 20
	fig.set_size_inches(length, height)	

	# Bar width specification
	width = (1/2)*ceil( g_maxReadLength / g_binNumber ) 
	
	# Create the corrected long read bar graph
	corrGraph = axes.bar(ind, corrMean, width, color='r', yerr=corrStdev, align='edge')

	# Create the uncorrected long read bar graph
	uncorrGraph = axes.bar(ind+width, uncorrMean, width, color='y', yerr=uncorrStdev)

	# Add labels to graph
	axes.set_ylabel("Mean error rates of reads")
	axes.set_xlabel("Length of read")
	axes.set_title("Mean Error Rates of Corrected and Uncorrected Reads by Length")

	# The lengths that fall in each bin
	lengthBins = np.linspace(0, g_maxReadLength, g_binNumber)
	
	# Create x-tick labels
	axes.set_xticks(lengthBins + width)
	binSize = len(lengthBins)
	xticklabels = ["%d" % (lengthBins[i+1]) for i in range(binSize) if i < binSize - 1]
	axes.set_xticklabels(xticklabels)

	axes.legend( (corrGraph[0], uncorrGraph[0]), ('Corrected Reads', 'Uncorrected Reads') )

	savePath = "%s_error_rates_bargraph.png" % (testPrefix)
	fig.savefig(savePath, dpi=100, bbox_inches='tight')

def getUncorrThroughput(data):
	'''
	Accepts as input a list of ReadDatum objects.

	Returns the total throughput, which is defined as the sum of the lengths of
	all the reads.
	'''
	uncorrThroughput = 0
	for datum in data:
		uncorrThroughput += datum.getUncorrLength()
	return uncorrThroughput	

def getTrueAndFalsePositives(data):
	'''
	Accepts as input a list of UntrimmedDatum objects.

	Returns the total number of true positives and false positives in
	corrected and uncorrected regions of the corrected long reads.
	'''
	corrTruePos, corrFalsePos, uncorrTruePos, uncorrFalsePos = (0, 0, 0, 0)

	for datum in data:
		corrTruePos = corrTruePos + datum.getCorrTruePositives()
		corrFalsePos = corrFalsePos + datum.getCorrFalsePositives()
		uncorrTruePos = uncorrTruePos + datum.getUncorrTruePositives()
		uncorrFalsePos = uncorrFalsePos + datum.getUncorrFalsePositives()

	assert corrTruePos != 0

	return (corrTruePos, corrFalsePos, uncorrTruePos, uncorrFalsePos)

def getTotalUncorrErrors(data):
	'''
	Accepts as input a list of ReadDatum objects.

	Returns the total number of erroreneous bases in the uncorrected long reads.
	'''
	uReadErrors = 0
	for datum in data:
		uReadErrors += datum.getUncorrErrors()
	return uReadErrors 

def makeThroughputBarGraph(data, testPrefix):
	'''
	Accepts as input either a list of ReadDatum objects.
	and a string testPrefix.

	Saves to disk a stacked bar graph comparing the throughputs of corrected and
	uncorrected long reads, the two stacks that compose a bar are the total number
	of true positives and total number of false positives, all at the location and
	with file name specified with testPrefix. 
	'''
	(corrTrue, corrFalse, uncorrTrue, uncorrFalse) = getTrueAndFalsePositives(data)

	uncorrThroughput = getUncorrThroughput(data)	
	uncorrErrors = getTotalUncorrErrors(data)
	# Since the number of correct bases is equivalent to the total
	# number of bases less the erroneous
	uncorrCorrect = uncorrThroughput - uncorrErrors
	
	# Make two subplots, one for corrected long reads and the other for
	# corrected long reads. The subplots share the y-axis.
	fig, axes = plt.subplots()

	# Set size of graph
	length = 40
	height = 20
	fig.set_size_inches(length, height)	

	# Since we only have one bar, the number of independent variables is 1
	ind = 1
	width = 0.1 

	# Plot the corrected bar graph
	uncorrFalsePosBar = axes.bar(ind, uncorrFalse, width, color='r')
	uncorrTruePosBar = axes.bar(ind, uncorrTrue, width, bottom=uncorrFalse, color='r')
	corrFalsePosBar = axes.bar(ind, corrFalse, width, bottom=uncorrTrue, color='y')
	corrTruePosBar = axes.bar(ind, corrTrue, width, bottom=corrFalse, color='y') 

	# Plot the uncorrected bar graph
	# uncorrErrorsBar = axes.bar(ind, uncorrErrors, width='b')
	# uncorrCorrectBar = axes.bar(ind, uncorrCorrect, width, bottom=uncorrErrors, color='b')

	savePath = "%s_throughput_bar_graph.png" % (testPrefix)
	fig.savefig(savePath, bbox_inches='tight')

def findMutationProportions(data):
	'''
	Accepts as input a list of ReadDatum objects.

	Returns three lists of pairs, one for deletion, insertion and substitution, 
	where the first object in the pair is the length of the read and the second 
	is the mutation proportion. 
	'''
	return []
	

def makeMutationProportionsBarGraphs(data, testPrefix):
	'''
	Accepts as input list of ReadDatum objects and a string
	testPrefix.

	Saves to disk a 3 bar-graph diagram comparing the the deletion, insertion
	and substitution proportions of the corrected and uncorrected long reads.
	''' 
	return

def test():
	testPath = "test.stats"

	with open(testPath, 'w') as file:
		N = 10000
		data = []

		for i in range(N):
			cLength = randint(1,g_maxReadLength)
			uLength = cLength

			cDel = ceil( (9/2000)*cLength )
			cIns = cDel
			cSub = ceil( (1/1000)*cLength )

			uDel = ceil( (9/200)*uLength )
			uIns = uDel
			uSub = ceil( (1/100)*uLength )

			cFalsePos = cDel + cIns + cSub
			cTruePos = cLength - cFalsePos 
			uFalsePos = uDel + uIns + uSub
			uTruePos = uLength - uFalsePos
			line = "%s %d %d %d %d %d %d %d %d %d %d %d %d\n" % ('u', cLength, uLength, cDel, cIns, cSub, uDel, uIns, uSub, cTruePos, cFalsePos, uTruePos, uFalsePos)
			file.write(line)

	untrimmedData = retrieveRawData(testPath)[1]

	testPrefix = "/Users/laseanl/Documents/test"
	# makeErrorRateBarGraph(trimmedData, testPrefix)	
	makeThroughputBarGraph(untrimmedData, testPrefix)

# global variables
# Maximum expected read length
g_maxReadLength = 60000
# Number of read length bins
g_binNumber = 50

helpMessage = "Visual long read correction data statistics."
#usageMessage = "Usage: %s [-h help and usage] [-i directory]" % (sys.argv[0])
usageMessage = "Usage: %s [-h help and usage] [-t test functions]" % (sys.argv[0])
options = "hi:o:t"

try:
	opts, args = getopt.getopt(sys.argv[1:], options)
except getopt.GetoptError:
	print "Error: unable to read command line arguments."
	sys.exit(2)

if len(sys.argv) == 1:
	print usageMessage
	sys.exit(2)

inputPath = ""
outputPrefix = ""

for opt, arg in opts:
	if opt == '-h':
		print helpMessage
		print usageMessage
		sys.exit()
	elif opt == '-i':
		inputPath = arg
	elif opt == '-o':
		outputPrefix = arg
	elif opt == '-t':
		test()
		sys.exit()
	else:
		print "Error: unrecognized command line option."
		print helpMessage
		print usageMessage
		sys.exit(2)

optsIncomplete = False

if inputPath == "":
	print "Please provide an input path."
	optsIncomplete = True
if outputPath == "":
	print "Please provide an output prefix."
	optsIncomplete = True
if optsIncomplete:
	print usageMessage
	sys.exit(2)
