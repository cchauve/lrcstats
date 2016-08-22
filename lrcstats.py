import argparse
import sys
from script_gen import * 

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
		"# Path to the read simulator programs\n" \
		"art = \n" \
		"simlord = \n" \
		"\n" \
		"# Path to the correction tools and dependencies\n" \
		"proovread = \n" \
		"colormap = \n" \
		"colormap_oea = \n" \
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
		"email = \n" \
		"\n" \
		"[experiment_details]\n" \
		"# No spaces in between items in list please\n" \
		"# i.e. in the form [item_1,...,item_n]\n" \
		"genomes = [fly,yeast,ecoli,human]\n" \
		"short_coverages = []\n" \
		"long_coverages = []\n" \
		"programs = []\n" 

	blankConfigPath = "blank.config"
	with open(blankConfigPath,'w') as file:
		file.write(config)	

def parseListString(list_string):
	'''
	Given a string of the form "[item_1,...,item_n]",
	returns a list of the form ["item_1", ... , "item_n"] 
	'''
	# Get rid of the braces

	# Reverse the string
	list_string = list_string[::-1]

	# Get rid of the first left brace
	list_string = list_string.rstrip("[")

	# Unreverse the string
	list_string = list_string[::-1]

	# Get rid of the last brace
	list_string = list_string.rstrip("]")

	# Split that string
	detail_list = list_string.split(",")

	return detail_list
def readConfig(configPath):
	'''
	Reads a configuration file and outputs a dict of user variables
	to the necessary programs.
	''' 
	paths = {}
	experiment_details = {} 
	with open(configPath, 'r') as config:
		for line in config:
			tokens = line.split()
			# hashtags are comments
			if line[0] != "#":
				if len(tokens) == 1 and line[0] == "[variables]":
					currentSection = "variables"
				elif len(tokens) == 1 and line[0] == "[experiment_details]":
					currentSection = "experiment_details"
				elif len(tokens) == 3 and currentSection is "variables":
					key = tokens[0]
					path = tokens[2]
					paths[key] = path				
				elif len(tokens) == 3 and currentSection is "experiment_details":
					key = tokens[0]
					detail_list = parseListString(tokens[2])
					experiment_details[key] = detail_list

	configVariables = {"paths": paths, "experiment_details": experiment_details}
	return configVariables

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
parser.add_argument('-s', '--simulate', action='store_true', help=
	"""
	create read simulation scripts
	""")
parser.add_argument('-c', '--correct', action='store_true', help=
	"""
	create correction job scripts
	""")
parser.add_argument('-a', '--align', action='store_true', help=
	"""
	create three-way alignment scripts
	""") 
parser.add_argument('-s', '--stats', action='store_true', help=
	"""
	create stats scripts
	""")

requiredNamed = parser.add_argument_group('required named arguments')
requiredNamed.add_argument('-i', '--input_config', metavar='CONFIG', type=str, help="path to the configuration file")

args = parser.parse_args()

if args.blank_config:
	createBlankConfig()
	print("Created a new blank configuration file in script_gen folder.")
	sys.exit()

if args.input_config:
	configVariables = readConfig( args.input_config )
	print("Read configuration file.")
else:
	print("Error; please provide a configuration file.")
	sys.exit(2) 

experiment_details = configVariables["experiment_details"]
paths = configVariables["paths"]

for program in experiment_details["programs"]:
	for genome in experiment_details["genomes"]:
		for short_coverage in experiment_details["short_coverages"]:
			for long_coverage in experiment_details["long_coverages"]:
				test_details = {"program": program, "genome": genome, \
						"short_coverage": short_coverage, \
						"long_coverage": long_coverage}
				if args.simulate:
					stats.generateStatsJob(test_details) 
