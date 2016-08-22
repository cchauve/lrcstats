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

def writePaths(file, test_details):
	'''
	Write the paths to the data.
	Inputs:
        - (file object) file
        - (dict of strings) test: dict of test parameters
	'''
	lrcstats = "lrcstats=%s\n" % (variables["lrcstats"])

	program = "program=%s\n" % (test_details["program"])

        genome = "genome=%s\n" % (test_details["genome"])

        long_cov = "long_cov=%s\n" % (test_details["long_cov"])

	short_cov = "short_cov=%s\n" % (test_details["short_cov"])

        prefix = "prefix=%s/${genome}\n" % (variables["data"])

	test = "test=${program}-${genome}-${short_cov}Sx${long_cov}L\n"

	line = lrcstats + program + genome + long_cov + prefix + test 
        file.write(line)
	
	line = "outputDir=${prefix}/alignments/${program}/${test}\n" \
		"inputDir=${prefix}/corrections/${program}/${test}\n" \
		"maf=${prefix}/simlord/long-d${long_cov}/${genome}-long-d${long_cov}.fastq.sam.maf\n" \
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
		"sortfasta=$lrcstats/src/preprocessing/sortfasta/sortfasta.py\n" \
		"sortedOutput=$outputDir/sorted.fasta\n" \
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
		"prunemaf=${lrcstats}/src/preprocess/prunemaf/prunemaf.py\n" \
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
		"concatenated_output=$outputdir/concatenated.fasta\n" \
		"\n" \
		"python $concatenate -i $input -o $concatenated_output\n" \
		"\n" \
		"input=$concatenated_output\n" \
		"\n"
	file.write(line)

def writeAlignment(file, program):
	'''
	Write the commands to create a three-way alignment
	between the cLR, uLR and ref
	'''
	line = "############### Generate three-way alignment ###########\n" \
		"echo 'Generating three-way alignment...'\n" \
		"lrcstats=/home/seanla/Projects/lrcstats/src/collection/lrcstats\n" \
		"mafOutput=${outputDir}/${test}.maf\n" \
		"\n"
	file.write(line)

	if program in ["jabba", "proovread"]:
		command = "$lrcstats maf -m $maf -c $input -t -o $mafOutput\n" \
			"\n"
		file.write(command)
	elif program in ["lordec", "colormap", "colormap_oea"]:
		command = "$lrcstats maf -m $maf -c $input -o $mafOutput\n" \
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
		"fastq2fasta=$preprocesspath/fastq2fasta/fastq2fasta.py\n" \
		"outputq2a=$outputdir/${test}\n" \
		"\n" \
		"python $fastq2fasta -i $input -o $outputq2a\n" \
		"\n" \
		"input=${outputq2a}.fasta\n" \
		"\n"
	file.write(line)

def writeLordec(file, test_details):
	'''
	Write the commands for lordec alignment
	'''
	inputfasta="input=${inputDir}/${test}.fasta\n"
	file.write(inputfasta)

	writeSortFasta(file)
	writePruneMaf(file)
	writeAlignment(file, test_details["program"])

def writeJabba(file, test_details):
	'''
	Write the commands for jabba alignment
	'''
	inputFastq="input=${inputDir}/jabba/Jabba-${genome}-long-d${long_cov}.fastq\n"
	file.write(inputFastq)
	writeConvertFastq2Fasta(file)
	writeProcessedTrimmedReads(file)
	writePruneMaf(file)
	writeAlignment(file, test_details["program"])

def writeProovread(file, test_details):
	'''
	Write the commands for proovread alignment
	'''
	inputfasta="input=${inputDir}/${test}.trimmed.fa\n"
	file.write(inputFasta)
	writeProcessedTrimmedReads(file)
	writePruneMaf(file)
	writeAlignment(file, test_details["program"])

def writeColormap(file, test_details):
	'''
	Write the commands for colormap w/o OEA
	'''
	inputfasta="input=${inputDir}/${test}_corr.fa\n" 
	file.write(inputFasta)
	writeSortFasta(file)
	writePruneMaf(file)
	writeAlignment(file, test_details["program"])

def writeColormapOea(file, test_details):
	'''
	Write the commands for colormap w/ OEA
	'''
	inputfasta="input=${inputDir}/${test}_oea.fa\n"
	file.write(inputfasta)
	writeSortFasta(file)
	writePruneMaf(file)
	writeAlignment(file, test_details["program"])

def generateAlignmentJob(test_details):
	'''
	Generates a PBS job script for cLR, uLR and ref alignments.
	Input
	- (dict of strings) test: dict of test parameters
	'''
	test_name = "%s-%s-%sSx%sL" \
		% (test_details["program"], test_details["genome"], \
			 test_details["short_cov"], test_details["long_cov"])
	scriptPath = "%s/scripts/align/%s/%s-correct.pbs" \
		% (variables["lrcstats"], test_details["program"], test_name)
	with open(scriptPath, 'w') as file:
		job_header.writeHeader(file)
		jobOutputPath = "#PBS -o %s/%s/alignments/%s/%s/%s.out" \
                        % (variables["data"], test["genome"], test["program"], test_name, test_name)
                file.write(jobOutputPath)

		job_name = "#PBS -N %s-align\n" % (test_name)
                file.write(job_name)

		writeResources(file)
		writePaths(file, test_details)
		
		line = "set -e\n" \
                        "\n"
                file.write(line)

                if test_details["program"] == "colormap":
                        writeColormap(file)
                elif test_details["program"] == "colormap_oea":
                        writeColormapOea(file)
                elif test_details["program"] == "proovread":
                        writeProovread(file)
                elif test_details["program"] == "lordec":
                        writeLordec(file)
                elif test_details["program"] == "jabba":
                        writeJabba(file)
