import sys
import getopt

def writeHeader(file, scriptPath):
	# Write the generic header lines for PBS scripts
	line = "#!/bin/bash\n"
	file.write(line)

	# Write the resources
	resources = ['walltime=12:00:00', 'mem=8gb', 'nodes=1:ppn=4']
	for resource in resources:
		line = "PBS -l %s\n" % (resource)
		file.write(line)

	# Specify the location of the epilogue script
	line = "#PBS -l epilogue=/home/seanla/Jobs/epilogue.script\n"
	file.write(line)

	# Email to send info about jobs
	line = "#PBS -M laseanl@sfu.ca\n"
	file.write(line)
	
	# Only send emails when jobs are done or aborted
	line = "#PBS -m ea\n"
	file.write(line)
	
	# Epilogue info all in one file
	line = "#PBS -j oe\n"	
	file.write(line)

	# Epilogue script output path
	line = "#PBS -o %s.out\n" % (scriptPath)
	file.write(line)

def simulateShortReads(genome, coverage):
	# Given the genome and coverage, make PBS script to simulate short reads
	scriptPath = "%s/simulate_%s_short_d%s.pbs" % (jobsDir, genome, coverage) 
	with open(scriptPath, 'w') as file:
		writeGenericHeader(file)

		# Name of the job
		line = "#PBS -N simulate_%s_short_d%s\n" % (genome, coverage)
		file.write(line)

		file.write('\n')

		# Write genome name and coverage
		coverage = "cov=%s\n" % (coverage)
		file.write(coverage)

		genome = "genome=%s\n" % (genome)
		file.write(genome)

		genomeDir = "genomeDir=%s/${genome}\n" % (scratchDir, genome)
		file.write(genomeDir)

		outputDir = "outputDir=$genomeDir/art/short-d${cov}\n"
		file.write(outputDir)

		outputPrefix = "outputPrefix=$outputDir/${genome}-short-paired-d${cov}\n" 
		file.write(outputPrefix)

		reference = "$genomeDir/${genome}_reference.fasta\n" 
		file.write(reference)

		artPath = "art=/home/seanla/Software/art_bin_GreatSmokyMountains/art_illumina\n"
		file.write(artPath)

		file.write('\n')

		mkdir = "mkdir -p $outputDir\n"
		file.write(mkdir)

		command = "$art -p -i $ref -l 100 -f $cov -o $outputPrefix\n"
		file.write(command)

		file.write('\n')

		fq2fastqPath = "fq2fastq=/home/seanla/Projects/lrcstats/src/preprocessing/fq2fastq.py\n"
		file.write(fq2fastqPath)

		file.write('\n')

		fq2fastqCommand = "python $fq2fastq -i $outputDir\n"
		file.write(fq2fastqCommand)

def simulateLongReads(genome, coverage):
	# Given the genome and coverage, make PBS script to simulate short reads
	scriptPath = "%s/simulate_%s_long_%s.pbs" % (jobsDir, genome, coverage) 
	with open(scriptPath, 'w') as file:
		writeGenericHeader(file)

		# Name of the job
		line = "#PBS -N simulate_%s_long_%s\n" % (genome, coverage)
		file.write(line)

		file.write('\n')

		# Write genome name and coverage
		coverage = "cov=%s\n" % (coverage)
		file.write(coverage)

		genome = "genome=%s\n" % (genome)
		file.write(genome)

		genomeDir = "genomeDir=%s/${genome}\n" % (scratchDir, genome)
		file.write(genomeDir)

		outputDir = "outputDir=$genomeDir/simlord/long-d${cov}\n"
		file.write(outputDir)

		outputPrefix = "outputPrefix=$outputDir/${genome}-long-d${cov}\n" 
		file.write(outputPrefix)

		reference = "$genomeDir/${genome}_reference.fasta\n" 
		file.write(reference)

		if genome is "ecoli":
			fastq = ecoliFastq
		elif genome is "yeast":
			fastq = yeastFastq
		elif genome is "fly":
			fastq = flyFastq

		fastqPath = "fastq=$genomeDir/%s\n" % (fastq)
		file.write(fastqPath)

		file.write('\n')

		reads4coverage="reads4coverage=/home/seanla/Projects/lrcstats/src/preprocessing/reads4coverage.py\n"
		file.write(reads4coverage)

		simlord = "simlord=/home/seanla/Software/anaconda2/envs/simlord/bin/simlord\n"
		file.write(simlord)

		file.write('\n')

		mkdir = "mkdir -p $outputDir\n"
		file.write(mkdir)

		reads = "reads=$(python $reads4coverage -c $cov -i $fastq -r $ref)\n"
		file.write(reads)

		command = "$simlord -n $reads -sf $fastq -rr $ref $output\n"
		file.write(command)

# Global variables
jobsDir = "/home/seanla/Jobs/lrcstats/simulate"
scratchDir = "/global/scratch/seanla/Data"
ecoliFastq = "SRR1284073.fastq"
yeastFastq = "SRR1284073-1284662_combined.fastq"
flyFastq = "SRR1204085.fastq"

helpMessage = "Generate PBS job scripts for simulating DNA reads."
usageMessage = "Usage: %s [-h help and usage] [-f fly] [-e ecoli] [-y yeast] [-l simulate long reads] [-s simulate short reads] [-c coverage] [-a simulate all coverages]" % (sys.argv[0])

options = "hfeylsca:"

try:
	opts, args = getopt.getopt(sys.argv[1:], options)
except getopt.GetoptError:
	print "Error: unable to read command line arguments."
	sys.exit(2)

if len(sys.argv) == 1:
	print usageMessage
	sys.exit(2)

simLong = False
simShort = False
coverage = None
allCov = False

doYeast = False
doEcoli = False
doFly = False

genomes = []
coverage = None

for opt, arg in opts:
	# Help message
	if opt == '-h':
		print helpMessage
		print usageMessage
		sys.exit()
	elif opt == '-f':
		doFly = True
		genomes.append('fly')
	elif opt == '-e':
		doEcoli = True
		genomes.append('ecoli')
	elif opt == '-y':
		doYeast = True
		genomes.append('yeast')
	elif opt == '-s':
		simShort = True
	elif opt == '-l':
		simLong = True
	elif opt == '-c':
		coverages = [arg]
	elif opt == '-a':
		allCov = True

optsIncomplete = False

if not doFly or not doYeast or not doEcoli:
	print "Please select a genome to simulate."
	optsIncomplete = True
if not simLong and not simShort:
	print "Please select which type of reads you would like to simulate."
	optsIncomplete = True
if simLong and simShort and not allCov:
	print "You can only simulate both short and long reads by specifying simulating all coverages."
	optsIncomplete = True

if optsIncomplete:
	print usageMessage
	sys.exit(2)

if simLong:
	coverages = ['10', '20', '50', '75']
elif simShort:
	coverages = ['50', '100', '200']

for genome in genomes:
	for coverage in coverages:
		if simLong:
			simulateLongReads(genome, coverage)
		elif simShort:
			simulateShortReads(genome, coverage) 
