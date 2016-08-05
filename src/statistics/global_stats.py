from __future__ import division
import data
import sys
import getopt

def collectStatistics(trimmedData):
	'''
	Collect statistics from data.
	Inputs
	- (list of TrimmedDatum objects) trimmedData: contains the data
	Outputs
	- (dict of ints) statistics: contains the statistics
	'''
	statistics = {correctedBases_k : 0,
			correctedDeletions_k : 0,
			correctedInsertions_k : 0,
			correctedSubstitutions_k : 0,
			uncorrectedBases_k : 0,
			uncorrectedDeletions_k : 0,
			uncorrectedInsertions_k : 0,
			uncorrectedSubstitutions_k : 0}	
			
	for datum in trimmedData:
		# Corrected read statistics
		statistics[correctedBases_k] += datum.getCorrLength()
		statistics[correctedDeletions_k] += datum.getCorrDel()
		statistics[correctedInsertions_k] += datum.getCorrIns()
		statistics[correctedSubstitutions_k] += datum.getCorrSub()
		# Uncorrected read statistics
		statistics[uncorrectedBases_k] += datum.getUncorrLength()
		statistics[uncorrectedDeletions_k] += datum.getUncorrDel()
		statistics[uncorrectedInsertions_k] += datum.getUncorrIns()
		statistics[uncorrectedSubstitutions_k] += datum.getUncorrSub()		

	return statistics

def writeStatisticsSummary(outputPath, trimmedStatistics, untrimmedStatistics, doBoth):
	'''
	Write the summary of the statistics into a text file.
	Inputs
	- (string) outputPath: the path to save file
	- (dict of ints) statistics: contains the statistics
	'''
	# Trimmed read statistics
	# Get the corrected read statistics
	correctedThroughputTrimmed = trimmedStatistics[correctedBases_k]
	correctedMutationsTrimmed = trimmedStatistics[correctedDeletions_k] + trimmedStatistics[correctedInsertions_k] + trimmedStatistics[correctedSubstitutions_k]
	correctedTruePositivesTrimmed = correctedThroughputTrimmed - correctedMutationsTrimmed
	correctedErrorRateTrimmed = correctedMutationsTrimmed/correctedThroughputTrimmed

	# Get the uncorrected read statistics
	uncorrectedThroughputTrimmed = trimmedStatistics[uncorrectedBases_k]
	uncorrectedMutationsTrimmed = trimmedStatistics[uncorrectedDeletions_k] + trimmedStatistics[uncorrectedInsertions_k] + trimmedStatistics[uncorrectedSubstitutions_k]
	uncorrectedTruePositivesTrimmed = uncorrectedThroughputTrimmed - uncorrectedMutationsTrimmed
	uncorrectedErrorRateTrimmed = uncorrectedMutationsTrimmed/uncorrectedThroughputTrimmed

	if doBoth:
		# Untrimmed statistics
		# Get the corrected read statistics
		correctedThroughputUntrimmed = untrimmedStatistics[correctedBases_k]
		correctedMutationsUntrimmed = untrimmedStatistics[correctedDeletions_k] + untrimmedStatistics[correctedInsertions_k] + untrimmedStatistics[correctedSubstitutions_k]
		correctedTruePositivesUntrimmed = correctedThroughputUntrimmed - correctedMutationsUntrimmed
		correctedErrorRateUntrimmed = correctedMutationsUntrimmed/correctedThroughputUntrimmed

	# Get the uncorrected read statistics
		uncorrectedThroughputUntrimmed = untrimmedStatistics[uncorrectedBases_k]
		uncorrectedMutationsUntrimmed = untrimmedStatistics[uncorrectedDeletions_k] + untrimmedStatistics[uncorrectedInsertions_k] + untrimmedStatistics[uncorrectedSubstitutions_k]
		uncorrectedTruePositivesUntrimmed = uncorrectedThroughputUntrimmed - uncorrectedMutationsUntrimmed
		uncorrectedErrorRateUntrimmed = uncorrectedMutationsUntrimmed/uncorrectedThroughputUntrimmed

	with open(outputPath, 'w') as file:
		header = "            Error Rate   Throughput   Correct   Incorrect   Deletions   Insertions   Substitutions\n"
		file.write(header)

		correctedLine = "Corrected - trimmed   %f %d %d %d %d %d %d\n" \
				% (correctedErrorRateTrimmed, correctedThroughputTrimmed, correctedTruePositivesTrimmed, 
					correctedMutationsTrimmed, trimmedStatistics[correctedDeletions_k], trimmedStatistics[correctedInsertions_k], trimmedStatistics[correctedSubstitutions_k])	
		file.write(correctedLine)

		uncorrectedLine = "Uncorrected - trimmed %f %d %d %d %d %d %d\n" \
				% (uncorrectedErrorRateTrimmed, uncorrectedThroughputTrimmed, uncorrectedTruePositivesTrimmed, 
					uncorrectedMutationsTrimmed, trimmedStatistics[uncorrectedDeletions_k], 
					trimmedStatistics[uncorrectedInsertions_k], trimmedStatistics[uncorrectedSubstitutions_k])	
		file.write(uncorrectedLine)

		if doBoth:
			correctedLine = "Corrected - untrimmed   %f %d %d %d %d %d %d\n" \
				% (correctedErrorRateUntrimmed, correctedThroughputUntrimmed, correctedTruePositivesUntrimmed, 
					correctedMutationsUntrimmed, untrimmedStatistics[correctedDeletions_k], 
					untrimmedStatistics[correctedInsertions_k], 
					untrimmedStatistics[correctedSubstitutions_k])	
			file.write(correctedLine)

			uncorrectedLine = "Uncorrected - untrimmed %f %d %d %d %d %d %d\n" \
				% (uncorrectedErrorRateUntrimmed, uncorrectedThroughputUntrimmed, uncorrectedTruePositivesUntrimmed,
					uncorrectedMutationsUntrimmed, untrimmedStatistics[uncorrectedDeletions_k], 
					untrimmedStatistics[uncorrectedInsertions_k], 
					untrimmedStatistics[uncorrectedSubstitutions_k])	
			file.write(uncorrectedLine)

# Global variables for data dict
correctedBases_k = "CORRECTED BASES"
correctedDeletions_k = "CORRECTED DELETIONS"
correctedInsertions_k = "CORRECTED INSERTIONS"
correctedSubstitutions_k = "CORRECTED SUBSTITUTIONS"

uncorrectedBases_k = "UNCORRECTED BASES"
uncorrectedDeletions_k = "UNCORRECTED DELETIONS"
uncorrectedInsertions_k = "UNCORRECTED INSERTIONS"
uncorrectedSubstitutions_k = "UNCORRECTED SUBSTITUTIONS"

helpMessage = "Summarize global long read correction data statistics."
usageMessage = "Usage: %s [-h help and usage] [-i stats file input path] [-b data is untrimmed] [-o output path]" % (sys.argv[0])
options = "hi:o:tb"

try:
	opts, args = getopt.getopt(sys.argv[1:], options)
except getopt.GetoptError:
	print "Error: unable to read command line arguments."
	sys.exit(2)

if len(sys.argv) == 1:
	print usageMessage
	sys.exit(2)

inputPath = None
outputPath = None
testRun = False
doBoth = False

for opt, arg in opts:
	if opt == '-h':
		print helpMessage
		print usageMessage
		sys.exit()
	elif opt == '-i':
		inputPath = arg
	elif opt == '-o':
		outputPath = arg
	elif opt == '-b':
		doBoth = True
	elif opt == '-t':
		testRun = True

optsIncomplete = False

if inputPath is None and not testRun:
	print "Please specify the input path."
	optsIncomplete = True
if outputPath is None:
	print "Please specify the output path."
	optsIncomplete = True

if optsIncomplete:
	print usageMessage
	sys.exit(2)

# We don't use the untrimmedData
trimmedData, untrimmedData = data.retrieveRawData(inputPath)

trimmedStatistics = collectStatistics(trimmedData)
untrimmedStatistics = collectStatistics(untrimmedData)
writeStatisticsSummary(outputPath, trimmedStatistics, untrimmedStatistics, doBoth)
