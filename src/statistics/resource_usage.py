import os, sys, getopt

def gatherResourceUsage(dirPath):
	'''
	Given the path to a directory, gather resource usage statistics from all PBS epilogue files contained
	in the directory.
	Input
	- (string) dirPath: the system path to the directory in question
	Returns
	- (dict of dicts) resourceUsages: given the test name, returns the resource statistics
	'''
	resourceUsages = {}
	return resourceUsages

def writeResourceStats(outputPath, resourceUsages)
	'''
	Write the resource usage statistics to a file to be analyzed by process_stats.py
	Input
	- (string) outputPath: system path to the output file
	- (dict of dicts) resourceUsages: given the test name, returns the resource usage stats
	Returns
	- None
	'''
	return

helpMessage = "Given the path to a directory, gather all resource usage statistics from PBS epilogue files."
usageMessage = "Usage: %s [-h help and usage] [-d output directory] [-o output path]" % (sys.argv[0])
options = "hd:o:"

try:
	opts, args = getopt.getopt(sys.argv[1:], options)
except getopt.GetoptError:
	print "Error: unable to read command line arguments."
	sys.exit(2)

if len(sys.argv) == 1:
	print usageMessage
	sys.exit(2)

dirPath = None
outputPath = None

for opt, arg in opts:
	if opt == '-h':
		print helpMessage
		print usageMessage
		sys.exit()
	elif opt == '-d':
		dirPath = arg
	elif opt == '-o':
		outputPath = arg

if dirPath is None:
	print "Please provide the path to the directory."
	optsIncomplete = True
if outputPath is None:
	print "Please provide the path to the output file."
	optsIncomplete = True

if optsIncomplete:
	print usageMessage
	sys.exit(2)
	
resourceUsages = gatherResourceUsage(dirPath)
writeSummary(outputPath, resourceUsages)
