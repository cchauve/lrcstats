from __future__ import division
import sys, os, getopt
from random import randint
from math import ceil
from math import floor
import numpy as np

import matplotlib as mpl
# agg backend is used to create plot as a .png file
mpl.use('agg')

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

class ReadDatum(object):
	'''
	Preprocesses and outputs general statistics for reads.
	'''
	def __init__(self, data):
		'''
		Accepts as input list of trimmed read data points obtained
		directly from the STATS file outputted by lrcstats
		'''
		self.data = {}
		# KEYS_g is a global variable and contains the keys
		# for the data dictionary in ReadDatum objects.
		# These keys can be found initialized in the main body of the
		# program.
		for i in range(1, len(data)):
			self.data[ KEYS_g[i-1] ] = int(data[i])

	def getCorrLength(self):
		'''
		Returns the length of the corrected long read.
		'''
		return self.data[corrLength_k]

	def getCorrErrorRate(self):
		'''
		Returns the error rate of the corrected trimmed long read,
		which is defined as the number of mutations divided by
		the length of the read.
		'''
		cDel = self.data[corrDel_k]
		cIns = self.data[corrIns_k]
		cSub = self.data[corrSub_k]
		cLength = self.data[corrLength_k]	
		return (cDel + cIns + cSub)/cLength

	def getUncorrLength(self):
		'''
		Returns the length of the corresponding uncorrected long read.
		'''
		uLength = self.data[uncorrLength_k]
		return uLength

	def getUncorrErrorRate(self):
		'''
		Returns the error rate of the corresponding long read,
		which is defined as the number of mutations divided by
		the length of the read.
		'''
		uDel = self.data[uncorrDel_k]
		uIns = self.data[uncorrIns_k]
		uSub = self.data[uncorrSub_k]
		uLength = self.data[uncorrLength_k]	
		return (uDel + uIns + uSub)/uLength

	def getUncorrErrors(self):
		'''
		Returns the number of erroreneous bases in the uncorrected
		long read.
		'''
		uDel = self.data[uncorrDel_k]
		uIns = self.data[uncorrIns_k]
		uSub = self.data[uncorrSub_k]
		return uDel + uIns + uSub

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

	# Get the corresponding number of mutations of the corrected long read
	# and its corresponding uncorrected read

	def getCorrDel(self):
		cDel = self.data[corrDel_k]
		return cDel

	def getCorrIns(self):
		cIns = self.data[corrIns_k]
		return cIns

	def getCorrSub(self):
		cSub = self.data[corrSub_k]
		return cSub

	def getUncorrDel(self):
		uDel = self.data[uncorrDel_k]
		return uDel

	def getUncorrIns(self):
		uIns = self.data[uncorrIns_k]
		return uIns

	def getUncorrSub(self):
		uSub = self.data[uncorrSub_k]
		return uSub

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

	def getCorrTruePositives(self):
		'''
		Corrected true positives are defined as bases that
		have been corrected and are equivalent to its respective
		base in the referene alignment (not reference sequence)
		'''
		correctedTruePos = self.data[cTruePos_k]
		return correctedTruePos

	def getCorrFalsePositives(self):
		'''
		Corrected false positives are defined as bases that
		have been corrected and are NOT equivalent to its
		respective base in the reference alignment (not reference
		sequence)
		'''
		correctedFalsePos = self.data[cFalsePos_k]
		return correctedFalsePos

	def getCorrSegmentErrorRate(self):
		'''
		Returns the error rate over only those segments
		in the corrected long read which have been
		corrected. 
		'''
		correctedTruePos = self.data[cTruePos_k]
		correctedFalsePos = self.data[cFalsePos_k]
		return (correctedFalsePos)/(correctedTruePos + correctedFalsePos)
	
	# These methods apply to the uncorrected segments of corrected long reads

	def getUncorrTruePositives(self):
		'''
		Uncorrected true positives are defined as bases
		that have NOT been corrected and are equivalent
		to its respective base in the reference alignment.
		'''
		uncorrectedTruePos = self.data[uTruePos_k]
		return uncorrectedTruePos

	def getUncorrFalsePositives(self):
		'''
		Uncorrected false positives are defined as bases that
		have NOT been corrected and are NOT equivalent to its
		respective base in the reference alignment.
		'''
		uncorrectedFalsePos = self.data[uFalsePos_k]
		return uncorrectedFalsePos

	def getUncorrSegmentErrorRate(self):
		'''
		Returns the error rate over only those segments of
		the corrected long read which have not been
		corrected.
		'''
		uncorrectedTruePos = self.data[uTruePos_k]
		uncorrectedFalsePos = self.data[uFalsePos_k]
		return (uncorrectedFalsePos)/(uncorrectedTruePos + uncorrectedFalsePos)

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
			datum = TrimmedDatum(datum)
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

	fig, axes = plt.subplots()

	# Set size of graph
	length = 9
	height = 9
	fig.set_size_inches(length, height)	

	# Custom x-axis labels
	labels = ['Corrected Reads', 'Uncorrected Read']
	axes.set_xticklabels(labels)

	# Keep only the bottom and left axes
	axes.get_xaxis().tick_bottom()
	axes.get_yaxis().tick_left()

	# Set the labels of the graph
	axes.set_ylabel("Error Rate")
	axes.set_title("Frequency of error rates in corrected and uncorrected long reads.")

	# Create the boxplot	
	bp = axes.boxplot(data) 

	# Save the figure
	savePath = "%s_error_rate_boxplot.png" % (testPrefix)
	fig.savefig(savePath, bbox_inches='tight')

def findMeanAndStdev(errorRates):
	'''
	Accepts a list of tuples of read length and error rate. 

	Returns a list of means and standard deviations of the error rates of the reads
	whose lengths fall between intervals starting from 0 to maxReadLength_g of size
	binNumber_g. 
	'''
	length = len(errorRates)
	errorRates = np.array(errorRates).reshape( length, 2 )
	bins = np.linspace(0, maxReadLength_g, binNumber_g) 

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
	ind = np.linspace(0, maxReadLength_g, binNumber_g)
	ind = np.delete(ind, -1)

	fig, axes = plt.subplots()

	# Show left and bottom spines
	axes.yaxis.set_ticks_position('left')
	axes.xaxis.set_ticks_position('bottom')

	# Set size of graph
	length = 20
	height = 10
	fig.set_size_inches(length, height)	

	# Bar width specification
	barWidth = (1/2)*ceil( maxReadLength_g / binNumber_g ) 
	
	# Create the corrected long read bar graph
	corrGraph = axes.bar(ind, corrMean, barWidth, color='#17B12B', yerr=corrStdev)
	# Create the uncorrected long read bar graph
	uncorrGraph = axes.bar(ind+barWidth, uncorrMean, barWidth, color='#F45F5B', yerr=uncorrStdev)

	# Add labels to graph
	axes.set_ylabel("Mean error rates of reads")
	axes.set_xlabel("Length of read")
	axes.set_title("Mean Error Rates of Corrected and Uncorrected Reads by Length")

	# The lengths that fall in each bin
	lengthBins = np.linspace(0, maxReadLength_g, binNumber_g/5)
	
	# Create x-tick labels
	axes.set_xticks(lengthBins)

	# Set the legend
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

	fig, (corrAxes, uncorrAxes) = plt.subplots(1, 2, sharey=True)

	# Move subplots closer together
	fig.subplots_adjust(hspace=1.0)

	numItems = 1

	# Set size of graph
	length = 5
	height = 15
	fig.set_size_inches(length, height)	

	ind = np.arange(numItems)

	margin = 0.30

	# Set the bar width
	width = 0.15

	# Plot the corrected bar graph
	uncorrFalsePos = corrAxes.bar(
				ind,
				uncorrFalse,
				width,
				color='#C25B46')

	corrFalsePos = corrAxes.bar(
				ind,
				corrFalse,
				width,
				bottom=uncorrFalse,
				color='#F6954A')

	uncorrTruePos = corrAxes.bar(
				ind,
				uncorrTrue,
				width,
				bottom=corrFalse+uncorrFalse,
				color='#4A87CA')

	corrTruePos = corrAxes.bar(
				ind,
				corrTrue,
				width,
				bottom=uncorrTrue+corrFalse+uncorrFalse,
				color='#69B957') 

	# Plot the uncorrected read bar graph
	uncorrIncorrect = uncorrAxes.bar(
				ind,
				uncorrErrors,
				width,
				color='#F45F5B')

	uncorrCorrect = uncorrAxes.bar(
				ind,
				uncorrCorrect,
				width,
				bottom=uncorrErrors,
				color='#17B12B')

	# Add the legend
	corrAxes.legend( 
		[corrTruePos, uncorrTruePos, corrFalsePos, uncorrFalsePos],
		["Corrected True Positives", "Uncorrected True Positives",
		"Corrected False Positives", "Uncorrected False Positives"], 
		bbox_to_anchor=[4.3,1], 
		borderaxespad=0.)

	uncorrAxes.legend( 
		[uncorrCorrect, uncorrIncorrect],
		["Correct Bases","Incorrect Bases"],
		bbox_to_anchor=[2.5,0.85],
		borderaxespad=0.)

	# Add labels to graph
	corrAxes.set_ylabel("Number of bases")
	corrAxes.set_xlabel("Corrected")
	uncorrAxes.set_xlabel("Uncorrected")

	# Remove xtick labels
	for axes in (corrAxes, uncorrAxes):
		for label in axes.get_xticklabels():
			label.set_visible(False)

	fig.suptitle("Composition of Throughput of Corrected and Uncorrected Reads")

	savePath = "%s_throughput_bar_graph.png" % (testPrefix)
	fig.savefig(savePath, bbox_inches='tight')

def findLengths(data):
	'''
	Accepts as input a list of ReadDatum objects.
	Returns two lists containing the lengths of all the corrected
	and uncorrected reads.
	'''
	corrLengths = []	
	uncorrLengths = []

	for datum in data:
		corrLengths.append( datum.getCorrLength() )
		uncorrLengths.append( datum.getCorrLength() )

	return corrLengths, uncorrLengths

def makeLengthHistograms(data, savePrefix):
	'''
	Accepts as input a list of ReadDatum objects and
	a string for the save location.
	Creates and saves a histogram of the lengths of corrected
	and uncorrected reads.
	'''
	corrLengths, uncorrLengths = findLengths(data)

	assert len(corrLengths) > 0
	assert len(uncorrLengths) > 0

	fig, axes = plt.subplots()
	bins = np.linspace(0, maxReadLength_g, 50)

	# Create the actual histograms.
	axes.hist(corrLengths, bins, alpha=0.5, label="Corrected")
	axes.hist(uncorrLengths, bins, alpha=0.5, label="Uncorrected")

	axes.legend(loc='upper right')

	# Add labels
	axes.set_ylabel("Number of reads")
	axes.set_xlabel("Length of read")
	axes.set_title("Histogram of lengths of corrected and uncorrected long reads")

	savePath = "%s_length_histograms.png" % (savePrefix)
	fig.savefig(savePath, bbox_inches='tight')

def getErrorRates(data):
	'''
	Accepts as input a list of ReadDatum objects.
	Returns two lists containing all error rates of the
	corrected and uncorrected long reads.
	'''
	corrErrorRates = []
	uncorrErrorRates = []
	
	for datum in data:
		uncorrErrorRates.append( datum.getUncorrErrorRate() )
		corrErrorRates.append( datum.getCorrErrorRate() )
	
	return corrErrorRates, uncorrErrorRates

def makeErrorRateScatterPlot(data, savePrefix):
	'''
	Accepts as input a list of ReadDatum objects and a string
	indicating the file prefix and save location.
	Creates and saves an error rate scatter plot of the
	corrected and uncorrected reads.
	'''
	corrErrorRates, uncorrErrorRates = getErrorRates( data )	

	fig, axes = plt.subplots()
	axes.scatter(uncorrErrorRates, corrErrorRates)

	# Add labels
	axes.set_ylabel("Error Rate of Corrected Read")
	axes.set_xlabel("Error Rate of Uncorrected Read")
	axes.set_title("Error Rate of Corresponding Corrected and Uncorrected Reads")

	savePath = "%s_error_rate_scatter.png" % (savePrefix)
	fig.savefig(savePath, bbox_inches='tight')

def getTotalMutations(data):
	'''
	Accepts as input a list of TrimmedDatum objects.
	Returns the total number of mutations for the corrected long read and the
	corresponding uncorrected long read.
	'''
	corrDel = 0
	uncorrDel = 0

	corrIns = 0
	uncorrIns = 0

	corrSub = 0
	uncorrSub = 0

	for datum in data:
		corrDel += datum.getCorrDel()
		uncorrDel += datum.getUncorrDel()

		corrIns += datum.getCorrIns()
		uncorrIns += datum.getUncorrIns()

		corrSub += datum.getCorrSub()
		uncorrSub += datum.getUncorrSub()

	return corrDel, uncorrDel, corrIns, uncorrIns, corrSub, uncorrSub

def makeMutationsBarGraph(data, savePrefix):
	'''
	Accepts as input a list of TrimmedDatum objects and a string.
	Create a bar graph displaying the amount of mutation errors in
	corrected long reads and its corresponding uncorrected read. 
	'''
	corrDel, uncorrDel, corrIns, uncorrIns, corrSub, uncorrSub = getTotalMutations(data) 
	corrData = [corrDel, corrIns, corrSub]
	uncorrData = [uncorrDel, uncorrIns, uncorrSub]
	
	ind = np.arange(3)
	width = 0.35
	
	fig, axes = plt.subplots()

	corrPlot = axes.bar(ind, corrData, width, color="#17B12B")
	uncorrPlot = axes.bar(ind+width, uncorrData, width, color="#F45F4B")

	axes.set_title("Number of Mutations in Corrected and Uncorrected Long Reads")
	axes.set_xticks(ind+width)
	axes.set_xticklabels( ('Deletions', 'Insertions', 'Substitutions') )
	axes.legend( (corrPlot[0], uncorrPlot[0]), ('Corrected', 'Uncorrected') )

	savePath = "%s_mutations_bar_graph.png" % (savePrefix)
	fig.savefig(savePath, bbox_inches='tight')

def test(testPrefix):
	testPath = "test.stats"

	with open(testPath, 'w') as file:
		N = 1000
		data = []

		for i in range(N):
			cLength = randint(1,maxReadLength_g)
			uLength = randint(1,maxReadLength_g)

			cDel = ceil( cLength * 0.01 )
			cIns = ceil( cLength * 0.01 ) 
			cSub = ceil( cLength * 0.01 ) 

			uDel = ceil( uLength * 0.05 )			
			uIns = ceil( uLength * 0.05 )
			uSub = ceil( uLength * 0.1 )

			cFalsePos = ceil( 0.2*(cDel + cIns + cSub) )
			uFalsePos = floor( 0.8*(cDel + cIns + cSub) ) 

			cTruePos = floor( ceil(0.8*cLength) - cFalsePos )
			uTruePos = ceil( floor(0.2*cLength) - uFalsePos )

			line = "%s %d %d %d %d %d %d %d %d %d %d %d %d\n" % ('t', cLength, uLength, cDel, cIns, cSub, uDel, uIns, uSub, cTruePos, cFalsePos, uTruePos, uFalsePos)
			file.write(line)
			line = "%s %d %d %d %d %d %d %d %d %d %d %d %d\n" % ('u', cLength, uLength, cDel, cIns, cSub, uDel, uIns, uSub, cTruePos, cFalsePos, uTruePos, uFalsePos)
			file.write(line)

	trimmedData, untrimmedData = retrieveRawData(testPath)

	makeErrorRateBarGraph(untrimmedData, testPrefix)	
	makeErrorRateBoxPlot(untrimmedData, testPrefix)
	makeThroughputBarGraph(untrimmedData, testPrefix)
	makeLengthHistograms(untrimmedData, testPrefix)
	makeErrorRateScatterPlot(untrimmedData, testPrefix)
	makeMutationsBarGraph(trimmedData, testPrefix)

# global variables

# Maximum expected read length
maxReadLength_g = 60000

# Number of read length bins
binNumber_g = 50

# Keys for ReadDatum member variable dictionary
corrLength_k = 0
uncorrLength_k = 1

corrDel_k = 2
corrIns_k = 3
corrSub_k = 4

uncorrDel_k = 5
uncorrIns_k = 6
uncorrSub_k = 7

cTruePos_k = 8
cFalsePos_k = 9
uTruePos_k = 10
uFalsePos_k = 11

KEYS_g=[corrLength_k, uncorrLength_k, corrDel_k, corrIns_k, corrSub_k,
	uncorrDel_k, uncorrIns_k, uncorrSub_k, cTruePos_k, cFalsePos_k,
	uTruePos_k, uFalsePos_k]	

helpMessage = "Visualize long read correction data statistics."
usageMessage = "Usage: %s [-h help and usage] [-i directory] [-o output prefix]" % (sys.argv[0])
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
testRun = False

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
		testRun = True

optsIncomplete = False

if inputPath == "" and not testRun:
	print "Please provide an input path."
	optsIncomplete = True
if outputPrefix == "":
	print "Please provide an output prefix."
	optsIncomplete = True
if optsIncomplete:
	print usageMessage
	sys.exit(2)

if testRun:
	test(outputPrefix)
