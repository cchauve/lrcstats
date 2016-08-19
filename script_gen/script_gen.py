import argparse
import sys
import simulate

def createBlankConfig():
	'''
	Creates a blank configuration file in the current directory.
	'''
	config ="[variables]\n" \
		"# For each path, don't include the leading \ please!\n" \
		"\n" \
		"# Absolute path to LRCStats dir\n" \
		"lrcstats = \n" \
		"\n" \
		"# Path to the read simulator programs\n" \
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
		"data = \n" \
		"\n" \
		"# File names of the real PacBio read FASTQ files for\n" \
		"# E.coli, yeast and fly\n" \
		"yeast_fastq = \n" \
		"ecoli_fastq = \n" \
		"fly_fastq = \n" \
		"\n" \
		"# Your email address to send PBS job info to\n" \
		"email = \n"

	blankConfigPath = "blank.config"
	with open(blankConfigPath,'w') as file:
		file.write(config)	

def readConfig(configPath):
	'''
	Reads a configuration file and outputs a dict of user variables
	to the necessary programs.
	''' 
	with open(configPath, 'r') as config:
		variables = {}
		for line in config:
			tokens = line.split()
			# hashtags are comments
			if len(tokens) == 3 and line[0] != "#":
				key = tokens[0]
				path = tokens[2]
				variables[key] = path				
	return variables

MAJOR_VERSION = 1
MINOR_VERSION = 0

# Command line arguments go here.
parser = argparse.ArgumentParser(description='''
	Long Read Correction Stats (LRCStats) PBS script generator,
	Version %d.%d
	''' % (MAJOR_VERSION, MINOR_VERSION))

parser.add_argument('-b', '--blank_config', action='store_true', help=
	"""
	create a new blank configuration file in the current directory 
	to construct your own testing pipeline and exit the program
	""")

requiredNamed = parser.add_argument_group('required named arguments')
requiredNamed.add_argument('-c', '--config', metavar='CONFIG', type=str, help="path to the configuration file")

args = parser.parse_args()

if args.blank_config:
	createBlankConfig()
	print("Created a new blank configuration file.")
	sys.exit()

if args.config:
	variables = readConfig( args.config )
	print("Read configuration file.")
else:
	print("Error; please provide a configuration file.")
	sys.exit(2) 
