import sys, getopt

def addSpaces(cigar):
	newCigar = ""
	lastWasAlpha = False 
	for i in range( len(cigar) ):
		if not cigar[i].isdigit():
			newCigar = newCigar + " " + cigar[i] + " "
			lastWasAlpha = True
		else:
			newCigar = newCigar + cigar[i] 
	return newCigar

def getCigarList(cigar):
	cigar = cigar.split()

	numOps = []
	ops = []
	for i in range( len(cigar) ):
		if i % 2 == 0:
			numOps.append( int(cigar[i]) )
		else:
			ops.append( cigar[i] )

	assert len(numOps) == len(ops)

	cigarList = [] 
	
	for i in range( len(numOps) ):
		for u in range( numOps[i] ):
			cigarList.append(ops[i])	
	return cigarList 

def nextBase(base, flag):
	if (flag == 16):
		if base == "A":
			return "T"
		elif base == "T":
			return "A"
		elif base == "G":
			return "C"
		elif base == "C":
			return "G"
	else:
		return base

def getRefSeq(ref, refPos, cigarList):
	refSeq = ""
	index = 0

	for i in range( len(cigarList) ):
		if cigarList[i] != "I":
			refSeq += ref[refPos+index]
			index += 1
	return refSeq

def getReverse(seq):
	return seq[::-1]

def getRefAlignment(refSeq, refPos, cigarList, flag):

	index = 0
	refAlignment = ""

	for i in range( len(cigarList) ):
		currentOp = cigarList[i]
		if currentOp == "I":
			refAlignment += "-"
		else:
			refAlignment += nextBase( refSeq[index], flag )
			index += 1
	return refAlignment

def getReadAlignment(read, cigarList):
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
	reference = ""
	with open(refPath, 'r') as file:
		for line in file:
			if len(line) > 0 and line[0] != ">":
				reference += line.strip('\n')		
	assert '\n' not in reference
	return reference

def getGaplessLength(seq):
	length = 0
	for i in range( len(seq) ):
		if seq[i] != "-":
			length += 1
	return length

def convert(ref, samPath, mafPath):
	srcSize = len( ref )
	readNumber = 0

	with open(samPath, 'r') as sam:
		with open(mafPath, 'w') as maf:
			for line in sam:
				if len( line ) > 0 and line[0] != "@":
					line = line.split("	")

					flag = int( line[1] )
					start = int( line[3] ) - 1
					cigar = line[5]
					read = line[9]

					cigar = addSpaces(cigar)
					cigarList = getCigarList(cigar)

					refSeq = getRefSeq(ref, start, cigarList)
					if flag == 16:
						refSeq = getReverse(refSeq)

					refAlignment = getRefAlignment(refSeq, start, cigarList, flag)
					readAlignment = getReadAlignment(read, cigarList)
					assert len(refAlignment) == len(readAlignment)

					readSize = getGaplessLength(readAlignment)
					refSize = getGaplessLength(refAlignment) 
					
					if flag == 16:
						strand = "-"
					else:
						strand = "+"
					maf.write("a\n")
					refLine = "s ref %s %s %s %s %s\n" % (start, refSize, strand, srcSize, refAlignment)
					maf.write(refLine)
					readLine = "s read%d %s %s %s %s %s\n" % (readNumber, start, readSize, strand, srcSize, readAlignment)
					maf.write(readLine)
					maf.write("\n")
					readNumber += 1
				
						

helpMessage = ""
usageMessage = "-h -r refpath -s sam path -o maf path"

options = "hr:s:o:"

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

if refPath is None or samPath is None or mafPrefix is None:
	print helpMessage
	print usageMessage
	sys.exit(2)

mafPath = "%s.maf" % (mafPrefix)

ref = getReference(refPath)
convert(ref, samPath, mafPath)
