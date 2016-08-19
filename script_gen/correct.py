import datetime

def writeJob(program, species, shortCov, longCov):
	################ Various variables ##########################
	now = datetime.datetime.now()
	test = "%s-%s-%sSx%sL" % (program, species, shortCov, longCov)
	# LoRDeC uses more memory than other programs
	if species == "fly":
		mem = 200 
	elif program is "lordec":
		if int(shortCov) >= 200:
			mem = 64
		else:
			mem = 48
	else:
		mem = 32
	resources = ["walltime=3:00:00:00", "mem=%dgb" % (mem), "nodes=1:ppn=8"]
	###############################################################
	
	filename = "/home/seanla/Jobs/lrcstats/corrections/%s.pbs" % (test)
	file = open(filename, 'w')
	
	################### Write the resources #######################
	file.write("#!/bin/bash\n")
	for resource in resources:
		line = "#PBS -l %s\n" %(resource)
		file.write(line)
	###############################################################

	######## Write other important information for job ############
	file.write("#PBS -l epilogue=/home/seanla/Jobs/epilogue.script\n")
	file.write("#PBS -M laseanl@sfu.ca\n")
	file.write("#PBS -m ea\n")
	file.write("#PBS -j oe\n")

	outputdir = "/global/scratch/seanla/Data/%s/corrections/%s/%s/%s/%s" % (species, now.month, now.day, program, test)

	outlog = "#PBS -o %s/%s.out\n" % (outputdir, test)
	file.write(outlog)

	jobName = "#PBS -N %s-correction\n" % (test)
	file.write(jobName)

	file.write('\n')
	###############################################################

	file.write("set -e\n")
	file.write('\n')

	################## Data paths #################################
	test = "test=%s\n" % (test)
	file.write(test)

	species = "species=%s\n" % (species)
	file.write(species)

	prefix = "prefix=/global/scratch/seanla/Data/${species}\n"
	file.write(prefix)

	shortCov = "shortCov=%s\n" % (shortCov)
	file.write(shortCov)

	longCov = "longCov=%s\n" % (longCov)
	file.write(longCov)

	art = "art=$prefix/art/short-paired-d${shortCov}\n"
	file.write(art)


	if program is "colormap":
		mergedShort = "mergedShort=$art/${species}-short-paired-d${shortCov}-merged.fastq\n"
		file.write(mergedShort)
	else:
		short1 = "short1=$art/${species}-short-paired-d${shortCov}1.fastq\n" 
		file.write(short1)

		short2 = "short2=$art/${species}-short-paired-d${shortCov}2.fastq\n"
		file.write(short2)

	long = "long=$prefix/simlord/long-d${longCov}/${species}-long-d${longCov}.fastq\n"
	file.write(long)

	outputdir = "outputDir=%s\n" % (outputdir)
	file.write(outputdir)
	
	mkdir = "mkdir -p $outputDir\n"
	file.write(mkdir)

	file.write('\n')

	############## Write program specific commands ###############
	if program is "lordec":
		output = "output=$output/$test.fasta"

		dir = "cd $outputDir\n\n"
		file.write(dir)

		programPath = "lordec=/home/seanla/Software/LoRDEC-0.6/lordec-correct\n"
		file.write(programPath)

		command = "$lordec -T ${PBS_NUM_PPN} --trials 5 --branch 200 --errorrate 0.4 -2 $short1 $short2 -k 19 -s 3 -i $long -o $output"
		file.write(command)

	if program is "jabba":
		karectOutput = "karectDir=$outputDir/karect\n"
		file.write(karectOutput)

		brownieOutput = "brownieDir=$outputDir/brownie\n"
		file.write(brownieOutput)

		jabbaOutput = "jabbaDir=$outputDir/jabba\n"
		file.write(jabbaOutput)

		file.write('\n')

		mkdir = "mkdir -p $karectDir\n"
		file.write(mkdir)

		mkdir = "mkdir -p $brownieDir\n"
		file.write(mkdir)

		mkdir = "mkdir -p $jabbaDir\n"
		file.write(mkdir)

		file.write('\n')

		karectPath = "karect=/home/seanla/Software/karect/karect\n"
		file.write(karectPath)

		karectCommand = "$karect -correct -inputfile=$short1 -inputfile=$short2 -resultdir=$karectDir -tempdir=$karectDir -celltype=haploid -matchtype=hamming -threads=${PBS_NUM_PPN}\n"
		file.write(karectCommand)
		
		file.write('\n')

		karectShort1="short1=$karectDir/karect_${species}-short-paired-d${shortCov}1.fastq\n"
		file.write(karectShort1)

		karectShort2="short2=$karectDir/karect_${species}-short-paired-d${shortCov}2.fastq\n"
		file.write(karectShort2)

		browniePath= "brownie=/home/seanla/Software/brownie/brownie\n"
		file.write(browniePath)

		file.write('\n')

		brownieCommand = "$brownie graphCorrection -k 75 -p $short1 $short2 $brownieDir\n"
		file.write(brownieCommand)

		file.write('\n')

		removeKarect = "rm -r $karectDir\n"
		file.write(removeKarect)

		dbgraph = "dbGraph=$brownie/DBGraph.fasta\n"
		file.write(dbgraph)

		jabbaPath = "jabba=/home/seanla/Software/jabba/jabba\n"
		file.write(jabbaPath)

		file.write('\n')

		jabbaCommand = "$jabba -t ${PBS_NUM_PPN} -l 20 -k 75 -o $jabbaDir -g $dbGraph -fastq $long\n"
		file.write(jabbaCommand)

		file.write('\n')

		removeBrownie = "rm -r $brownieDir\n"
		file.write(removeBrownie)

	if program is "proovread":
		output = "output=$outputDir/$test\n"
		file.write(output)

		proovread = "proovread=/home/seanla/Software/proovread/bin/proovread\n"
		file.write(proovread)

		file.write('\n')

		command = "$proovread -t ${PBS_NUM_PPN} --lr-qv-offset 70 -s $short1 -s $short2 -l $long -p $output\n"
		file.write(command)

		file.write('\n')

		removeSam = "rm -r $samPath\n"

	if program is "colormap":
		colormapPath = "colormap=/home/seanla/Software/colormap/runBoth.sh\n"
		file.write(colormapPath)

		file.write('\n')

		cdCommand = "cd $outputDir\n"
		file.write(cdCommand)

		colormap = "$colormap $long $mergedShort $outputDir ${PBS_NUM_PPN}\n" 
		file.write(colormap)

	file.close()

if __name__ == "__main__":
        helpMessage = "Generate  PBS job scripts."
        usageMessage = "Usage: %s [-h help and usage] [-a do all coverages] [-f fly] [-e ecoli] [-y yeast] [-c CoLoRMap] [-d LoRDeC] [-j Jabba] [-p proovread] [-s short read coverage] [-l long read coverage]" % (sys.argv[0])

        options = "hafeycdjps:l:"

        try:
                opts, args = getopt.getopt(sys.argv[1:], options)
        except getopt.GetoptError:
                print "Error: unable to read command line arguments."
                sys.exit(2)

        if len(sys.argv) == 1:
                print usageMessage
                sys.exit(2)

	shortCov = None
	longCov = None

	doYeast = False
	doEcoli = False
	doFly = False

	doLordec = False
	doJabba = False
	doProovread = False
	doColormap = False

	allCov = False

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

	optsIncomplete = False

	if shortCov is None and allCov is False:
		print "Please input the short coverage."
		optsIncomplete = True
	if longCov is None and allCov is False:
		print "Please input the required long coverage."
		optsIncomplete = True
	if not doYeast and not doEcoli and not doFly:
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
		submitFile = "/home/seanla/Jobs/lrcstats/corrections/submitjobs-%s%s%s%s-all.sh" % (colormap, lordec, jabba, proovread)
	else:
		submitFile = "/home/seanla/Jobs/lrcstats/corrections/submitjobs-%s%s%s%s-%sSx%sL.sh" % (colormap, lordec, jabba, proovread, shortCov, longCov)

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
