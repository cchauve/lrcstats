import sys
import getopt
import re

class Alignment(object):
	'''
	Takes as input lines from a MAF file and computes a new alignment for
	unextended regions of the reads only.
	'''
	def __init__(self, refLine, uReadLine, cReadLine):
		'''
		Inputs
		- (list of strings) refLine: directly from MAF file
		- (list of strings) uReadLine: ditto
		- (list of strings) cReadLine: ditto
		'''	
		self.strand = refLine[4]
		self.srcSize = int(refLine[5])
		ref = refLine[6]
		
		readName = uReadLine[1]
		self.readNumber = int( re.findall('(\d+)', readName)[readNumberIndex_g] )
		uRead = uReadLine[6]

		cRead = cReadLine[6]

		assert len(cRead) == len(uRead)

		# Used to update the starting point where the reads align in the
		# reference
		lengthBeforeRemoval = len(ref)

		# First remove extended prefixes by reversing the strings
		ref, uRead, cRead = self.reverseReads(ref, uRead, cRead)
		ref, uRead, cRead = self.removeExtendedSuffix(ref, uRead, cRead)

		# Reverse the string to get it back to normal 
		ref, uRead, cRead = self.reverseReads(ref, uRead, cRead)

		# Update the starting point where the reads align in the reference
		lengthAfterRemoval = len(ref)
		difference = lengthBeforeRemoval - lengthAfterRemoval
		oldStart = int(refLine[2])	
		self.start = oldStart + difference

		# Remove extended suffix of ref, uRead and cRead and store result
		self.ref, self.uRead, self.cRead = self.removeExtendedSuffix(ref, uRead, cRead)

	def getReadNumber(self):
		'''
		Returns the read number of the alignments.
		'''
		return self.readNumber

	def getStrand(self):
		'''
		Returns '+' or '-' to indicate whether the alignment 
		is to the original ('+') or reverse-complemented ('-') source
		'''
		return self.strand

	def getSrcSize(self):
		'''
		Returns the size of the original reference genome.
		'''
		return self.srcSize

	def getStart(self):
		'''
		Returns the start of the aligning region in the source sequence.
		'''
		return self.start

	def getRefSize(self):
		'''
		Returns the number of non-'-' characters in the reference alignment
		'''
		return self.sizeOfSequence(self.ref)

	def getUncorrectedSize(self):
		'''
		Returns the number of non-'-' characters in the uncorrected alignment
		'''
		return self.sizeOfSequence(self.uRead)

	def getCorrectedSize(self):
		'''
		Returns the number of non-'-' characters in the corrected alignment
		'''
		return self.sizeOfSequence(self.uRead)

	def getRef(self):
		'''
		Get the truncated reference alignment with extended prefix and suffix removed.
		'''
		return self.ref

	def getUncorrectedRead(self):
		'''
		Get the truncated uncorrected read alignment with extended prefix and suffix removed.
		'''
		return self.uRead

	def getCorrectedRead(self):	
		'''
		Get the truncated corrected read alignment with extended prefix and suffix removed.
		'''
		return self.cRead

	def removeExtendedSuffix(self, ref, uRead, cRead): 
		# Trim off trailing '-'
		lengthBeforeStrip = len(ref)

		ref = ref.rstrip('-')
		lengthAfterStrip = len(ref)

		lengthDifference = lengthBeforeStrip - lengthAfterStrip
		
		newEndIndex = len(cRead) - lengthDifference

		extendedSegment = cRead[newEndIndex:]
		cRead = cRead[0:newEndIndex]
		uRead = uRead[0:newEndIndex]

		if self.isInMiddleOfTrimmedRead(cRead):
			ref += '-'
			uRead += 'X'
			cRead += 'X'

		return ref, uRead, cRead

	def reverseReads(self, ref, uRead, cRead):
		# Reverse the reads
		ref = ref[::-1]
		uRead = uRead[::-1]
		cRead = cRead[::-1]
		return ref, uRead, cRead

	def sizeOfSequence(self, read):
		# Returns the number of all non-'-' or 'X' characters in read
		read = read.replace('-', '')
		read = read.replace('X', '')
		return len(read)

	def isInMiddleOfTrimmedRead(self, read):
		# Returns whether the extended sequence is in the middle of
		# a trimmed read in the corrected long read alignment
		numX = read.count('X')
		if numX % 2 == 0:
			return False
		else:
			return True

def readInput(mafInputPath):
	'''
	Read and store the alignments from the three-way MAF file.
	Input
	- (string) mafInputPath: the path to the three-way MAF file generated by lrcstats
	Output
	- (list of Alignment objects) alignments
	'''
	with open(mafInputPath, 'r') as file:
		alignments = []
		refLine = None
		uReadLine = None
		cReadLine = None
		for line in file:
			line = line.split()
			if len(line) > 0 and line[0] != "#" and line[0] != "track":
				# Indicates start of read
				if line[0] == 'a':
					refLine = None
					uReadLine = None
					cReadLine = None

				elif refLine is None:
					refLine = line

				elif uReadLine is None:
					uReadLine = line

				elif cReadLine is None:
					cReadLine = line
					alignment = Alignment(refLine, uReadLine, cReadLine)
					alignments.append( alignment )
	assert len(alignments) > 0
	return alignments

def writeUnextended(outputPath, alignments):
	'''
	Write the unextended alignments into new MAF file
	Inputs
	- (string) outputPath: absolute path to the output file
	- (list of Alignment objects): contains the unextended alignments
	'''	
	assert len(alignments) > 0

	with open(outputPath,'w') as file:
		file.write("##maf version=1\n\n\n\n")
		for alignment in alignments:
			file.write("a\n")
			
			readNumber = alignment.getReadNumber()
			start = alignment.getStart()	
			strand = alignment.getStrand()
			srcSize = alignment.getSrcSize()

			refSrc = "%d.reference" % (readNumber)
			refSize = alignment.getRefSize()
			ref = alignment.getRef()

			refLine = "s %s %d %d %s %d %s\n" % (refSrc, start, refSize, strand, srcSize, ref) 
			file.write(refLine)
			
			uReadSrc = "%d.uncorrected" % (readNumber)
			uReadSize = alignment.getUncorrectedSize()
			uRead = alignment.getUncorrectedRead()
			# Since the long read is considered to be the "source" of the alignment
			start = 0
			srcSize = uReadSize

			uReadLine = "s %s %d %d %s %d %s\n" % (uReadSrc, start, uReadSize, strand, srcSize, uRead) 
			file.write(uReadLine)

			cReadSrc = "%d.corrected" % (readNumber)
			cReadSize = alignment.getCorrectedSize()
			cRead = alignment.getCorrectedRead()
			# Since the long read is considered to be the "source" of the alignment
			srcSize = cReadSize

			cReadLine = "s %s %d %d %s %d %s\n" % (cReadSrc, start, cReadSize, strand, srcSize, cRead) 
			file.write(cReadLine)
			file.write('\n')

def test():
	testInputPath = "test_in.maf"
	print "Writing MAF test file..."
	with open(testInputPath, 'w') as file:
		for i in range(2):
			file.write('a\n')

			refLine = "s 1.reference 10 4 + 1000000 ----ACGA----\n"
			file.write(refLine)

			uReadLine = "s 1.uncorrected 0 4 + 4 ----ACGA----\n"
			file.write(uReadLine) 

			cReadLine = "s 1.corrected 0 12 + 12 XXXXACGAXXXX\n"
			file.write(cReadLine)
			file.write('\n')

		file.write('a\n')

		refLine = "s 1.reference 10 4 + 1000000 ACGA----\n"
		file.write(refLine)

		uReadLine = "s 1.uncorrected 0 4 + 4 ACGA----\n"
		file.write(uReadLine) 

		cReadLine = "s 1.corrected 0 8 + 8 ACGAXXXX\n"
		file.write(cReadLine)
		file.write('\n')

		file.write('a\n')

		refLine = "s 1.reference 10 4 + 1000000 ----ACGA\n"
		file.write(refLine)

		uReadLine = "s 1.uncorrected 0 4 + 4 ----ACGA\n"
		file.write(uReadLine) 

		cReadLine = "s 1.corrected 0 8 + 8 XXXXACGA\n"
		file.write(cReadLine)
		file.write('\n')

	print "Reading MAF test file and processing alignments..."
	alignments = readInput(testInputPath) 
	testOutputPath = "test_out.maf"
	print "Writing output file..."
	writeUnextended(testOutputPath, alignments)
	print "Test complete! Please check the input and output to ensure correctness."

# Global variable
readNumberIndex_g = 0

helpMessage = "Reads three-way alignment MAF files and outputs another three-way MAF file without extended segments on reads and a second MAF file with only alignment between the reference and the extended segment of the read."
usageMessage = "[-h help and usage] [-i three-way MAF file] [-m unextended MAF output path] [-p used PBSim]"

options = "hi:m:pt"

try:
	opts, args = getopt.getopt(sys.argv[1:], options)
except getopt.GetoptError:
	print "Error: unable to read command line arguments."
	sys.exit(2)

if len(sys.argv) == 1:
	print usageMessage
	sys.exit(2)

mafInputPath = None
#refPath = None
unextendedPath = None
#extensionPath = None
usedPbsim = False

for opt, arg in opts:
	if opt == '-h':
		print helpMessage
		print usageMessage
		sys.exit()
	elif opt == '-i':
		mafInputPath = arg
	elif opt == '-m':
		unextendedPath = arg
	elif opt == '-p':
		usedPbsim = True
	elif opt == '-t':
		test()
		sys.exit()

if usedPbsim:
	readNumberIndex_g = 1

if mafInputPath is None or unextendedPath is None:
	print "Missing argument - please double check your command."
	sys.exit(2)

print "Reading file and unextending alignments..."
alignments = readInput( mafInputPath )
print "Writing output file..."
writeUnextended(unextendedPath, alignments)
