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

def writePaths(file, test_details):
	'''
	Write the paths to the file.
	Inputs:
	- (file object) file
	- (dict of strings) test: dict of test parameters
	'''
 	program = "program=%s\n" % (test_details["program"])

	genome = "genome=%s\n" % (test_details["genome"])

	short_coverage = "short_coverage=%s\n" % (test_details["short_coverage"])

	long_coverage = "long_coverage=%s\n" % (test_details["long_coverage"])

	prefix = "prefix=%s/${genome}\n" % (paths["data"])

	art = "art=${prefix}/art/short-paired-d${short_coverage}\n"

	line = program + genome + short_coverage + long_coverage + prefix + art
	file.write(line)

	line = "test=${program}-${genome}-${short_coverage}Sx${long_coverage}L\n"
		"mergedShort=${art}/${genome}-short-paired-d${short_coverage}-merged.fastq\n" \
		"short1=${art}/${genome}-short-paired-d${short_coverage}1.fastq\n" \
		"short2=${art}/${genome}-short-paired-d${short_coverage}2.fastq\n" \
		"long=${prefix}/simlord/long-d${long_coverage}/${genome}-long-d${long_coverage}.fastq\n" \
		"outputDir=${prefix}/corrections/${program}/${test}\n" \
		"\n"
	file.write(line)

def writeLordec(file):
	'''
	Generate LoRDEC pipeline
	'''
	line = "output=${output}/${test}.fasta" \
		"cd ${outputDir}\n" \
		"\n" \
		"lordec=/home/seanla/Software/LoRDEC-0.6/lordec-correct\n" \
		"$lordec -T ${PBS_NUM_PPN} --trials 5 --branch 200 --errorrate 0.4 " \
			"-2 ${short1} ${short2} -k 19 -s 3 -i ${long} -o ${output}\n"
	file.write(line)

def writeJabba(file):
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
		"short1=$karectDir/karect_${genome}-short-paired-d${short_coverage}1.fastq\n" \
		"short2=$karectDir/karect_${genome}-short-paired-d${short_coverage}2.fastq\n" \
		"\n" \
		"$brownie graphCorrection -k 75 -p $short1 $short2 $brownieDir\n" \
		"\n" \
		"rm -r $karectDir\n" \
		"\n" \
		"dbGraph=$brownie/DBGraph.fasta\n" \
		"\n" \
		"$jabba -t ${PBS_NUM_PPN} -l 20 -k 75 -o $jabbaDir -g $dbGraph -fastq $long\n" \
		"\n" \
		"rm -r $brownieDir\n"
	file.write(line)

def writeProovread(file):
	'''
	Generate Proovread correction commands.
	'''
	proovread = "proovread=%s\n" % ( paths["proovread"] )
	file.write(proovread)

	line = "output=$outputDir\n" \
		"\n" \
		"$proovread -t ${PBS_NUM_PPN} --lr-qv-offset 70 -s $short1 -s $short2 -l $long -p $output\n"
	file.write(line)

def writeColormap(file):
	'''
	Generate CoLoRMap correction commands w/o OEA
	'''
	line = "colormap=/home/seanla/Software/colormap/runCorr.sh\n" \
		"\n" \
		"cd $outputDir\n" \
		"$colormap $long $mergedShort $outputDir ${PBS_NUM_PPN}\n" 
	file.write(line)

def writeColormapOea(file):
	'''
	Generate CoLoRMap correction script w/ OEA
	'''
	line = "colormap=/home/seanla/Software/colormap/runOea.sh\n" \
		"\n" \
		"cd $outputDir\n" \
		"$colormap $long $mergedShort $outputDir ${PBS_NUM_PPN}\n" 
	file.write(line)

def generateCorrectionJob(test_details):
	'''
	Generates a PBS job script for long read correction.
	Input
	- (dict of strings) test: dict of test parameters
	'''
	test_name = "%s-%s-%sSx%sL" \
		% (test_details["program"], test_details["genome"], \
			test_details["short_coverage"], test_details["long_coverage"])
	scriptPath = "%s/scripts/correct/%s/%s-correct.pbs" \
		% (paths["lrcstats"], test_details["program"], test_name)
	with open(scriptPath,'w') as file:
		job_header.writeGenericHeader(file)

		jobOutputPath = "#PBS -o %s/%s/corrections/%s/%s/%s.out" \
			% (paths["data"], test_details["genome"], test_details["program"], \
				test_name, test_name)
		file.write(jobOutputPath)

		jobName = "#PBS -N %s-correct\n" % (test_name)
		file.write(jobName)

		writeResources(file, test_details["genome"])
		writePaths(file, test_details)

		line = "set -e\n" \
			"mkdir -p $outputDir\n" \
			"\n"
		file.write(line)

		if test["program"] == "colormap":
			writeColormap(file)
		elif test["program"] == "colormap_oea":
			writeColormapOea(file)
		elif test["program"] == "proovread":
			writeProovread(file)
		elif test["program"] == "lordec":
			writeLordec(file)
		elif test["program"] == "jabba":
			writeJabba(file)
