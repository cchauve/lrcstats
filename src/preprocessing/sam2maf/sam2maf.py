import sys
import getopt

def getDelimitedCigar(cigar):
	'''
	Returns a space delimited cigar string.
	e.g. "11M3D" -> "11 M 3 D"	
	'''
	newCigar = ""
	for i in range( len(cigar) ):
		# If the current char in the string is not a digit,
		# then it is an operation, so we add a space around it.
		if not cigar[i].isdigit():
			newCigar = newCigar + " " + cigar[i] + " "
		else:
			newCigar = newCigar + cigar[i] 
	return newCigar

def getCigarList(cigar):
	'''
	Returns a list of operations given a space delimited CIGAR string.
	e.g. "3 M 3 D 3 I" -> ['M', 'M', 'M', 'D', 'D', 'D', 'I', 'I', 'I']
	'''
	cigar = cigar.split()

	assert len(cigar) % 2 == 0

	numOps = []
	ops = []

	for i in range( len(cigar) ):
		# Chars at even indices of the CIGAR list are ints
		if i % 2 == 0:
			numOps.append( int(cigar[i]) )
		# Odd are the CIGAR opts
		else:
			ops.append( cigar[i] )

	assert len(numOps) == len(ops)

	cigarList = [] 
	
	# Converts these lists:
	# numOps = [3, 3, 3]
	# ops = ['M', 'D', 'I']
	# Into:
	# ['M', 'M', 'M', 'D', 'D', 'D', 'I', 'I', 'I']
	for i in range( len(numOps) ):
		for u in range( numOps[i] ):
			cigarList.append(ops[i])	
	return cigarList 

def nextBase(base, flag):
	'''
	If flag is 16, then the sequence is question is the reverse
	complement of the original sequence and we return the complement
	of base. Otherwise, just return the original base.
	'''
	complement = { 'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G' }

	if (flag == 16):
		return complement[base]
	else:
		return base

def getRefSeq(ref, refPos, cigarList):
	'''
	Returns the segment of the reference sequence with starting base
	at refPos and length equivalent to the number of non-'I' chars
	in the cigarList.
	'''
	refSeq = ""
	index = 0

	for i in range( len(cigarList) ):
		if cigarList[i] != "I":
			refSeq += ref[refPos+index]
			index += 1
	return refSeq

def getReverse(seq):
	'''
	Returns the reverse of seq.
	'''
	return seq[::-1]

def getRefAlignment(refSeq, cigarList, flag):
	'''
	Given the refSeq, SAM flag and list of CIGAR ops cigarList,
	returns the reference alignment to the long read.
	'''
	refIndex = 0
	refAlignment = ""

	for i in range( len(cigarList) ):
		currentOp = cigarList[i]
		if currentOp == "I":
			refAlignment += "-"
		else:
			refAlignment += nextBase( refSeq[refIndex], flag )
			# We only increment the refIndex if the current cigar OP is not an
			# insertion
			refIndex += 1
	return refAlignment

def getReadAlignment(read, cigarList):
	'''
	Given the read and the CIGAR list, returns the alignment
	of the read to the reference sequence.
	'''
	readAlignment = ""
	index = 0

	for i in range( len(cigarList) ):
		currentOp = cigarList[i]
		if currentOp == "D":
			readAlignment += "-"
		else:
			readAlignment += read[index]
			index += 1

	return readAlignment

def getReference(refPath):
	'''
	Retrieve the reference genome from refPath
	'''
	reference = ""
	with open(refPath, 'r') as file:
		for line in file:
			if len(line) > 0 and line[0] != ">":
				reference += line.strip('\n')		
	assert '\n' not in reference
	assert '>' not in reference
	return reference

def getGaplessLength(seq):
	'''
	Returns the number of non-'-' bases in the seq
	'''
	length = 0
	for i in range( len(seq) ):
		if seq[i] != "-":
			length += 1
	return length

def convert(ref, samPath, mafPath):
	'''
	Converts the SAM file into a MAF file.
	'''
	srcSize = len( ref )
	readNumber = 0

	with open(samPath, 'r') as sam:
		with open(mafPath, 'w') as maf:
			for line in sam:
				if len( line ) > 0 and line[0] != "@":
					line = line.split("	")

					# Get relevant info from the SAM file for that particular read
					flag = int( line[1] )
					start = int( line[3] ) - 1
					cigar = line[5]
					read = line[9]

					# Get the list of CIGAR ops
					cigar = getDelimitedCigar(cigar)
					cigarList = getCigarList(cigar)

					# get the reference sequence from the reference genome
					refSeq = getRefSeq(ref, start, cigarList)

					if flag == 16:
						read = getReverse(read)

					refAlignment = getRefAlignment(refSeq, start, cigarList, flag)
					readAlignment = getReadAlignment(read, cigarList)
					assert len(refAlignment) == len(readAlignment)

					readSize = getGaplessLength(readAlignment)
					refSize = getGaplessLength(refAlignment) 
					
					if flag == 16:
						readAlignment = getReverse(readAlignment)
						refAlignment = getReverse(refAlignment)		
						strand = "-"
					else:
						strand = "+"
					maf.write("a\n")
					refLine = "s ref %s %s %s %s %s\n" % (start, refSize, strand, srcSize, refAlignment)
					maf.write(refLine)
					readLine = "s %d %s %s %s %s %s\n" % (readNumber, start, readSize, strand, srcSize, readAlignment)
					maf.write(readLine)
					maf.write("\n")
					readNumber += 1

def unitTest():
	'''
	Unit test for this script.
	'''
	print "Testing module..."

	# Test delimitCigar module
	cigar = "10I1=1M2X3D"				
	actualDelimitCigar = "10 I 1 = 1 M 2 X 3 D "						
	delimitCigar = getDelimitedCigar(cigar) 

	assert actualDelimitCigar == delimitCigar

	actualCigarList = []

	for i in range(10):
		actualCigarList.append('I')

	for i in range(1):
		actualCigarList.append('=')

	for i in range(1):
		actualCigarList.append('M')

	for i in range(2):
		actualCigarList.append('X')

	for i in range(3):
		actualCigarList.append('D')

	cigarList = getCigarList(delimitCigar) 

	assert cigarList == actualCigarList

	bases = ['A', 'C', 'G', 'T']
	complements = ['T', 'G', 'C', 'A']	
	flags = [0, 16]

	for flag in flags:
		for i in range( len(bases) ):
			if flag == 0:
				assert nextBase(bases[i], flag) == bases[i]
			else:
				assert nextBase(bases[i], flag) == complements[i]

	print "All tests passed!"

helpMessage = ("Converts SAM file to Multiple Alignment Format.\n"
		+ "Behavior only defined for CIGAR ops 'D', '=', 'I', 'M', or 'X'")
usageMessage = "[-h help and usage] [-r <path to the reference FASTA file>] [-s <path to the SAM file>] [-o <MAF output path>]"

options = "hr:s:o:t"

try:
	opts, args = getopt.getopt(sys.argv[1:], options)
except getopt.GetoptError:
	print "Error: unable to read command line arguments."
	sys.exit(2)

if len(sys.argv) == 1:
	print usageMessage
	sys.exit()

refPath = None
samPath = None
mafPrefix = None

for opt, arg in opts:
	if opt == '-h':
		print helpMessage
		print usageMessage
		sys.exit()
	elif opt == '-r':
		refPath = arg
	elif opt == '-s':
		samPath = arg
	elif opt == '-o':
		mafPrefix = arg
	elif opt == '-t':
		unitTest()
		sys.exit()

if refPath is None or samPath is None or mafPrefix is None:
	print helpMessage
	print usageMessage
	sys.exit(2)

mafPath = "%s.maf" % (mafPrefix)

ref = getReference(refPath)
convert(ref, samPath, mafPath)
