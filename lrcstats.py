import argparse
# For sys.exit
import sys
# For os.makedirs
import os
from pipeline import simulate
from pipeline import correct
from pipeline import align
from pipeline import stats

def createBlankConfig():
	'''
	Creates a blank configuration file in the current directory.
	'''
	config ="[paths]\n" \
		"# For each path, don't include the ending / please!\n" \
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
		"# Paths to the reference genome FASTA file\n" \
		"yeast_ref = \n" \
		"ecoli_ref = \n" \
		"fly_ref = \n" \
		"\n" \
		"# Paths to the real PacBio read FASTQ files\n" \
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

	# Reminder: experimentName is a global variable
	blankConfigPath = "config/%s.config" % (experimentName)
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

def testParseListString():
	testString = "[proovread,lordec,jabba,colormap,colormap_oea]"
	actualList = ["proovread", "lordec", "jabba", "colormap", "colormap_oea"]
	details = parseListString(testString)

	assert actualList == details

	print("Parse list string passed!")

def readConfig(configPath):
	'''
	Reads a configuration file and outputs a dict of user variables
	to the necessary programs.
	''' 
	paths = {}
	experimentDetails = {} 
	currentSection = None

	with open(configPath, 'r') as config:
		for line in config:
			tokens = line.split()
			# hashtags are comments
			if line[0] != "#":
				if len(tokens) == 1 and tokens[0] == "[paths]":
					currentSection = "paths"

				elif len(tokens) == 1 and tokens[0] == "[experiment_details]":
					currentSection = "experimentDetails"

				elif len(tokens) == 3 and currentSection is "paths":
					key = tokens[0]
					path = tokens[2]
					paths[key] = path				

				elif len(tokens) == 3 and currentSection is "experimentDetails":
					key = tokens[0]
					details = parseListString(tokens[2])
					experimentDetails[key] = details

	configVariables = {"paths": paths, "experimentDetails": experimentDetails}
	return configVariables

def test():
	testParseListString()

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
parser.add_argument('-t', '--stats', action='store_true', help=
	"""
	create stats scripts
	""")
parser.add_argument('-u', '--test', action='store_true', help=
	"""
	perform unit tests for this module
	""")

requiredNamed = parser.add_argument_group('required named arguments')
requiredNamed.add_argument('-i', '--input_config', metavar='CONFIG', type=str, help=
	"""
	path to the configuration file;
	required only if -b is not set
	""")
requiredNamed.add_argument('-n', '--experiment_name', metavar='NAME', type=str, help=
	"""
	name of the experiment; scripts will appear in the folder of this name
	under the directory `scripts`
	""")

args = parser.parse_args()

if args.test:
	test()
	sys.exit()

optsIncomplete = False

if args.experiment_name:
	experimentName = args.experiment_name
else:
	optsIncomplete = True
	print("Error; please provide the name of the experiment")

if optsIncomplete:
	sys.exit(2) 

if args.blank_config:
	createBlankConfig()
	print("Created a new blank configuration file in config folder.")
	sys.exit()

optsIncomplete = False

if args.input_config:
	configPath = args.input_config
	print( "Reading configuration file at %s..." % (configPath) )
	configVariables = readConfig(configPath)
else:
	optsIncomplete = True
	print("Error; please provide a configuration file.")

if optsIncomplete:
	sys.exit(2) 

paths = configVariables["paths"]
experimentDetails = configVariables["experimentDetails"]

# Create the necessary directories under `scripts`
experimentDir = "scripts/%s" % (experimentName)

if not os.path.exists(experimentDir):
	os.makedirs(experimentDir)

for stage in ["simulate", "correct", "align", "stats"]: 
	stageDir = "%s/%s" % (experimentDir, stage)
	if not os.path.exists(stageDir):
		os.makedirs(stageDir)
	for program in experimentDetails["programs"]:
		programDir = "%s/%s" % (stageDir, program)
		if not stage is "simulate" and not os.path.exists(programDir):
			os.makedirs(programDir)

print("Creating PBS job scripts...")

simulations = []
# Make the short and long read simulation scripts
if args.simulate:
	for genome in experimentDetails["genomes"]:
		for shortCov in experimentDetails["short_coverages"]:
			testDetails = {"genome": genome, "experimentName": experimentName, "shortCov": shortCov}
			simulate.simulateArtShortReads(testDetails,paths)		
			simulations.append(testDetails)
		for longCov in experimentDetails["long_coverages"]:
			testDetails = {"genome": genome, "experimentName": experimentName, "longCov": longCov}
			simulate.simulateSimlordLongReads(testDetails,paths)		
			simulations.append(testDetails)

# Find all test cases
tests = []

for program in experimentDetails["programs"]:
	for genome in experimentDetails["genomes"]:
		for shortCov in experimentDetails["short_coverages"]:
			for longCov in experimentDetails["long_coverages"]:
				if int(shortCov) > int(longCov):
					testDetails = {"program": program, "genome": genome, 
							"experimentName": experimentName,
							"shortCov": shortCov, "longCov": longCov}
					tests.append(testDetails)

# Create the rest of the pipeline
for testDetails in tests:
	if args.correct:
		correct.generateCorrectionJob(testDetails,paths)
	if args.align:
		align.generateAlignmentJob(testDetails,paths)
	if args.stats:
		stats.generateStatsJob(testDetails,paths)	

# Create shell scripts to submit all jobs at once
print("Creating quick-qsub scripts...")

if args.simulate:
	simulate.createQuickQsubScript(simulations, paths, experimentName)
if args.correct:
	correct.createQuickQsubScript(tests, paths, experimentName)
if args.align:
	align.createQuickQsubScript(tests, paths, experimentName)
if args.stats:
	stats.createQuickQsubScript(tests, paths, experimentName)	

print("PBS job scripts are ready - they can be found under `scripts/%s`." % (experimentName))
