import job_header

def writeResources(file, genome):
        '''
        Write the resource usage into the job script.
        '''
        resources = ["walltime=3:00:00:00", "mem=16gb", "nodes=1:ppn=8"]

        for resource in resources:
                line = "#PBS -l %s\n" % (resource)
                file.write(line)

	file.write('\n')

def writePaths(file, testDetails):
	'''
	Write the paths to the data.
	Inputs:
        - (file object) file
        - (dict of strings) test: dict of test parameters
	'''
	# Reminder: experimentName is a global variable - initialized in lrcstats.py
	experiment = "experiment=%s\n" % (experimentName)

	lrcstats = "lrcstats=%s\n" % (variables["lrcstats"])

	program = "program=%s\n" % (testDetails["program"])

        genome = "genome=%s\n" % (testDetails["genome"])

        longCov = "longCov=%s\n" % (testDetails["longCov"])

	shortCov = "shortCov=%s\n" % (testDetails["shortCov"])

        prefix = "prefix=%s/${genome}/${experiment}\n" % (variables["data"])

	test = "test=${program}-${genome}-${shortCov}Sx${longCov}L\n"

	line = experiment + lrcstats + program + genome + longCov + prefix + test 
        file.write(line)
	
	line = "outputDir=${prefix}/align/${program}/${test}\n" \
		"inputDir=${prefix}/correct/${program}/${test}\n" \
		"maf=${prefix}/simulate/simlord/long-d${longCov}/${genome}-long-d${longCov}.fastq.sam.maf\n" \
		"\n" \
		"set -e\n" \
		"mkdir -p ${outputDir}\n" \
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
		"python $sortfasta -i $input -o $sortedOutput\n"
		"\n" \
		"input=$sortedOutput\n" \
		"\n" 
	file.write(line)	

def writePruneMaf(file):
	'''
	Write the commands to prune the MAF file
	'''
	line = "############### Prune the maf file(s) ###########\n" \
		"echo 'Pruning MAF file(s)...'\n") \
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
		"align=${lrcstats}/src/collection/align\n" \
		"mafOutput=${outputDir}/${test}.maf\n" \
		"\n"
	file.write(line)

	if program in ["jabba", "proovread"]:
		command = "$align maf -m $maf -c $input -t -o $mafOutput\n" \
			"\n"
		file.write(command)
	elif program in ["lordec", "colormap", "colormap_oea"]:
		command = "$align maf -m $maf -c $input -o $mafOutput\n" \
			"\n"
		file.write(command)

	line = "maf=${mafOutput}\n" \
		"\n"
	file.write(line)

def writeConvertFastq2Fasta(file):
	'''
	Write the commands for FASTQ2FASTA script
	'''
	line = "############### Convert FASTQ to FASTA ###########\n" \
		"echo 'Converting FASTQ to FASTA...'\n" \
		"\n" \
		"fastq2fasta=${lrcstats}/src/preprocessing/fastq2fasta/fastq2fasta.py\n" \
		"outputq2a=$outputdir/${test}\n" \
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
	inputfasta="input=${inputDir}/${test}.fasta\n"
	file.write(inputfasta)

	writeSortFasta(file)
	writePruneMaf(file)
	writeAlignment(file, testDetails["program"])

def writeJabba(file, testDetails):
	'''
	Write the commands for jabba alignment
	'''
	inputFastq="input=${inputDir}/jabba/Jabba-${genome}-long-d${longCov}.fastq\n"
	file.write(inputFastq)
	writeConvertFastq2Fasta(file)
	writeProcessedTrimmedReads(file)
	writePruneMaf(file)
	writeAlignment(file, testDetails["program"])

def writeProovread(file, testDetails):
	'''
	Write the commands for proovread alignment
	'''
	inputfasta="input=${inputDir}/${test}.trimmed.fa\n"
	file.write(inputFasta)
	writeProcessedTrimmedReads(file)
	writePruneMaf(file)
	writeAlignment(file, testDetails["program"])

def writeColormap(file, testDetails):
	'''
	Write the commands for colormap w/o OEA
	'''
	inputfasta="input=${inputDir}/${test}_corr.fa\n" 
	file.write(inputFasta)
	writeSortFasta(file)
	writePruneMaf(file)
	writeAlignment(file, testDetails["program"])

def writeColormapOea(file, testDetails):
	'''
	Write the commands for colormap w/ OEA
	'''
	inputfasta="input=${inputDir}/${test}_oea.fa\n"
	file.write(inputfasta)
	writeSortFasta(file)
	writePruneMaf(file)
	writeAlignment(file, testDetails["program"])

def generateAlignmentJob(testDetails):
	'''
	Generates a PBS job script for cLR, uLR and ref alignments.
	Input
	- (dict of strings) test: dict of test parameters
	'''
	testName = "%s-%s-%sSx%sL" \
		% (testDetails["program"], testDetails["genome"], \
			 testDetails["shortCov"], testDetails["longCov"])
	scriptPath = "%s/scripts/%s/align/%s/%s-correct.pbs" \
		% (variables["lrcstats"], experimentName, testDetails["program"], testName)
	with open(scriptPath, 'w') as file:
		job_header.writeHeader(file)
		jobOutputPath = "#PBS -o %s/%s/%s/align/%s/%s/%s.out" \
                        % (variables["data"], test["genome"], experimentName, test["program"], testName, testName)
                file.write(jobOutputPath)

		jobName = "#PBS -N %s-align\n" % (testName)
                file.write(jobName)

		writeResources(file)
		writePaths(file, testDetails)
		
		line = "set -e\n" \
                        "\n"
                file.write(line)

		program = testDetails["program"]

                if program == "colormap":
                        writeColormap(file)
                elif program == "colormap_oea":
                        writeColormapOea(file)
                elif program == "proovread":
                        writeProovread(file)
                elif program == "lordec":
                        writeLordec(file)
                elif program == "jabba":
                        writeJabba(file)
