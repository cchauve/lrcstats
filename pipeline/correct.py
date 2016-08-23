import job_header

def writeResources(file, genome):
	'''
	Write the resource usage into the job script.
	'''
	if genome == "fly":
		mem = 128
	else:
		mem = 64
	resources = ["walltime=3:00:00:00", "mem=%dgb" % (mem), "nodes=1:ppn=8"]

	for resource in resources:
		line = "#PBS -l %s\n" % (resource)
		file.write(line)
	file.write("\n")

def writePaths(file, testDetails, paths):
	'''
	Write the paths to the file.
	Inputs:
	- (file object) file
	- (dict of strings) testDetails: dict of test parameters
	'''

 	program = "program=%s\n" % (testDetails["program"])

	genome = "genome=%s\n" % (testDetails["genome"])

	experiment = "experiment=%s\n" % (testDetails["experimentName"])

	shortCov = "shortCov=%s\n" % (testDetails["shortCov"])

	longCov = "longCov=%s\n" % (testDetails["longCov"])

	prefix = "prefix=%s/${experiment}\n" % (paths["data"])

	art = "art=${prefix}/simulate/art/short-d${shortCov}\n"

	line = experiment + program + genome + shortCov + longCov + prefix + art
	file.write(line)

	line = "testName=${program}-${genome}-${shortCov}Sx${longCov}L\n" \
		"mergedShort=${art}/${genome}-short-paired-d${shortCov}-merged.fastq\n" \
		"short1=${art}/${genome}-short-paired-d${shortCov}1.fastq\n" \
		"short2=${art}/${genome}-short-paired-d${shortCov}2.fastq\n" \
		"long=${prefix}/simulate/simlord/long-d${longCov}/${genome}-long-d${longCov}.fastq\n" \
		"outputDir=${prefix}/correct/${program}/${testName}\n" \
		"\n"
	file.write(line)

def writeLordec(file, paths):
	'''
	Generate LoRDEC pipeline
	'''
	line = "lordec=%s\n" % (paths["lordec"])
	file.write(line)

	line = "output=${outputDir}/${testName}.fasta" \
		"\n" \
		"cd ${outputDir}\n" \
		"$lordec -T ${PBS_NUM_PPN} --trials 5 --branch 200 --errorrate 0.4 " \
			"-2 ${short1} ${short2} -k 19 -s 3 -i ${long} -o ${output}\n"
	file.write(line)

def writeJabba(file, paths):
	'''
	Generate Jabba pipeline.
	'''
	karectPath = "karect=%s\n" % ( paths["karect"] ) 
	file.write(karectPath)

	browniePath= "brownie=%s\n" % ( paths["brownie"] )
	file.write(browniePath)

	jabbaPath = "jabba=%s\n" % ( paths["jabba"] )
	file.write(jabbaPath)

	line = "karectDir=$outputDir/karect\n" \
		"brownieDir=$outputDir/brownie\n" \
		"jabbaDir=$outputDir/jabba\n" \
		"\n" \
		"mkdir -p $karectDir\n" \
		"mkdir -p $brownieDir\n" \
		"mkdir -p $jabbaDir\n" \
		"\n" \
		"$karect -correct -inputfile=$short1 -inputfile=$short2 -resultdir=$karectDir " \
			"-tempdir=$karectDir -celltype=haploid -matchtype=hamming -threads=${PBS_NUM_PPN}\n" \
		"\n" \
		"short1=$karectDir/karect_${genome}-short-paired-d${shortCov}1.fastq\n" \
		"short2=$karectDir/karect_${genome}-short-paired-d${shortCov}2.fastq\n" \
		"\n" \
		"$brownie graphCorrection -k 75 -p $brownieDir $short1 $short2\n" \
		"\n" \
		"rm -r $karectDir\n" \
		"\n" \
		"dbGraph=$brownieDir/DBGraph.fasta\n" \
		"\n" \
		"$jabba -t ${PBS_NUM_PPN} -l 20 -k 75 -o $jabbaDir -g $dbGraph -fastq $long\n" \
		"\n" \
		"rm -r $brownieDir\n"
	file.write(line)

def writeProovread(file, paths):
	'''
	Generate Proovread correction commands.
	'''
	proovread = "proovread=%s\n" % ( paths["proovread"] )
	file.write(proovread)

	line = "output=$outputDir\n" \
		"\n" \
		"$proovread -t ${PBS_NUM_PPN} --lr-qv-offset 70 -s $short1 -s $short2 -l $long -p $output\n"
	file.write(line)

def writeColormap(file, paths):
	'''
	Generate CoLoRMap correction commands w/o OEA
	'''
	line = "colormap=%s\n" % ( paths["colormap"] ) 
	file.write(line)

	line = 	"\n" \
		"cd $outputDir\n" \
		"$colormap $long $mergedShort $outputDir ${PBS_NUM_PPN}\n" 
	file.write(line)

def writeColormapOea(file, paths):
	'''
	Generate CoLoRMap correction script w/ OEA
	'''
	line = "colormapOea=%s\n" % ( paths["colormap_oea"] ) 
	file.write(line)

	line = 	"\n" \
		"cd $outputDir\n" \
		"${colormapOea} $long $mergedShort $outputDir ${PBS_NUM_PPN}\n" 
	file.write(line)

def generateCorrectionJob(testDetails, paths):
	'''
	Generates a PBS job script for long read correction.
	Input
	- (dict of strings) testDetails: dict of test parameters
	- (dict of strings) paths: contains the paths to the different program paths
	'''
	testName = "%s-%s-%sSx%sL" \
		% (testDetails["program"], testDetails["genome"], \
			testDetails["shortCov"], testDetails["longCov"])

	scriptPath = "%s/scripts/%s/correct/%s/%s-correct.pbs" \
		% (paths["lrcstats"], testDetails["experimentName"], testDetails["program"], testName)

	with open(scriptPath,'w') as file:
		job_header.writeHeader(file, paths)

		# job epilogue output files will be in the same directory as the output data
		jobOutputPath = "#PBS -o %s/%s/correct/%s/%s/%s.out\n" \
			% (paths["data"], testDetails["experimentName"],
				 testDetails["program"], testName, testName)
		file.write(jobOutputPath)

		jobName = "#PBS -N %s-correct\n" % (testName)
		file.write(jobName)

		writeResources(file, testDetails["genome"])
		writePaths(file, testDetails, paths)

		line = "set -e\n" \
			"mkdir -p $outputDir\n" \
			"\n"
		file.write(line)

		program = testDetails["program"]

		if program == "colormap":
			writeColormap(file, paths)
		elif program == "colormap_oea":
			writeColormapOea(file, paths)
		elif program == "proovread":
			writeProovread(file, paths)
		elif program == "lordec":
			writeLordec(file, paths)
		elif program == "jabba":
			writeJabba(file, paths)
