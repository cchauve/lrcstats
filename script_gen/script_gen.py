import sys
import argparse
import datetime

def createBlankConfig():
	'''
	Creates a blank configuration file in the current directory.
	'''
	config ="[path]\n" \
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
