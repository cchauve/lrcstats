from __future__ import division
import getopt
import sys
import re

helpMessage = "Returns combined error rate given a SimLoRD FASTQ file." 
usageMessage = "Usage: %s [-h help and usage] [-i SimLoRD FASTQ input path]" 
options = "hi:"

try:
	opts, args = getopt.getopt(sys.argv[1:], options)
except getopt.GetoptError:
	print "Error: unable to read command line arguments."
	sys.exit(2)

if len(sys.argv) == 1:
	print usageMessage
	sys.exit(2)

inputPath = None 

for opt, arg in opts:
	if opt == '-h':
		print helpMessage
		print usageMessage
	elif opt == '-i':
		inputPath = arg

if inputPath is None:
	print("Error; please provide a SimLoRD FASTQ file")
	print usageMessage
	sys.exit(2)

totalBases = 0
errorBases = 0
 
with open(inputPath,'r') as file:
	for line in file:
		if len(line) > 4 and line[0:5] == "@Read":
			totalBases += int( re.findall('(\d+)', line)[1] )
			errorBases += int( re.findall('(\d+)', line)[3] )

totalErrorRate = errorBases / totalBases

print("Error rate = %f" % (totalErrorRate))

print("Length = %d" % (totalBases))
print("Errors = %d" % (errorBases))
