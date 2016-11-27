class ReadDatum(object):
	# Keys for ReadDatum member variable dictionary
	corrReadLength_k = "CORRECTED READ LENGTH"
	uncorrReadLength_k = "UNCORRECTED READ LENGTH"

	alignmentLength_k = "ALIGNMENT LENGTH"

	corrDel_k = "CORRECTED DELETION"
	corrIns_k = "CORRECTED INSERTION"
	corrSub_k = "CORRECTED SUBSTITUTION"

	uncorrDel_k = "UNCORRECTED DELETION"
	uncorrIns_k = "UNCORRECTED INSERTION"
	uncorrSub_k = "UNCORRECTED SUBSTITUTION"

	keys = [corrReadLength_k,
		uncorrReadLength_k,
		alignmentLength_k,
		corrDel_k,
		corrIns_k,
		corrSub_k,
		uncorrDel_k,
		uncorrIns_k,
		uncorrSub_k
		]
	'''
	Preprocesses and outputs general statistics for reads.
	'''
	def __init__(self, data):
		'''
		Accepts as input list of trimmed read data points obtained
		directly from the STATS file outputted by lrcstats
		'''
		self.data = {}
		# keys is a class variable and contains the keys
		# for the data dictionary in ReadDatum objects.

		# ignore the read ID and read type
		data = data[2:]

		for i in range(0, len(data)):
			self.data[ReadDatum.keys[i]] = int(data[i])

	def getAlignmentLength(self):
		'''
		Returns the length of the alignment
		'''
		return self.data[ReadDatum.alignmentLength_k]

	def getCorrLength(self):
		'''
		Returns the length of the corrected long read.
		'''
		return self.data[ReadDatum.corrReadLength_k]

	def getUncorrLength(self):
		'''
		Returns the length of the corresponding uncorrected long read.
		'''
		uLength = self.data[ReadDatum.uncorrReadLength_k]
		return uLength

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
		if datum[1] == 'u':
			datum = ReadDatum(datum)
			UntrimmedData.append(datum)
		elif datum[1] == 't':
			datum = ReadDatum(datum)
			TrimmedData.append(datum)

	return (TrimmedData, UntrimmedData)
