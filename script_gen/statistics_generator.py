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

def writePaths(file, test):
	'''
	Write the paths to the data.
	Inputs:
        - (file object) file
        - (dict of strings) test: dict of test parameters
	'''
	lrcstats = "lrcstats=%s\n" % (variables["lrcstats"])

	program = "program=%s\n" % (test["program"])

        genome = "genome=%s\n" % (test["genome"])

        longCov = "longCov=%s\n" % (test["longCov"])

        prefix = "prefix=%s/${genome}\n" % (variables["data"])


	line = lrcstats + program + genome + longCov + prefix + test 
        file.write(line)
	
	line = "outputDir=${prefix}/alignments/${program}/${test}\n" \
		"inputDir=${prefix}/corrections/${program}/${test}\n" \
		"maf=${prefix}/simlord/long-d${longCov}/${genome}-long-d${longCov}.fastq.sam.maf\n" \
		"\n" \
		"set -e\n" \
		"mkdir -p ${outputDir}\n"
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

def writeLordec(file, test):
	'''
	Write the commands for lordec alignment
	'''
	inputfasta="input=$inputdir/${test}.fasta\n"
	file.write(inputfasta)

	writeSortFasta(file)
	writePruneMaf(file)

def writeJob(program, species, shortCov, longCov):

	if program is "jabba":
		inputfasta="input=$inputdir/jabba/Jabba-%s-long-d%s.fastq\n" % (species, longCov)
	if program is "proovread":
		inputfasta="input=$inputdir/%s/%s.trimmed.fa\n" % (test, test)
	if program is "colormap":
		inputOea="inputOea=$inputdir/%s_oea.fa\n" % (test)
		file.write(inputOea)
		inputfasta="input=$inputdir/%s_corr.fa\n" % (test)
	file.write(inputfasta)
	file.write('\n')

	if program is "jabba":
		file.write("############### Convert FASTQ to FASTA ###########\n")
		file.write("echo 'Converting FASTQ to FASTA...'\n\n")

		fastq2fasta = "fastq2fasta=$preprocesspath/fastq2fasta/fastq2fasta.py\n"
		file.write(fastq2fasta)

		q2aOutPrefix = "outputq2a=$outputdir/%s\n\n" % (test)
		file.write(q2aOutPrefix)

		fastq2fastaCommand = "python $fastq2fasta -i $input -o $outputq2a\n\n" 
		file.write(fastq2fastaCommand)
	
		inputfasta = "input=${outputq2a}.fasta\n"
		file.write(inputfasta)
		
	if program in ["lordec", "colormap"]:
		file.write("############### Sort FASTA ###########\n")
		file.write("echo 'Sorting FASTA file...'\n\n")

		sortPath = "sortfasta=$preprocesspath/sortfasta/sortfasta.py\n"
		file.write(sortPath)

		sortOutputLine = "sortoutput=$outputdir/sorted.fasta\n\n" 	
		file.write(sortOutputLine)

		sortCommand = "python $sortfasta -i $input -o $sortoutput\n\n"
		file.write(sortCommand)
	
		inputLine = "input=$sortoutput\n\n"
		file.write(inputLine)
	
	if program is "colormap":
		sortOutputLineOea = "sortoutputoea=$outputdir/sorted_oea.fasta\n"
		file.write(sortOutputLineOea)

		sortCommand = "python $sortfasta -i $inputOea -o $sortoutputoea\n\n"
		file.write(sortCommand)

		inputOea = "inputOea=$sortoutputoea\n\n"
		file.write(inputOea)

	if program in ["proovread", "jabba"]:
		file.write("############### Processing Trimmed Reads ###########\n")
		file.write("echo 'Processing trimmed reads...'\n")
		
		processPath = "concatenate=$preprocesspath/concatenate_trimmed/concatenate_trimmed.py\n"
		file.write(processPath)

		processOutput = "concatenated_output=$outputdir/concatenated.fasta\n\n"
		file.write(processOutput)

		processCommand = "python $concatenate -i $input -o $concatenated_output\n\n"
		file.write(processCommand)

		inputfasta = "input=$concatenated_output\n\n"
		file.write(inputfasta)


	file.write("############### Prune the maf file(s) ###########\n")
	file.write("echo 'Pruning MAF file(s)...'\n")

	prunePath = "prunemaf=$preprocesspath/prunemaf/prunemaf.py\n"
	file.write(prunePath)

	pruneOutput = "pruneOutput=$outputdir/pruned\n\n"
	file.write(pruneOutput)

	pruneCommand = "python $prunemaf -f $input -m $maf -o $pruneOutput\n\n"
	file.write(pruneCommand)

	newMafPath = "maf=${pruneOutput}.maf\n"
	file.write(newMafPath)

	if program is "colormap":
		pruneOutput = "pruneOutputOea=$outputdir/prunedOea\n\n"
		file.write(pruneOutput)

		pruneCommand = "python $prunemaf -f $inputOea -m $mafOea -o $pruneOutputOea\n\n"
		file.write(pruneCommand)

		mafLine = "mafOea=${pruneOutputOea}.maf\n\n"
		file.write(mafLine)

	file.write("############### Generate three-way alignment ###########\n")
	file.write("echo 'Generating three-way alignment...'\n")

	lrcstatsPath = "lrcstats=/home/seanla/Projects/lrcstats/src/collection/lrcstats\n"
	file.write(lrcstatsPath)

	mafOutput = "mafOutput=$outputdir/%s.maf\n\n" % (test)
	file.write(mafOutput)

	if program is "jabba" or program is "proovread":
		command = "$lrcstats maf -m $maf -c $input -t -o $mafOutput\n\n"
		file.write(command)
	elif program is "lordec":
		command = "$lrcstats maf -m $maf -c $input -o $mafOutput\n\n"
		file.write(command)
	else:
		command = "$lrcstats maf -m $maf -c $input -o $mafOutput\n\n"
		file.write(command)

		mafOutputOea = "mafOutputOea=$outputdir/%s_oea.maf\n\n" % (test)
		file.write(mafOutputOea)
	
		command = "$lrcstats maf -m $mafOea -c $inputOea -o $mafOutputOea\n\n"
		file.write(command)

	if program in ["colormap", "jabba"]:
		file.write("############### Removing extended regions #############\n")
		file.write("echo 'Removing extended regions...'\n")

		unextendPath = "unextend=/home/seanla/Projects/lrcstats/src/preprocessing/unextend_alignments/unextend_alignments.py\n"
		file.write(unextendPath)

		unextendOutput = "unextendOutput=$outputdir/%s_unextended.maf\n\n" % (test)
		file.write(unextendOutput)

		unextendCommand = "python $unextend -i $mafOutput -m $unextendOutput\n\n"
		file.write(unextendCommand)

		mafOutput = "mafOutput=$unextendOutput\n\n"
		file.write(mafOutput)

		if program is "colormap":
			unextendOutput = "unextendOutputOea=$outputdir/%s_oea_unextended.maf\n\n" % (test)
			file.write(unextendOutput)

			unextendCommand = "python $unextend -i $mafOutputOea -m $unextendOutputOea\n\n"
			file.write(unextendCommand)

			mafOutput = "mafOutputOea=$unextendOutputOea\n\n"
			file.write(mafOutput)

	file.write("############### Collecting data ###########\n")
	file.write("echo 'Collecting data...'\n")

	statsOutput = "statsOutput=$outputdir/%s.stats\n\n" % (test)
	file.write(statsOutput)

	if program is "jabba" or program is "proovread":
		command = "$lrcstats stats -m $mafOutput -o $statsOutput -t\n\n"
	else:
		command = "$lrcstats stats -m $mafOutput -o $statsOutput\n\n"
	file.write(command)

	if program is "colormap":
		statsOutput = "statsOutputOea=$outputdir/%s_oea.stats\n\n" % (test)
		file.write(statsOutput)

		command = "$lrcstats stats -m $mafOutputOea -o $statsOutputOea\n\n"
		file.write(command)

	file.write("############## Finding global statistics ############\n")
	file.write("echo 'Finding global statistics...'\n\n")
	
	global_stats = "global_stats=/home/seanla/Projects/lrcstats/src/statistics/global_stats.py\n"
	file.write(global_stats)

	globalOutput = "global_stats_output=$outputdir/%s_global_stats.txt\n\n" % (test)
	file.write(globalOutput)

	if program in ['proovread', 'jabba']:
		command = "python $global_stats -i $statsOutput -o $global_stats_output\n\n"
	else:
		command = "python $global_stats -i $statsOutput -o $global_stats_output -b\n\n"
	file.write(command)

	if program is "colormap":
		globalOutput = "global_stats_output_oea=$outputdir/%s_oea_global_stats.txt\n\n" % (test)
		file.write(globalOutput)

		command = "python $global_stats -i $statsOutputOea -o $global_stats_output_oea -b\n\n"
		file.write(command)

	if constructVisualizations:
		file.write("############### Visualizing statistics ###########\n")
		file.write("echo 'Visualizing statistics'\n")

		visualize_stats = "visualize_stats=/home/seanla/Projects/lrcstats/src/statistics/visualize_stats.py\n"
		file.write(visualize_stats)

		command = "python $visualize_stats -i $statsOutput -d $outputdir -n %s\n\n" % (test)
		file.write(command)

		if program is "colormap":
			command = "python $visualize_stats -i $statsOutputOea -d $outputdir -n %s_oea\n\n" % (test)
			file.write(command)

	file.close()

def generateAlignmentJob(test):
	'''
	Generates a PBS job script for cLR, uLR and ref alignments.
	Input
	- (dict of strings) test: dict of test parameters
	'''
	testName = "%s-%s-%sSx%sL" % (test["program"], test["genome"], test["shortCov"], test["longCov"])
	scriptPath = "%s/scripts/align/%s/%s-correct.pbs" % (variables["lrcstats"], test["program"], testName)

	with open(scriptPath, 'w') as file:
		job_header.writeGenericHeader(file)
		jobOutputPath = "#PBS -o %s/%s/alignments/%s/%s/%s.out" \
                        % (variables["data"], test["genome"], test["program"], testName, testName)
                file.write(jobOutputPath)

		jobName = "#PBS -N %s-align\n" % (testName)
                file.write(jobName)

		writeResources(file)
		writePaths(file, test)
		
		line = "set -e\n" \
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
