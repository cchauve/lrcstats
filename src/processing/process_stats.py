import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

class TrimmedStat:
	def __init__(self, data):
		self.cLength = data[1]
		self.uLength = data[2]
		self.cDel = data[3]
		self.uDel = data[4]
		self.cIns = data[5]
		self.uIns = data[6]
		self.cSub = data[7]
		self.uSub = data[8]

	def getCorrLength(self):
		return self.cLength

	def getUncorrLength(self):
		return self.uLength

	def getDelProportion(self):
		return self.cDel/self.uDel

	def getInsProportion(self):
		return self.cIns/self.uIns

	def getSubProportion(self):
		return self.cSub/self.uSub

	def getCorrErrorRate(self):
		return (self.cDel + self.cIns + self.cSub)/self.cLength

	def getUncorrErrorRate(self):
		return (self.uDel + self.uIns + self.uSub)/self.uLength

class UntrimmedStat:
	def __init__(self, data):
		self.cLength = data[1]
		self.uLength = data[2]

		self.cDel = data[3]
		self.uDel = data[4]
		self.cIns = data[5]
		self.uIns = data[6]
		self.cSub = data[7]
		self.uSub = data[8]
		
		self.correctedTruePos = data[9]
		self.correctedFalsePos = data[10]
		self.uncorrectedTruePos = data[11]
		self.uncorrectedFalsePos = data[12]

		self.correctedBases = data[13]
		self.uncorrectedBases = data[14]

	def getCorrLength(self):
		return self.cLength

	def getUncorrLength(self):
		return self.uLength

	def getCorrErrorRate(self):
		return (self.cDel + self.cIns + self.cSub)/self.cLength

	def getUncorrErrorRate(self):
		return (self.uDel + self.uIns + self.uSub)/self.uLength
		
def retrieveRawData(dataPath):
	rawData = []
	with open(dataPath, 'r') as file:
		for line in file:
			rawData.append(line)
	return rawData

def processRawData(rawData):
	TrimmedStats = []
	UntrimmedStats = []

	for datum in rawData:
		datum = datum.split()

		if datum[0] == 'u':
			stat = UntrimmedStat(datum)
			UntrimmedStats.append(stat)
		elif datum[0] == 't':
			stat = TrimmedStat(datum)
			TrimmedStats.append(stat)

	return (TrimmedStats, UntrimmedStats)

def makeErrorRateBoxPlot(stats, test):
	corrErrorRates = []
	uncorrErrorRates = []

	# Collect the data from the stats list
	for read in stats:
		corrErrorRate = read.getCorrErrorRate()
		corrErrorRates.append(corrErrorRate)
		uncorrErrorRate = read.getUncorrErrorRate()
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
	savePath = "%s/%s_error_rate_boxplot.png" % (dir,test)
	fig.savefig(savePath, bbox_inches='tight')

def makeErrorRateBarGraph(stats, test):
	corrErrorRates = [] 
	uncorrErrorRates = [] 

	# Collect the data from the stats list
	for read in stats:
		corrLength = read.getCorrLength()
		corrErrorRate = read.getCorrErrorRate()
		corrDataPoint = (corrLength,corrErrorRate)
		corrErrorRates.append(corrDataPoint)

		uncorrLength = read.getUncorrLength()
		uncorrErrorRate = read.getUncorrErrorRate()
		uncorrDataPoint = (uncorrLength,uncorrErrorRate)
		uncorrErrorRates.append(uncorrDataPoint)

	corrErrorRates = np.asmatrix(corrErrorRates)
	uncorrErrorRates = np.asmatrix(uncorrErrorRates)

	# Save the figure
	savePath = "%s/%s_error_rate_bargraph.png" % (dir,test)
	fig.savefig(savePath, bbox_inches='tight')

# agg backend is used to create plot as a .png file
mpl.use('agg')
