import argparse
# For sys.exit
import sys
# For os.makedirs
import os

def createBlankConfig(configPath):
	'''
	Creates a blank configuration file in the current directory.
	'''
	config ="[Experiment Details]\n" \
		"experiment_name = example_name\n" \
		"# Number of threads you'd like to run the aligner with\n" \
		"threads = 1\n" \
		"# true or false\n" \
		"trimmed = false\n" \
		"extended = false\n" \
		"\n" \
		"[Paths]\n" \
		"# Directory to store read data\n" \
		"data = \n" \
		"clr = example.fasta\n" \
		"# Paths to MAF two-way alignment file\n" \
		"maf = example.maf\n" \
		"\n" \
		"[Initialization Commands]\n" \
		"# List shell commands you would like to perform before alignment\n" \
		"# Load python 2.7.2\n" \
		"module load python/2.7.2\n" \
		"# Load g++ 5.1.0\n" \
		"module load gcc/gcc-5.1.0\n" \
		"\n" \
		"[PBS Parameters]\n" \
		"# Enter the PBS Parameters that will appear in the header of the LRCStats job file\n" \
		"# Do not prepend each line with a # character - this will be interpreted as a comment\n" \
		"PBS -M email@domain.com\n" \
		"PBS -m bea\n" \
		"PBS -j oe\n" \
		"PBS -N example_job\n" \
		"PBS -l mem=8gb\n" \
		"PBS -l nodes:1:ppn=1\n" \
		"PBS -l walltime=01:00:00\n"

	blankConfigPath = "%s" % (configPath)
	with open(blankConfigPath,'w') as file:
		file.write(config)

def parseToken(token):
	if token.lower() == "false":
		return False
	elif token.lower() == "true":
		return True
	else:
		return token 

def readConfig(configPath):
	'''
	Reads a configuration file and outputs a dict of user variables
	to the necessary programs.
	''' 
	experimentDetails = { "extended": False, "trimmed": False }
	paths = {}
	initCommands = []
	pbsOptions = []
	currentSection = None

	with open(configPath, 'r') as config:
		for line in config:
			# Remove comments
			line = line.split("#")[0].rstrip()
			if len(line) > 0:
				# check if new section and change section
				if line == "[Paths]":
					currentSection = "paths"
				elif line == "[Initialization Commands]": 
					currentSection = "init"
				elif line == "[PBS Parameters]": 
					currentSection = "pbs"
				elif line == "[Experiment Details]":
					currentSection = "Experiment Details"
				# if not in new section of config file, perform section specific operations
				else:
					if currentSection is "Experiment Details":
						# remove whitespace from line	
						line = line.replace(" ","")
						line = line.replace("	","")
						tokens = line.split("=")
						experimentDetails[tokens[0]] = parseToken(tokens[1])	
					elif currentSection is "paths":
						# remove whitespace from line	
						line = line.replace(" ","")
						line = line.replace("	","")
						tokens = line.split("=")
						# add path to the dict
						paths[tokens[0]] = parseToken(tokens[1])
					elif currentSection is "init":
						initCommands.append( line.rstrip() )
					elif currentSection is "pbs":
						pbsOptions.append( line.rstrip() )

	return experimentDetails, paths, initCommands, pbsOptions

def writeHeader(file, pbsOptions):
	file.write("#!/bin/bash\n")
	for option in pbsOptions:
		line = "# %s\n" %(option)
		file.write(line)
	file.write('\n')

def writeInit(file, initCommands):
	for command in initCommands:
		line = "%s\n" % (command)
		file.write(line) 
	file.write('\n')

def writePaths(file, paths):
	lrcstatsPath = os.path.dirname(os.path.realpath(__file__))
	line = "lrcstats=%s\n" % (lrcstatsPath)
	file.write(line)
	for key in paths:
		line = "%s=%s\n" % (key, paths[key])
		file.write(line)
	file.write('\n')

def writeSort(file):
        '''
        Write the commands to sort FASTA file
        '''
        line = "############### Sort FASTA ###########\n" \
                "echo 'Sorting FASTA file...'\n" \
                "\n" \
                "sortfasta=${lrcstats}/src/preprocessing/sortfasta/sortfasta.py\n" \
                "sortedOutput=${data}/sorted.fasta\n" \
                "\n" \
                "python $sortfasta -i $input -o $sortedOutput\n" \
                "\n" \
                "clr=$sortedOutput\n" \
                "\n" 
        file.write(line)        

def writePrune(file):
        '''
        Write the commands to prune the MAF file
        '''
        line = "############### Prune the maf file(s) ###########\n" \
                "echo 'Pruning MAF file(s)...'\n" \
                "\n" \
                "prunemaf=${lrcstats}/src/preprocessing/prunemaf/prunemaf.py\n" \
                "pruneOutput=${data}/pruned\n" \
                "python $prunemaf -f $input -m $maf -o $pruneOutput\n" \
                "\n" \
                "maf=${pruneOutput}.maf\n" \
                "\n"
        file.write(line)

def writeConcatenateTrimmedReads(file):
        '''
        Write the commands to process trimmed reads.
        '''
        line = "############### Concatenate Trimmed Reads ###########\n" \
                "echo 'Processing trimmed reads...'\n" \
                "concatenate=${lrcstats}/src/preprocessing/concatenate_trimmed/concatenate_trimmed.py\n" \
                "concatenated_output=${data}/concatenated.fasta\n" \
                "\n" \
                "python ${concatenate} -i ${clr} -o ${concatenated_output}\n" \
                "\n" \
                "clr=${concatenated_output}\n" \
                "\n"
        file.write(line)

def writeAlignment(file, trimmed, extended, threads):
        '''
        Write the commands to create a three-way alignment
        between the cLR, uLR and ref
        '''
        line = "############### Generate three-way alignment ###########\n" \
                "echo 'Generating three-way alignment...'\n" \
                "aligner=${lrcstats}/src/aligner/aligner\n" \
                "mafOutput=${data}/${experiment_name}.maf\n" \
                "\n"
        file.write(line)

	if trimmed and extended: 
		command = "$aligner maf -m $maf -c $clr -t -e -o $mafOutput -p %s\n" % (threads)
        elif trimmed:
                command = "$aligner maf -m $maf -c $clr -t -o $mafOutput -p %s\n" % (threads)
        elif extended:
                command = "$aligner maf -m $maf -c $clr -e -o $mafOutput -p %s\n" % (threads)
        else:
                command = "$aligner maf -m $maf -c $clr -o $mafOutput -p %s\n" % (threads)
	file.write(command)
	line = "maf=${mafOutput}\n"
	file.write(line)

def writeRemoveExtensions(file):
	line = "############### Removing extended regions #############\n" \
               "echo 'Removing extended regions...'\n" \
               "unextend=${lrcstats}/src/preprocessing/unextend_alignments/unextend_alignments.py\n" \
               "unextendOutput=${data}/${experiment_name}_unextended.maf\n" \
               "python $unextend -i ${maf} -m ${unextendOutput}\n" \
               "maf=$unextendOutput\n" \
               "\n"
	file.write(line)

def writeStats(file, trimmed, extended):
	if extended:
		writeRemoveExtensions(file)

	line = "############### Collecting data ###########\n" \
                "echo 'Collecting data...'\n" \
                "\n" \
                "statsOutput=${data}/${experiment_name}.stats\n" \
                "\n"
	file.write(line)

	if trimmed:
		command = "$aligner stats -m ${maf} -o ${statsOutput} -t}\n\n"
	else:
		command = "$aligner stats -m ${maf} -o ${statsOutput}\n\n"
	file.write(command)

	line = "input=${statsOutput}\n" \
		"\n"
	file.write(line)
	line = "############## Summarizing statistics ############\n" \
		"echo 'Summarizing statistics...'\n" \
		"\n" \
		"summarizeStats=${lrcstats}/src/statistics/summarize_stats.py\n" \
		"statsOutput=${data}/${testName}_results.txt\n" \
                        "\n"
	file.write(line)

	if trimmed:
		line = "python ${summarizeStats} -i ${input} -o ${statsOutput}\n"
	else:
		line = "python ${summarizeStats} -i ${input} -b -o ${statsOutput}\n"
	file.write(line)

def writePipeline(file, experimentDetails):
	trimmed = experimentDetails["trimmed"]
	extended = experimentDetails["extended"]
	threads = experimentDetails["threads"]
	writeSort(file)
	writePrune(file)
	if trimmed:
		writeConcatenate(file)
	writeAlignment(file,trimmed,extended,threads)
	writeStats(file,trimmed,extended)
		
MAJOR_VERSION = 1
MINOR_VERSION = 0

# Command line arguments go here.
parser = argparse.ArgumentParser(description='''
	Long Read Correction Stats (LRCStats) Pipeline generator,
	Version %d.%d
	''' % (MAJOR_VERSION, MINOR_VERSION))

parser.add_argument('-b', '--blank_config', metavar='CONFIG_PATH', type=str, help=
	"""
	create a new configuration file at CONFIG_PATH 
	""")

parser.add_argument('-i', '--input_config', metavar='CONFIG', type=str, help=
	"""
	path to the configuration file
	""")
parser.add_argument('-n', '--experiment_name', metavar='NAME', type=str, help=
	"""
	name of the experiment
	""")
parser.add_argument('-t', '--trimmed', action="store_true", help=
	"""
	corrected long reads are trimmed
	""")
parser.add_argument('-e', '--extended', action="store_true", help=
	"""
	corrected long reads are extended
	""")
parser.add_argument('-d', '--data', metavar='DATA_PATH', type=str, help=
	"""
	directory to store temporary and results files
	""")
parser.add_argument('-c', '--clr', metavar='CLR_PATH', type=str, help=
	"""
	path to the cLR FASTA file
	""")
parser.add_argument('-m', '--maf', metavar='MAF_PATH', type=str, help=
	"""
	path to the ref-uLR two-way alignment MAF file
	""")
parser.add_argument('-o', '--output', metavar='OUTPUT_PATH', type=str, help=
	"""
	output path for pipeline script
	""")
parser.add_argument('-p', '--threads', metavar="NUM_THREADS", type=str, help=
	"""
	number of threads to use
	""")

args = parser.parse_args()

if args.blank_config:
	createBlankConfig(args.blank_config)
	print("Created a new configuration file.")
	sys.exit()

experimentDetails = {}
paths = {}
initCommands = []
pbsOptions = []
outputPath = None

# input_config must come before the rest of the command line options

if args.input_config:
	experimentDetails, paths, initCommands, pbsOptions = readConfig(args.input_config)

if args.experiment_name:
	experimentDetails["experiment_name"] = args.experiment_name
if args.trimmed:
	experimentDetails["trimmed"] = True
else:
	experimentDetails["trimmed"] = False
if args.extended:
	experimentDetails["extended"] = True
else:
	experimentDetails["extended"] = False
if args.threads:
	experimentDetails["threads"] = args.threads
if args.data:
	paths["data"] = args.data
if args.clr:
	paths["clr"] = args.clr
if args.maf:
	paths["maf"] = args.maf
if args.output:
	outputPath = args.output

argsIncomplete = False

if "experiment_name" not in experimentDetails:
	argsIncomplete = True
	print("Error: please provide the name of the experiment.")
if "data" not in paths:
	argsIncomplete = True
	print("Error: please provide the path to the data directory.")
if "clr" not in paths:
	argsIncomplete = True
	print("Error: please provide the path to the corrected long reads FASTA file.")
if "maf" not in paths:
	argsIncomplete = True
	print("Error: please provide the path to the ref-uLR two-way alignment MAF file.")
if "threads" not in experimentDetails:
	argsIncomplete = True
	print("Error: please provide the number of threads you would like to use.")
if outputPath is None:
	argsIncomplete = True
	print("Error: please provide an output path.")

if argsIncomplete:
	sys.exit(1)
	
with open(outputPath,'w') as file:
	writeHeader(file,pbsOptions)
	writeInit(file,initCommands)
	writePaths(file,paths)
	writePipeline(file,experimentDetails)

print("LRCStats pipeline shell script created at %s" % (outputPath))
