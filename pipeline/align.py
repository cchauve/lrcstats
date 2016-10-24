import job_header

def writeResources(file):
        '''
        Write the resource usage into the job script.
        '''
        resources = ["walltime=3:00:00:00", "mem=64gb", "nodes=1:ppn=8"]

        for resource in resources:
                line = "#PBS -l %s\n" % (resource)
                file.write(line)

	file.write('\n')

def writePaths(file, testDetails, paths):
	'''
	Write the paths to the data.
	Inputs:
        - (file object) file
        - (dict of strings) test: dict of test parameters
	- (dict of strings) paths: contains the paths to the different programs in the user's machines
	'''
	experiment = "experiment=%s\n" % (testDetails["experimentName"])

	lrcstats = "lrcstats=%s\n" % (paths["lrcstats"])

	program = "program=%s\n" % (testDetails["program"])

        genome = "genome=%s\n" % (testDetails["genome"])

        longCov = "longCov=%s\n" % (testDetails["longCov"])

	shortCov = "shortCov=%s\n" % (testDetails["shortCov"])

        prefix = "prefix=%s/${experiment}\n" % (paths["data"])

	test = "testName=${program}-${genome}-${shortCov}Sx${longCov}L\n"

	line = experiment + lrcstats + program + genome + longCov + shortCov + prefix + test 
        file.write(line)
	
	line = "outputDir=${prefix}/align/${program}/${testName}\n" \
		"inputDir=${prefix}/correct/${program}/${testName}\n" \
		"maf=${prefix}/simulate/simlord/long-d${longCov}/${genome}-long-d${longCov}.fastq.sam.maf\n" \
		"\n"
	file.write(line)	

def writeSortFasta(file):
	'''
	Write the commands to sort FASTA file
	'''
	line = "############### Sort FASTA ###########\n" \
		"echo 'Sorting FASTA file...'\n" \
		"\n" \
		"sortfasta=${lrcstats}/src/preprocessing/sortfasta/sortfasta.py\n" \
		"sortedOutput=${outputDir}/sorted.fasta\n" \
		"\n" \
		"python $sortfasta -i $input -o $sortedOutput\n" \
		"\n" \
		"input=$sortedOutput\n" \
		"\n" 
	file.write(line)	

def writePruneMaf(file):
	'''
	Write the commands to prune the MAF file
	'''
	line = "############### Prune the maf file(s) ###########\n" \
		"echo 'Pruning MAF file(s)...'\n" \
		"\n" \
		"prunemaf=${lrcstats}/src/preprocessing/prunemaf/prunemaf.py\n" \
		"pruneOutput=${outputDir}/pruned\n" \
		"python $prunemaf -f $input -m $maf -o $pruneOutput\n" \
		"\n" \
		"maf=${pruneOutput}.maf\n" \
		"\n"
	file.write(line)

def writeProcessTrimmedReads(file):
	'''
	Write the commands to process trimmed reads.
	'''
	line = "############### Processing Trimmed Reads ###########\n" \
		"echo 'Processing trimmed reads...'\n" \
		"concatenate=${lrcstats}/src/preprocessing/concatenate_trimmed/concatenate_trimmed.py\n" \
		"concatenated_output=${outputDir}/concatenated.fasta\n" \
		"\n" \
		"python $concatenate -i $input -o ${concatenated_output}\n" \
		"\n" \
		"input=${concatenated_output}\n" \
		"\n"
	file.write(line)

def writeAlignment(file, program):
	'''
	Write the commands to create a three-way alignment
	between the cLR, uLR and ref
	'''
	line = "############### Generate three-way alignment ###########\n" \
		"echo 'Generating three-way alignment...'\n" \
		"aligner=${lrcstats}/src/aligner/aligner\n" \
		"mafOutput=${outputDir}/${testName}.maf\n" \
		"\n"
	file.write(line)

	if program is "jabba":
		command = "$aligner maf -m $maf -c $input -t -e -o $mafOutput -p ${PBS_NUM_PPN}\n"
		file.write(command)
	elif program is "proovread":
		command = "$aligner maf -m $maf -c $input -t -o $mafOutput -p ${PBS_NUM_PPN}\n"
		file.write(command)
	elif program is "lordec":
		command = "$aligner maf -m $maf -c $input -o $mafOutput -p ${PBS_NUM_PPN}\n"
		file.write(command)
	elif program in ["colormap", "colormap_oea"]:
		command = "$aligner maf -e -m $maf -c $input -o $mafOutput -p ${PBS_NUM_PPN}\n"
		file.write(command)

def writeConvertFastq2Fasta(file):
	'''
	Write the commands for FASTQ2FASTA script
	'''
	line = "############### Convert FASTQ to FASTA ###########\n" \
		"echo 'Converting FASTQ to FASTA...'\n" \
		"\n" \
		"fastq2fasta=${lrcstats}/src/preprocessing/fastq2fasta/fastq2fasta.py\n" \
		"outputq2a=$outputDir/${testName}\n" \
		"\n" \
		"python $fastq2fasta -i $input -o $outputq2a\n" \
		"\n" \
		"input=${outputq2a}.fasta\n" \
		"\n"
	file.write(line)

def writeLordec(file, testDetails):
	'''
	Write the commands for lordec alignment
	'''
	inputfasta="input=${inputDir}/${testName}.fasta\n\n"
	file.write(inputfasta)

	writeSortFasta(file)
	writePruneMaf(file)
	writeAlignment(file, testDetails["program"])

def writeJabba(file, testDetails):
	'''
	Write the commands for jabba alignment
	'''
	inputFastq="input=${inputDir}/jabba/Jabba-${genome}-long-d${longCov}.fastq\n\n"
	file.write(inputFastq)
	writeConvertFastq2Fasta(file)
	writeProcessTrimmedReads(file)
	writePruneMaf(file)
	writeAlignment(file, testDetails["program"])

def writeProovread(file, testDetails):
	'''
	Write the commands for proovread alignment
	'''
	inputFasta="input=${inputDir}/${testName}.trimmed.fa\n\n"
	file.write(inputFasta)
	writeProcessTrimmedReads(file)
	writePruneMaf(file)
	writeAlignment(file, testDetails["program"])

def writeColormap(file, testDetails):
	'''
	Write the commands for colormap w/o OEA
	'''
	inputFasta="input=${inputDir}/${testName}_iter2.fasta\n\n" 
	file.write(inputFasta)
	writeSortFasta(file)
	writePruneMaf(file)
	writeAlignment(file, testDetails["program"])

def writeColormapOea(file, testDetails):
	'''
	Write the commands for colormap w/ OEA
	'''
	inputFasta="input=${inputDir}/${testName}_oea.fasta\n\n"
	file.write(inputFasta)
	writeSortFasta(file)
	writePruneMaf(file)
	writeAlignment(file, testDetails["program"])

def generateAlignmentJob(testDetails, paths):
	'''
	Generates a PBS job script for cLR, uLR and ref alignments.
	Input
	- (dict of strings) testDetails: dict of test parameters
	- (dict of strings) paths: contains the paths to the programs on the user's machine
	'''
	testName = "%s-%s-%sSx%sL" \
		% (testDetails["program"], testDetails["genome"], \
			 testDetails["shortCov"], testDetails["longCov"])

	scriptPath = "%s/scripts/%s/align/%s/%s-align.pbs" \
		% (paths["lrcstats"], testDetails["experimentName"], testDetails["program"], testName)

	with open(scriptPath, 'w') as file:
		job_header.writeHeader(file, paths)
		jobOutputPath = "#PBS -o %s/%s/align/%s/%s/%s.out\n" \
                        % (paths["data"], testDetails["experimentName"], \
				 testDetails["program"], testName, testName)
                file.write(jobOutputPath)

		jobName = "#PBS -N %s-%s-align\n" % (testDetails["experimentName"], testName)
                file.write(jobName)

		writeResources(file)
		writePaths(file, testDetails, paths)
		
		line = "set -e\n" \
			"mkdir -p ${outputDir}\n" \
			"\n"
                file.write(line)

		program = testDetails["program"]

                if program == "colormap":
                        writeColormap(file, testDetails)
                elif program == "colormap_oea":
                        writeColormapOea(file, testDetails)
                elif program == "proovread":
                        writeProovread(file, testDetails)
                elif program == "lordec":
                        writeLordec(file, testDetails)
                elif program == "jabba":
                        writeJabba(file, testDetails)

		line = "qsub %s/scripts/%s/stats/%s/%s-stats.pbs\n" \
			% (paths["lrcstats"], testDetails["experimentName"], testDetails["program"], testName)
		file.write(line)

def createQuickQsubScript(testDetails, paths, experimentName):
	'''
	create a quick-qsub script for the alignment jobs
	'''
	 # Create a list of the paths to the correction jobs
        scriptPaths = []
        for testDetail in testDetails:
		testName = "%s-%s-%sSx%sL" \
			% (testDetail["program"], testDetail["genome"], testDetail["shortCov"], testDetail["longCov"])

		scriptPath = "%s/scripts/%s/align/%s/%s-align.pbs" \
			% (paths["lrcstats"], testDetail["experimentName"], testDetail["program"], testName)
                scriptPaths.append(scriptPath)

        path = "%s/scripts/%s/quick-qsub-align.sh" % (paths["lrcstats"], experimentName)
        with open(path,'w') as file:
		file.write("#!/bin/bash\n")
                for scriptPath in scriptPaths:
                        line = "qsub %s\n" % (scriptPath)
                        file.write(line)
