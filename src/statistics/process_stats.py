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
	# Keys for ReadDatum member variable dictionary
	corrReadLength_k = "CORRECTED READ LENGTH"
	uncorrReadLength_k = "UNCORRECTED READ LENGTH"

	corrAlignmentLength_k = "CORRECTED ALIGNMENT LENGTH"
	uncorrAlignmentLength_k = "UNCORRECTED ALIGNMENT LENGTH"

	corrDel_k = "CORRECTED DELETION"
	corrIns_k = "CORRECTED INSERTION"
	corrSub_k = "CORRECTED SUBSTITUTION"

	uncorrDel_k = "UNCORRECTED DELETION"
	uncorrIns_k = "UNCORRECTED INSERTION"
	uncorrSub_k = "UNCORRECTED SUBSTITUTION"

	cTruePos_k = "CORRECTED TRUE POSITIVE"
	cFalsePos_k = "CORRECTED FALSE POSITIVE"
	uTruePos_k = "UNCORRECTED TRUE POSITIVE"
	uFalsePos_k = "UNCORRECTED FALSE POSITIVE"

	KEYS_g = [corrReadLength_k, uncorrReadLength_k, corrDel_k, corrIns_k, corrSub_k,
		uncorrDel_k, uncorrIns_k, uncorrSub_k, cTruePos_k, cFalsePos_k,
		uTruePos_k, uFalsePos_k]	
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
		assert len(data) == 9 or len(data) == 13

		for i in range(1, len(data)):
			self.data[ ReadDatum.KEYS_g[i-1] ] = int(data[i])

	def getCorrLength(self):
		'''
		Returns the length of the corrected long read.
		'''
		return self.data[ReadDatum.corrReadLength_k]

	def getCorrErrors(self):
		'''
		Returns the number of errors in the read.
		'''
		cDel = self.data[ReadDatum.corrDel_k]
		cIns = self.data[ReadDatum.corrIns_k]
		cSub = self.data[ReadDatum.corrSub_k]
		return cDel + cIns + cSub

	def getCorrErrorRate(self):
		'''
		Returns the error rate of the corrected trimmed long read,
		which is defined as the number of mutations divided by
		the length of the read.
		'''
		cDel = self.data[ReadDatum.corrDel_k]
		cIns = self.data[ReadDatum.corrIns_k]
		cSub = self.data[ReadDatum.corrSub_k]

		mutations = cDel + cIns + cSub
		length = self.data[ReadDatum.corrReadLength_k]	

		if length == 0 and mutations == 0:
			return 0
		elif length == 0 and mutations != 0:
			return 1
		else
			return (cDel + cIns + cSub)/cLength

	def getUncorrLength(self):
		'''
		Returns the length of the corresponding uncorrected long read.
		'''
		uLength = self.data[ReadDatum.uncorrReadLength_k]
		return uLength

	def getUncorrErrorRate(self):
		'''
		Returns the error rate of the corresponding long read,
		which is defined as the number of mutations divided by
		the length of the read.
		'''
		uDel = self.data[ReadDatum.uncorrDel_k]
		uIns = self.data[ReadDatum.uncorrIns_k]
		uSub = self.data[ReadDatum.uncorrSub_k]
		uLength = self.data[ReadDatum.uncorrReadLength_k]	
		return (uDel + uIns + uSub)/uLength

	def getUncorrErrors(self):
		'''
		Returns the number of erroreneous bases in the uncorrected
		long read.
		'''
		uDel = self.data[ReadDatum.uncorrDel_k]
		uIns = self.data[ReadDatum.uncorrIns_k]
		uSub = self.data[ReadDatum.uncorrSub_k]
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
		cDel = self.data[ReadDatum.corrDel_k]
		return cDel

	def getCorrIns(self):
		cIns = self.data[ReadDatum.corrIns_k]
		return cIns

	def getCorrSub(self):
		cSub = self.data[ReadDatum.corrSub_k]
		return cSub

	def getUncorrDel(self):
		uDel = self.data[ReadDatum.uncorrDel_k]
		return uDel

	def getUncorrIns(self):
		uIns = self.data[ReadDatum.uncorrIns_k]
		return uIns

	def getUncorrSub(self):
		uSub = self.data[ReadDatum.uncorrSub_k]
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
		correctedTruePos = self.data[ReadDatum.cTruePos_k]
		return correctedTruePos

	def getCorrFalsePositives(self):
		'''
		Corrected false positives are defined as bases that
		have been corrected and are NOT equivalent to its
		respective base in the reference alignment (not reference
		sequence)
		'''
		correctedFalsePos = self.data[ReadDatum.cFalsePos_k]
		return correctedFalsePos

	def getCorrSegmentErrorRate(self):
		'''
		Returns the error rate over only those segments
		in the corrected long read which have been
		corrected. 
		'''
		correctedTruePos = self.data[ReadDatum.cTruePos_k]
		correctedFalsePos = self.data[ReadDatum.cFalsePos_k]
		return (correctedFalsePos)/(correctedTruePos + correctedFalsePos)
	
	# These methods apply to the uncorrected segments of corrected long reads

	def getUncorrTruePositives(self):
		'''
		Uncorrected true positives are defined as bases
		that have NOT been corrected and are equivalent
		to its respective base in the reference alignment.
		'''
		uncorrectedTruePos = self.data[ReadDatum.uTruePos_k]
		return uncorrectedTruePos

	def getUncorrFalsePositives(self):
		'''
		Uncorrected false positives are defined as bases that
		have NOT been corrected and are NOT equivalent to its
		respective base in the reference alignment.
		'''
		uncorrectedFalsePos = self.data[ReadDatum.uFalsePos_k]
		return uncorrectedFalsePos

	def getUncorrSegmentErrorRate(self):
		'''
		Returns the error rate over only those segments of
		the corrected long read which have not been
		corrected.
		'''
		uncorrectedTruePos = self.data[ReadDatum.uTruePos_k]
		uncorrectedFalsePos = self.data[ReadDatum.uFalsePos_k]
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

def makeErrorRateBoxPlot(data, testName, trimmedOrUntrimmed, saveDir):
	'''
	Creates an error rate frequency box plot and saves on disk.

	Accepts a list of either ReadDatum or UntrimmedDatum objects and
	a prefix designating the name of file and save location, 
	a string testName designating the name of the correction
	algorithm used and the coverages, and a string trimmedOrUntrimmed
	indicating whether the reads are trimmed or untrimmed.
	Also accepts a string saveDir indicating the save directory.
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

	fig.suptitle( "%s - %s" % (testName, trimmedOrUntrimmed), y=1.10 )

	# Save the figure
	savePath = "%s/%s_%s_error_rate_boxplot.png" % (saveDir, testName, trimmedOrUntrimmed)
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

def makeErrorRateBarGraph(data, testName, trimmedOrUntrimmed, saveDir):
	'''
	Creates an error rate bar graph and saves at the location given
	by testPrefix.
	Standard deviations are represented by error bars.
	The extension of the file is .png

	Accepts a list of ReadDatum objects.
	testName indicates the program and coverage used.
	trimmedOrUntrimmed indicates whether the reads or trimmed or not.
	saveDir indicates the path to save the image in. 

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

	fig.suptitle( "%s - %s" % (testName, trimmedOrUntrimmed), y=1.10 )

	savePath = "%s/%s_%s_error_rates_bargraph.png" % (saveDir, testName, trimmedOrUntrimmed)
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

def makeUntrimmedThroughputBarGraph(data, testName, saveDir):
	'''
	Accepts as input either a list of ReadDatum objects.
	and a string testPrefix.

	testName indicates the program and coverage used.
        saveDir indicates the path to save the image in.

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
	corrAxes.set_xlabel("Corrected Reads")
	uncorrAxes.set_xlabel("Uncorrected Reads")

	# Remove xtick labels
	for axes in (corrAxes, uncorrAxes):
		for label in axes.get_xticklabels():
			label.set_visible(False)

	fig.suptitle("Composition of Throughput of Untrimmed Corrected Reads and Uncorrected Reads", y=1.10)

	savePath = "%s/%s_untrimmed_throughput_bar_graph.png" % (saveDir, testName)
	fig.savefig(savePath, bbox_inches='tight')

def getCorrThroughputAndErrors(data):
	'''
	Accepts as input a list of ReadDatum objects.
	Returns the total throughput and the total number of errors.	
	'''
	throughput = 0
	errors = 0
	for datum in data:
		throughput += datum.getCorrLength()
		errors += datum.getCorrErrors()	
	return throughput, errors

def makeTrimmedThroughputBarGraph(data, testName, saveDir):
	'''
	Accepts as input either a list of ReadDatum objects.
	and a string testPrefix.

	testName indicates the program and coverage used.
        saveDir indicates the path to save the image in.

	Saves to disk a stacked bar graph of the throughput of corrected 
	long reads, the stacks that composes the bar are the total number
	of correct bases and the total number of incorrect bases, saved at the location and
	with file name specified with testPrefix. 
	'''
	throughput, errors = getCorrThroughputAndErrors(data)
	correct = throughput - errors
	assert correct > 0

	fig, axes = plt.subplots()

	# Set size of graph
	length = 20
	height = 10
	fig.set_size_inches(length, height)	

	numItems = 1

	# Set size of graph
	length = 5
	height = 15
	fig.set_size_inches(length, height)	

	ind = np.arange(numItems)

	margin = 0.30

	# Set the bar width
	width = 0.15

	# Plot the graph
	# The color is red
	errorPlot = axes.bar(ind,
			errors,
			width,
			color='#C25B46')
	
	correctPlot = axes.bar(ind,
			correct,
			width,
			bottom=errors,
			color='#69B957') 

	# Add the legend
	axes.legend( 
		[errorPlot, correctPlot],
		["Erroneous bases", "Correct Bases"])

	# Add labels to graph
	axes.set_ylabel("Number of bases")
	axes.set_xlabel("Corrected Long Reads")
	axes.set_title("Throughput composition of Trimmed Portion of Corrected Long Reads", y=1.08)

	# Remove xtick labels
	for label in axes.get_xticklabels():
		label.set_visible(False)

	fig.suptitle( "%s" % (testName), y=1.10 )

	savePath = "%s/%s_trimmed_throughput_bar_graph.png" % (saveDir, testName)
	fig.savefig(savePath, bbox_inches='tight')

def findLengths(trimmedData, untrimmedData):
	'''
	Accepts as input lists of TrimmedDatum and UntrimmedDatum objects.
	Returns two lists containing the lengths of all the trimmed corrected
	reads and uncorrected reads.
	'''
	corrLengths = []	
	uncorrLengths = []

	for datum in trimmedData:
		corrLengths.append( datum.getCorrLength() )

	for datum in untrimmedData:
		uncorrLengths.append( datum.getUncorrLength() )

	return corrLengths, uncorrLengths

def makeLengthHistograms(trimmedData, untrimmedData, testName, saveDir):
	'''
	Accepts as input list of TrimmedDatum and UntrimmeDatum objects.

	testName indicates the program and coverage used.
        saveDir indicates the path to save the image in.

	Creates and saves a histogram of the lengths of corrected
	and uncorrected reads.
	'''
	corrLengths, uncorrLengths = findLengths(trimmedData, untrimmedData)

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
	axes.set_title("Histogram of lengths of trimmed corrected long reads and uncorrected long reads", y=1.08)

	fig.suptitle( "%s" % (testName), y=1.10 )

	savePath = "%s/%s_length_histograms.png" % (saveDir, testName)
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

def makeErrorRateScatterPlot(data, testName, trimmedOrUntrimmed, saveDir):
	'''
	Accepts as input a list of ReadDatum objects.

	testName indicates the program and coverage used.
        trimmedOrUntrimmed indicates whether the reads or trimmed or not.
        saveDir indicates the path to save the image in.
 
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
	fig.suptitle( "%s - %s" % (testName, trimmedOrUntrimmed), y=1.10 )

	savePath = "%s/%s_%s_error_rate_scatter.png" % (saveDir, testName, trimmedOrUntrimmed)
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

def makeMutationsBarGraph(data, testName, saveDir):
	'''
	Accepts as input a list of TrimmedDatum objects.
	testName indicates the program and coverage used.
        saveDir indicates the path to save the image in.

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

	fig.suptitle( "%s" % (testName) )
	savePath = "%s/%s_mutations_bar_graph.png" % (saveDir, testName)
	fig.savefig(savePath, bbox_inches='tight')

def test(saveDir):
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

	testName = "test"
	
	for data in (trimmedData, untrimmedData):
		if data is trimmedData:
			trimmedOrUntrimmed = "trimmed"
		else:
			trimmedOrUntrimmed = "untrimmed"
		makeErrorRateBarGraph(data, testName, trimmedOrUntrimmed, saveDir) 
		makeErrorRateBoxPlot(data, testName, trimmedOrUntrimmed, saveDir) 
		makeErrorRateScatterPlot(data, testName, trimmedOrUntrimmed, saveDir) 

	makeUntrimmedThroughputBarGraph(untrimmedData, testName, saveDir)
	makeTrimmedThroughputBarGraph(trimmedData, testName, saveDir)
	makeMutationsBarGraph(trimmedData, testName, saveDir)
	makeLengthHistograms(trimmedData, untrimmedData, testName, saveDir)

# global variables

# Maximum expected read length
maxReadLength_g = 60000

# Number of read length bins
binNumber_g = 50


helpMessage = "Visualize long read correction data statistics."
usageMessage = "Usage: %s [-h help and usage] [-i stats file input path] [-d output directory] [-n experiment name]" % (sys.argv[0])
options = "hi:d:n:t"

try:
	opts, args = getopt.getopt(sys.argv[1:], options)
except getopt.GetoptError:
	print "Error: unable to read command line arguments."
	sys.exit(2)

if len(sys.argv) == 1:
	print usageMessage
	sys.exit(2)

inputPath = ""
saveDir = ""
testName = ""
testRun = False

for opt, arg in opts:
	if opt == '-h':
		print helpMessage
		print usageMessage
		sys.exit()
	elif opt == '-i':
		inputPath = arg
	elif opt == '-d':
		saveDir = arg
	elif opt == '-n':
		testName = arg
	elif opt == '-t':
		testRun = True

optsIncomplete = False

if inputPath == "" and not testRun:
	print "Please provide an input path."
	optsIncomplete = True
if saveDir == "":
	print "Please provide the output directory."
	optsIncomplete = True
if testName == "":
	print "Please indicate the name of the experiment."
	optsIncomplete = True 

if optsIncomplete:
	print usageMessage
	sys.exit(2)

if testRun:
	test(saveDir)
	sys.exit()

print "The command used to run this program was: %s" % ( " ".join(sys.argv) )

trimmedData, untrimmedData = retrieveRawData(inputPath)

# Generate data. If the appropriate data list is empty, skip it.
for data in (trimmedData, untrimmedData):
	if data is trimmedData:
		trimmedOrUntrimmed = "trimmed"
	else:
		trimmedOrUntrimmed = "untrimmed"

	if len(data) > 0:
		makeErrorRateBarGraph(data, testName, trimmedOrUntrimmed, saveDir) 
		makeErrorRateBoxPlot(data, testName, trimmedOrUntrimmed, saveDir) 
		makeErrorRateScatterPlot(data, testName, trimmedOrUntrimmed, saveDir) 
	else:
		print "No %s read data; skipping creation of trimmed error rate graphs." % (trimmedOrUntrimmed)

if ( len(untrimmedData) > 0 ):
	makeUntrimmedThroughputBarGraph(untrimmedData, testName, saveDir)
else:
	print "No untrimmed data; skipping creation of untrimmed throughput bar graph."

if ( len(trimmedData) > 0 ):
	makeTrimmedThroughputBarGraph(trimmedData, testName, saveDir)
	makeMutationsBarGraph(trimmedData, testName, saveDir)
else:
	print "No trimmed data; skipping creation of trimmed read throughput graph and mutations bar graph."

if ( len(trimmedData) > 0 and len(untrimmedData) > 0 ):
	makeLengthHistograms(trimmedData, untrimmedData, testName, saveDir)
else:
	print "Either no trimmed read data or untrimmed read data; skipping creation of length histogram."

print "Visualization completed."
