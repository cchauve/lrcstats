import sys
import argparse
import datetime

def createBlankConfig():
	'''
	Creates a blank configuration file in the current directory.
	'''
	config ="[paths]\n" \
		"# For each path, don't include the leading \ please!\n" \
		"\n" \
		"# Absolute path to LRCStats dir\n" \
		"lrcstats = \n" \
		"\n" \
		"# Directories of read simulator programs\n" \
		"art = \n" \
		"simlord = \n" \
		"\n" \
		"# Directories of correction tools and dependencies\n" \
		"proovread = \n" \
		"colormap = \n" \
		"lordec = \n" \
		"karect = \n" \
		"brownie = \n" \
		"jabba = \n" \
		"\n" \
		"# Directory to store read data\n" \
		"data = \n"
	blankConfigPath = "blank.config"
	with open(blankConfigPath,'w') as file:
		file.write(config)	

def readConfig(configPath):
	'''
	Reads a configuration file and outputs a dict of paths
	to the necessary programs.
	''' 
	with open(configPath, 'r') as config:
		paths = {}
		for line in config:
			tokens = line.split()
			# hashtags are comments
			if line[0] != "#" and len(tokens) == 3:
				key = tokens[0]
				path = tokens[2]
				paths[key] = path				
	return paths

def readConfig_test(testPath):
	paths = readConfig(testPath)
	for key in paths:
		print "%s = %s" % (key, paths[key])
	
MAJOR_VERSION = 1
MINOR_VERSION = 0

# Command line arguments go here.
parser = argparse.ArgumentParser(description='''
	Long Read Correction Stats (LRCStats) PBS script generator,
	Version %d.%d
	''' % (MAJOR_VERSION, MINOR_VERSION))

parser.add_argument('-c', '--config', metavar='PATH', type=str, help="path to the configuration file")
parser.add_argument('-b', '--blank_config', action='store_true', help=
	"""
	create a new blank configuration file in the current directory 
	to construct your own testing pipeline and exit the program
	""")

args = parser.parse_args()

if args.blank_config:
	print("Creating a new configuration file..")
	createBlankConfig()
