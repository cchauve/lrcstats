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

	keys = [corrReadLength_k,
		uncorrReadLength_k,
		corrAlignmentLength_k,
		uncorrAlignmentLength_k,
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
		assert len(data) == 11 or len(data) == 15

		for i in range(1, len(data)):
			self.data[ ReadDatum.keys[i-1] ] = int(data[i])

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
		length = self.data[ReadDatum.corrAlignmentLength_k]

		return mutations/length

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

		mutations = uDel + uIns + uSub
		length = self.data[ReadDatum.uncorrAlignmentLength_k]

		return mutations/length

	def getUncorrErrors(self):
		'''
		Returns the number of erroreneous bases in the uncorrected
		long read.
		'''
		uDel = self.data[ReadDatum.uncorrDel_k]
		uIns = self.data[ReadDatum.uncorrIns_k]
		uSub = self.data[ReadDatum.uncorrSub_k]
		return uDel + uIns + uSub

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
