import sys
import argparse
import datetime

def createBlankConfig():
	'''
	Creates a blank configuration file in the current directory.
	'''
	config = 
	"""
	# Feed this file into LRCStats (lrcstats.py) to generate all necessary
	# bash/PBS scripts. 
	# This configuration file should be written using shell script syntax.
	# For an example, generate the build-in configuration file.

	[details]
	
	correction_algorithms = []

	[paths]

	# Prefix of the directory that will contain all the data and results of the test
	prefix = 

	# Path to SimLoRD executable
	simlord =

	# Path to ART executable
	art =
	"""

def createBuildInConfig():
	'''
	Creates the build-in configuration file in the current directory.
	'''
	config =
	"""
	# Feed this file into LRCStats (lrcstats.py) to generate all necessary
	# bash/PBS scripts. 

	[details]
	# General details of the experiment.
	
	# Programs used
	correction_algorithms = [proovread, lordec, jabba, colormap]
	long_sim = simlord
	short_sim = art

	# Depth of coverages for short reads
	short_covs = [50, 100, 200]
	
	# Depth of coverages for long reads
	long_covs = [10, 20, 50, 75]

	# Genomes of organisms to be used.
	genomes = [ecoli, yeast, fly]

	[paths]
	# Paths to the executables.

	# Paths to correction algorithms
	proovread = 
	lordec = 
	jabba = 
	colormap =

	# Paths to read simulators 
	simlord =
	art =

	# Path to your local LRCStats build
	lrcstats = 

	# Prefix of the directory that will contain all the data and results of the test
	prefix = 

	[all-resources]
	# Resources to be used for all programs.
	# If you want to specify the resource usage for a specific program, replace 'all'
	# with the name of the program e.g. 'proovread-resources' 
	walltime = 
	num_procs = 
	mem = 
	"""

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
