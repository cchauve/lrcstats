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
		"genomes = [ecoli]\n" \
		"short_coverages = [50,100,200]\n" \
		"long_coverages = [10,20,50,75]\n" \
		"programs = [proovread,lordec,jabba,colormap,colormap_oea]\n" 

	blankConfigPath = "blank.config"
	with open(blankConfigPath,'w') as file:
		file.write(config)	

def parseListString(listString):
	'''
	Given a string of the form "[item_1,...,item_n]",
	returns a list of the form ["item_1", ... , "item_n"] 
	'''
	# Reverse the string
	listString = listString[::-1]

	# Get rid of the first left brace
	listString = listString.rstrip("[")

	# Unreverse the string
	listString = listString[::-1]

	# Get rid of the last brace
	listString = listString.rstrip("]")

	# Split that string
	details = listString.split(",")

	return details
def readConfig(configPath):
	'''
	Reads a configuration file and outputs a dict of user variables
	to the necessary programs.
	''' 
	paths = {}
	experimentDetails = {} 
	with open(configPath, 'r') as config:
		for line in config:
			tokens = line.split()
			# hashtags are comments
			if line[0] != "#":
				if len(tokens) == 1 and line[0] == "[variables]":
					currentSection = "variables"
				elif len(tokens) == 1 and line[0] == "[experiment_details]":
					currentSection = "experimentDetails"
				elif len(tokens) == 3 and currentSection is "variables":
					key = tokens[0]
					path = tokens[2]
					paths[key] = path				
				elif len(tokens) == 3 and currentSection is "experimentDetails":
					key = tokens[0]
					details = parseListString(tokens[2])
					experimentDetails[key] = details

	configVariables = {"paths": paths, "experimentDetails": experimentDetails}
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

experimentDetails = configVariables["experimentDetails"]
paths = configVariables["paths"]

for program in experimentDetails["programs"]:
	for genome in experimentDetails["genomes"]:
		for shortCov in experimentDetails["short_coverages"]:
			for longCov in experimentDetails["long_coverages"]:
				if int(shortCov) > int(longCov):
					testDetails = {"program": program, "genome": genome, \
							"shortCov": shortCov, \
							"longCov": longCov}
					if args.simulate:
						simulate.simulateArtShortReads(testDetails)
						simulate.simulateSimlordLongReads(testDetails)
					if args.correct:
						correct.generateCorrectionJob(testDetails)
					if args.align:
						align.generateAlignmentJob(testDetails)
					if args.stats:
						stats.generateStatsJob(testDetails)	
