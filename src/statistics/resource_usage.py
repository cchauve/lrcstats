import os
import sys
import getopt
import re

def findSummaryFiles(dirPath):
	'''
	Returns a list of paths to all files in the directory at dirPath that
	end with .out i.e. job summary files
	Input
	- (string) dirPath: the system path to the directory in question
	Returns
	- (list of strings) outFiles: list of all paths to job summary files
	'''
	outFiles = []
	for root, dirs, files in os.walk(dirPath):
		for file in files:
			if file.endswith(".out"):
				path = os.path.join(root, file)
				outFiles.append(path)	
	return outFiles

def extractResourceUsage(outFiles):
	'''
	Returns a dictionary containing the resource usage for every test case described
	by the files in outFiles.
	Input
	- (list of strings) outFiles: the paths to all the job summary files in the directory
	Returns
	- (dict of dicts of strings) resourceUsages: the resource usage for each test
	'''
	resourceUsages = {}
	for path in outFiles:
		test = os.path.basename(path)
		with open(path,'r') as file:
			for line in file:
				line = line.split()
				if len(line) > 1 and line[0] == "Resources" and line[1] == "Used:":
					resourceTokens = line[2].split(',')
					cput = resourceTokens[0]
					mem = resourceTokens[1]
					vmem = resourceTokens[2]
					walltime = resourceTokens[3]
					resources = { cput_k : cput, mem_k : mem, vmem_k : vmem, walltime_k : walltime }
					resourceUsages[test] = resources
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
	with open(outputPath,'w') as file:
		header = "Test cput mem vmem walltime\n"
		file.write(header)
		for test in resourceUsages:
			resources = resourceUsages[test]
			cput = resources[cput_k]
			mem = resources[mem_k]
			vmem = resources[vmem_k]
			walltime = resouces[walltime_k]
			line = "%s %s %s %s %s\n" % (test, cput, mem, vmem, walltime)
			file.write(line)

# Global variables
cput_k = "CPU TIME"
mem_k = "PEAK PHYSICAL MEMORY USAGE"
vmem_k = "PEAK VIRTUAL MEMORY USAGE"
walltime_k = "WALLTIME"

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
	
outFiles = findSummaryFiles(dirPath)
resourceUsages = gatherResourceUsage(outFiles)
writeSummary(outputPath, resourceUsages)
