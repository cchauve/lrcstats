import sys, getopt, datetime

def writeJob(program, species, shortCov, longCov):
	################ Various variables ##########################
	test = "%s-%s-%sSx%sL" % (program, species, shortCov, longCov)
	
	filename = "/home/seanla/Jobs/lrcstats/statistics/%s.pbs" % (test)
	file = open(filename, 'w')
	
	################### Write the resources #######################
	file.write("#!/bin/bash\n")
	resources = ["walltime=3:00:00:00", "mem=8gb", "nodes=1:ppn=4"]
	for resource in resources:
		line = "#PBS -l %s\n" %(resource)
		file.write(line)
	###############################################################

	######## Write other important information for job ############
	file.write("#PBS -l epilogue=/home/seanla/Jobs/epilogue.script\n")
	file.write("#PBS -M laseanl@sfu.ca\n")
	file.write("#PBS -m ea\n")
	file.write("#PBS -j oe\n")

	outlog = "#PBS -o /global/scratch/seanla/Data/%s/statistics/%s/%s/%s.out\n" %(species, program, test, test) 
	file.write(outlog)

	jobName = "#PBS -N %s-statistics\n\n" % (test)
	file.write(jobName)
	###############################################################

	################## Data paths #################################
	prefix = "/global/scratch/seanla/Data/%s" % (species)
	prefixLine = "prefix=%s\n" % (prefix)
	file.write(prefixLine)

	outputdir = "%s/statistics/%s/%s" % (prefix, program, test)
	outputdirLine = "outputdir=%s\n" % (outputdir)
	file.write(outputdirLine)

	maf = "%s/simlord/long-d%s/%s-long-d%s.fastq.sam.maf" % (prefix, longCov, species, longCov)
	mafLine = "maf=%s\n" % (maf)
	file.write(mafLine)

	if program is "colormap":
		mafOeaLine = "mafOea=$maf\n"
		file.write(mafOeaLine)

	file.write("\n")
	###############################################################

	# Script ends immediately if error
	file.write("set -e\n")

	mkdir = "mkdir -p %s\n\n" % (outputdir)
	file.write(mkdir)

	preprocess = "/home/seanla/Projects/lrcstats/src/preprocessing"
	preprocessPath = "preprocesspath=%s\n" % (preprocess)
	file.write(preprocessPath)

	inputdir = "inputdir=$prefix/corrections/%s/%s\n" % (program, test)
	file.write(inputdir)

	if program is "lordec":
		inputfasta="input=$inputdir/%s.fasta\n" % (test)
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

if __name__ == "__main__":
        helpMessage = "Generate PBS job scripts."
        usageMessage = "Usage: %s [-h help and usage] [-a do all coverages] [-e ecoli] [-y yeast] [-f fly] [-c CoLoRMap] [-d LoRDeC] [-j Jabba] [-p proovread] [-s short read coverage] [-l long read coverage] [-v construct visualizations]" % (sys.argv[0])

        options = "haeycdjps:l:fv"

        try:
                opts, args = getopt.getopt(sys.argv[1:], options)
        except getopt.GetoptError:
                print "Error: unable to read command line arguments."
                sys.exit(2)

        if len(sys.argv) == 1:
                print usageMessage
                sys.exit(2)

	allCov = False
	shortCov = None
	longCov = None

	doYeast = False
	doEcoli = False
	doFly = False

	doLordec = False
	doJabba = False
	doProovread = False
	doColormap = False
	
	constructVisualizations = False

        for opt, arg in opts:
                # Help message
                if opt == '-h':
                        print helpMessage
                        print usageMessage
                        sys.exit()
                elif opt == '-e':
                        doEcoli = True
                elif opt == '-y':
                        doYeast = True
		elif opt == '-f':
			doFly = True
		elif opt == '-s':
			shortCov = str(arg)
		elif opt == '-l':
			longCov = str(arg)
		elif opt == '-d':
			doLordec = True
		elif opt == '-j':
			doJabba = True
		elif opt == '-p':
			doProovread = True
		elif opt == '-a':
			allCov = True
		elif opt == '-c':
			doColormap = True
		elif opt == '-v':
			constructVisualizations = True

	optsIncomplete = False

	if shortCov is None and allCov is False:
		print "Please input the short coverage."
		optsIncomplete = True
	if longCov is None and allCov is False:
		print "Please input the required long coverage."
		optsIncomplete = True
	if not doYeast and not doEcoli and doFly:
		print "Please indicate which species you would like to test."
		optsIncomplete = True
	if not doColormap and not doLordec and not doJabba and not doProovread:
		print "Please select a program to use."
		optsIncomplete = True

	if optsIncomplete:
		print usageMessage
		sys.exit(2)

	species = []
	programs = []
	shortCovs = []
	longCovs = []

	proovread = ""
	jabba = ""
	lordec = ""
	colormap = ""

	if doYeast:
		species.append("yeast")
	if doEcoli:
		species.append("ecoli")
	if doFly:
		species.append("fly")

	if doLordec:
		programs.append("lordec")
		lordec = "l"	
	if doJabba:
		programs.append("jabba")
		jabba = "j"	
	if doProovread:
		programs.append("proovread")
		proovread = "p"
	if doColormap:
		programs.append("colormap")
		colormap = "c"

	# Do all the short and long coverages
	if allCov:
		shortCovs = ['50', '100', '200']
		longCovs = ['10', '20', '50', '75']
	else:
		shortCovs.append(shortCov)
		longCovs.append(longCov)

	# yes, specie is not the proper singular form of species, but im lazy
	for shortCov in shortCovs:
		for longCov in longCovs:
			for specie in species:
				for program in programs:
					writeJob(program, specie, shortCov, longCov)	

	if allCov:	
		submitFile = "/home/seanla/Jobs/lrcstats/statistics/submitjobs-%s%s%s%s-all.sh" % (colormap, lordec, jabba, proovread)
	else:
		submitFile = "/home/seanla/Jobs/lrcstats/statistics/submitjobs-%s%s%s%s-%sSx%sL.sh" % (colormap, lordec, jabba, proovread, shortCov, longCov)

	# Create the shell script to execute all jobs
	with open(submitFile, 'w') as file:
		file.write("#!/bin/bash\n\n")
		for shortCov in shortCovs:
			for longCov in longCovs:
				for specie in species:
					for program in programs:
						test = "%s-%s-%sSx%sL" % (program, specie, shortCov, longCov)
						filename = "%s.pbs" % (test)
						file.write( "qsub %s\n" % (filename) )
