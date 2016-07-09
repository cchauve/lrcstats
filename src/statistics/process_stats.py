import sys, os, getopt
import numpy as np
import matplotlib as mpl
# agg backend is used to create plot as a .png file
mpl.use('agg')
import matplotlib.pyplot as plt
from random import randint
import math # for ceil

class ReadDatum(object):
	'''
	Preprocesses and outputs general statistics for reads.
	'''
	def __init__(self, data):
		'''
		Accepts as input list of trimmed read data points obtained
		directly from the STATS file outputted by lrcstats
		'''
		data = [int(datum) in datum in data[1:]]
		self.cLength = data[1]
		self.uLength = data[2]

		self.cDel = data[3]
		self.uDel = data[4]
		self.cIns = data[5]
		self.uIns = data[6]
		self.cSub = data[7]
		self.uSub = data[8]

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
		return (self.uDel + self.uIns + self.uSub)/self.uLength

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


class UntrimmedReadDatum(ReadDatum):
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
		data = [int(datum) in datum in data[1:]]

		self.correctedTruePos = data[9]
		self.correctedFalsePos = data[10]
		self.uncorrectedTruePos = data[11]
		self.uncorrectedFalsePos = data[12]

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
	Returns two lists of UntrimmedReadDatum and ReadDatum objects,
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
			datum = UntrimmedReadDatum(datum)
			UntrimmedData.append(datum)
		elif datum[0] == 't':
			datum = ReadDatum(datum)
			TrimmedData.append(datum)

	return (TrimmedData, UntrimmedData)

def makeErrorRateBoxPlot(data, testPrefix):
	'''
	Creates an error rate frequency box plot and saves on disk.

	Accepts a list of either ReadDatum or UntrimmedReadDatum objects and
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
	g_readLengthInterval. 
	'''
	length = len(errorRates)
	errorRates = array(corrErrorRates).reshape( cLength, 2 )
	bins = np.linspace(0, g_maxReadLength, g_readLengthInterval) 

	# Digitize returns the indices of the elements that belong to bin i
	digitized = np.digitize(errorRates[:,1], bins)
	means = [ errorRates[digitized == i, 0].mean() for i in range( 1, len(bins) ) ]

	# Find the standard deviations
	stdevs = [ np.std( errorRates[digitized == i, 0], dtype=np.float64 ) for i in range( 1, len(bins) ) ]

	return means, stdevs

def makeErrorRateBarGraph(data, testPrefix):
	'''
	Creates an error rate bar graph and saves at the location given
	by testPrefix.
	Standard deviations are represented by error bars.
	The extension of the file is .png

	Accepts a list of either ReadDatum or UntrimmedReadDatum objects and
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

	fig, (corrAxes, uncorrAxes) = plt.subplots(1, 2, sharey=True)

	# Independent variable range
	bins = linspace(0, g_maxReadLength, g_readLengthInterval)
	
	# Create the corrected long read bar graph
	corrAxes.bar(corrInd, corrMean, yerr=corrStdev)

	# Create the uncorrected long read bar graph
	uncorrAxes.bar(uncorrInd, uncorrMean, yerr=uncorrStdev)

	savePath = "%s_error_rates_bargraph.png" % (testPrefix)
	fig.savefig(savePath, bbox_inches='tight')

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
	Accepts as input a list of UntrimmedReadDatum objects.

	Returns the total number of true positives and false positives in
	corrected and uncorrected regions of the corrected long reads.
	'''
	corrTruePos, corrFalsePos, uncorrTruePos, uncorrFalsePos = 0

	for datum in data:
		corrTruePos += datum.getCorrectedTruePositives()
		corrFalsePOs += datum.getCorrectedFalsePositives()
		uncorrTruePos += datum.getUncorrectedTruePositives()
		uncorrFalsePos += datum.getUncorrectedFalsePositives()

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
	fig, (corrAxes, uncorrAxes) = plt.subplots(2, sharey=True)

	# Since we only have one bar, the number of independent variables is 1
	ind = 1
	width = 0.35

	# Plot the corrected bar graph
	corrAxes.bar(ind, uncorrFalse, width)
	corrAxes.bar(ind, uncorrTrue, width, bottom=uncorrFalse)
	corrAxes.bar(ind, corrFalse, width, bottom=uncorrTrue)
	corrAxes.bar(ind, corrTrue, width, bottom=corrFalse) 

	# Plot the uncorrected bar graph
	uncorrAxes.bar(ind, uncorrErrors, width)
	uncorrAxes.bar(ind, uncorrCorrect, width, bottom=uncorrErrors)

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

def untrimmedTest():
	testPath = "test.stats"

	with open(testPath, 'w') as file:
		N = 10000
		data = []

		for i in range(N):
			cLength = randint(1,60000)
			uLength = cLength
			cLength = uLength 

			cDel = math.ceil( (9/2000)*cLength )
			cIns = cDel
			cSub = math.ceil( (1/1000)*cLength )

			uDel = math.ceil( (9/2000)*uLength )
			uIns = uDel
			uSub = math.ceil( (1/1000)*uLength )

			cFalsePos = cDel + cIns + cSub
			cTruePos = cLength - cFalsePos 
			uFalsePos = uDel + uIns + uSub
			uTruePos = uLength - uFalsePos
			line = "%s %d %d %d %d %d %d %d %d %d %d %d %d\n" % ('t', cLength, uLength, cDel, cIns, cSub, uDel, uIns, uSub, cFalsePos, cTruePos, uFalsePos, uTruePos)
			file.write(line)

	data = retrieveRawData(testPath)[0]

	testPrefix = "test"
	makeErrorRateBarGraph(data, testPrefix)	

# global variables
# Maximum expected read length
g_maxReadLength = 15000
# Interval of read length bins
g_readLengthInterval = 100

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
		untrimmedTest()
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
