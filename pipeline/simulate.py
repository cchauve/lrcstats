import job_header

def writeResources(file):
	'''
	Write the resources
	'''
	resources = ['walltime=24:00:00', 'mem=16gb', 'nodes=1:ppn=1']
	for resource in resources:
		line = "#PBS -l %s\n" % (resource)
		file.write(line)

def simulateArtShortReads(testDetails, paths):
	'''
	Given the genome and coverage, make PBS script to simulate short reads
	Inputs
	- (dict of strings) testDetails: contains the parameters for the test
	- (dict of strings) paths: contains the program paths for the users systems
	'''
	# Reminder: experimentName is a global variable - initialized in lrcstats.py
	scriptPath = "%s/scripts/%s/simulate/art/simulate-%s-short-d%s.pbs" \
			% (paths["lrcstats"], testDetails["experimentName"], testDetails["genome"], testDetails["shortCov"]) 
	with open(scriptPath, 'w') as file:
		job_header.writeHeader(file, paths)

		line = "#PBS -o %s/%s/simulate/art/short-d%s/short-d%s.out\n" \
			% (paths["data"], testDetails["experimentName"], testDetails["shortCov"], testDetails["shortCov"])
		file.write(line)

		writeResources(file)

		# Name of the job
		line = "#PBS -N %s-simulate-%s-short-d%s\n" \
			% (testDetails["experimentName"], testDetails["genome"], testDetails["shortCov"])
		file.write(line)

		file.write('\n')

		experiment = "experiment=%s\n" % (testDetails["experimentName"])

		coverage = "cov=%s\n" % (testDetails["shortCov"])

		genome = "genome=%s\n" % (testDetails["genome"])

		genomeDir = "genomeDir=%s\n" % (paths["data"])

		refKey = "%s_ref" % (testDetails["genome"])
		refPath = "ref=%s\n" % (paths[refKey])

		artPath = "art=%s\n" % (paths["art"])

		fq2fastqPath = "fq2fastq=%s/src/preprocessing/fq2fastq.py\n" % (paths["lrcstats"])

		merge_files = "merge_files=%s/src/preprocessing/utils/fastUtils\n" \
				% (paths["lrcstats"])

		line = experiment + coverage + genome + genomeDir + refPath + artPath + fq2fastqPath + merge_files
		file.write(line)

		line = "outputDir=$genomeDir/${experiment}/simulate/art/short-d${cov}\n" \
			"outputPrefix=$outputDir/${genome}-short-paired-d${cov}\n" \
			"\n" \
			"mkdir -p $outputDir\n" \
			"$art -p -i $ref -l 100 -f $cov -m 300 -s 25 -o $outputPrefix\n" \
			"\n" \
			"python $fq2fastq -i $outputDir\n" \
			"\n" \
			"short1=${outputPrefix}1.fastq\n" \
			"short2=${outputPrefix}2.fastq\n" \
			"shortMerged=${outputPrefix}-merged.fastq\n" \
			"\n" \
			"$merge_files shuffle -1 $short1 -2 $short2 -o $shortMerged\n"
		file.write(line)

def simulateSimlordLongReads(testDetails, paths):
	'''
	Given the genome and coverage, make PBS script to simulate short reads
	Input
	- (dict of strings) testDetails: contains the test parameters
	- (dict of strings) paths: contains the program paths for the users systems
	'''
	scriptPath = "%s/scripts/%s/simulate/simlord/simulate-%s-long-d%s.pbs" \
			% (paths["lrcstats"], testDetails["experimentName"], testDetails["genome"], testDetails["longCov"]) 

	with open(scriptPath, 'w') as file:
		job_header.writeHeader(file, paths)
		writeResources(file)

		line = "#PBS -o %s/%s/simulate/simlord/long-d%s/long-d%s.out\n" \
			% (paths["data"], testDetails["experimentName"], \
			testDetails["longCov"], testDetails["longCov"])
		file.write(line)

		# Name of the job
		line = "#PBS -N %s-simulate-%s-long-%s\n" \
			% (testDetails["experimentName"], testDetails["genome"], testDetails["longCov"])
		file.write(line)

		file.write('\n')

		# Write genome name and coverage

		# Reminder: experimentName is a global variable - initialized in lrcstats.py
		experiment = "experiment=%s\n" % (testDetails["experimentName"])

		coverage = "cov=%s\n" % (testDetails["longCov"])

		genome = "genome=%s\n" % (testDetails["genome"])

		genomeDir = "genomeDir=%s\n" % (paths["data"])

		refKey = "%s_ref" % (testDetails["genome"])
		refPath = "ref=%s\n" % (paths[refKey])

		simlord = "simlord=%s\n" % (paths["simlord"])

		lrcstats = "lrcstats=%s\n" % (paths["lrcstats"])

		line = experiment + coverage + genome + genomeDir + refPath + simlord + lrcstats
		file.write(line)

		line = "sam2maf=${lrcstats}/src/preprocessing/sam2maf/sam2maf.py\n" \
			"reads4coverage=${lrcstats}/src/preprocessing/reads4coverage.py\n" \
			"outputDir=${genomeDir}/${experiment}/simulate/simlord/long-d${cov}\n" \
			"outputPrefix=${outputDir}/${genome}-long-d${cov}\n"
		file.write(line)

		# Get the name of the real PacBio FASTQ file
		key = "%s_fastq" % (testDetails["genome"])
		fastq = paths[key]

		fastqPath = "fastq=%s\n" % (fastq)
		file.write(fastqPath)

		file.write('\n')

		line = "mkdir -p $outputDir\n" \
			"reads=$(python $reads4coverage -c $cov -i $fastq -r $ref)\n" \
<<<<<<< HEAD
			"$simlord -mp 1 -n $reads -sf $fastq -rr $ref $outputPrefix\n" \
=======
			"$simlord -n $reads -mp 1 -sf $fastq -rr $ref $outputPrefix\n" \
>>>>>>> dc50b592cb8c56bc725ad6231926d7eb1c71d6b8
			"\n" \
			"sam=${outputPrefix}.fastq.sam\n" \
			"maf=${sam}\n" \
			"\n" \
			"python $sam2maf -r $ref -s $sam -o $maf\n"
		file.write(line)

def createQuickQsubScript(shortTestDetails, longTestDetails, paths, experimentName):
	'''
	Create quick qsub script for read simulations
	'''
	scriptPaths = []
	for testDetail in longTestDetails:
		# Add the path to the short read sim
		scriptPath = "%s/scripts/%s/simulate/simlord/simulate-%s-long-d%s.pbs" \
			% (paths["lrcstats"], testDetail["experimentName"], testDetail["genome"], testDetail["longCov"]) 
		scriptPaths.append(scriptPath)

	for testDetail in shortTestDetails:
		# Add the path to the long read sim
		scriptPath = "%s/scripts/%s/simulate/art/simulate-%s-short-d%s.pbs" \
			% (paths["lrcstats"], testDetail["experimentName"], testDetail["genome"], testDetail["shortCov"]) 
		scriptPaths.append(scriptPath)

	path = "%s/scripts/%s/quick-qsub-simulate.sh" % (paths["lrcstats"], experimentName)
	with open(path,'w') as file:
		file.write("#!/bin/bash\n")
		for scriptPath in scriptPaths:
			line = "qsub %s\n" % (scriptPath)
			file.write(line)
