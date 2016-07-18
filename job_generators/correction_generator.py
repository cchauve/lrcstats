import sys, getopt, datetime

def writeJob(program, species, shortCov, longCov):
	################ Various variables ##########################
	now = datetime.datetime.now()
	test = "%s-%s-%sSx%sL" % (program, species, shortCov, longCov)
	# LoRDeC uses more memory than other programs
	if program is "lordec":
		if int(shortCov) >= 200:
			mem = 64
		else:
			mem = 48
	else:
		mem = 32
	resources = ["walltime=24:00:00", "mem=%dgb" % (mem), "nodes=1:ppn=8"]
	################## Data paths #################################
	prefix = "/global/scratch/seanla/Data/%s" % (species)
	art = "%s/art" % (prefix)
	short1 = "%s/short-paired-d%s/%s-short-paired-d%s1.fastq" % (art, shortCov, species, shortCov)
	short2 = "%s/short-paired-d%s/%s-short-paired-d%s2.fastq" % (art, shortCov, species, shortCov)
	mergedShort = "%s/short-paired-d%s/%s-short-paired-d%s-merged.fastq" % (art, shortCov, species, shortCov)

	long = "%s/simlord/long-d%s/%s-long-d%s.fastq" % (prefix, longCov, species, longCov) 
	outputdir = "%s/corrections/%s/%s/%s/%s" % (prefix, now.month, now.day, program, test)
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

	outlog = "#PBS -o /global/scratch/seanla/Data/%s/corrections/%s/%s/%s/%s/%s.out\n" %(species, now.month, now.day, program, test, test) 
	file.write(outlog)

	jobName = "#PBS -N %s\n\n" % (test)
	file.write(jobName)
	###############################################################

	file.write("set -e\n")
	mkdir = "mkdir -p %s\n" % (outputdir)

	file.write(mkdir)

	############## Write program specific commands ###############
	if program is "lordec":
		output = "%s/%s.fasta" % (outputdir, test)
		dir = "cd /home/seanla/Software/LoRDEC-0.6\n\n"
		command = "./lordec-correct -T ${PBS_NUM_PPN} --trials 5 --branch 200 --errorrate 0.4 -2 %s %s -k 19 -s 3 -i %s -o %s" % (short1, short2, long, output)
		file.write(dir)
		file.write(command)

	if program is "jabba":
		karectOutput = "%s/karect" % (outputdir)
		mkdir = "mkdir -p %s\n" % (karectOutput)
		file.write(mkdir)

		brownieOutput = "%s/brownie" % (outputdir)
		mkdir = "mkdir -p %s\n" % (brownieOutput)
		file.write(mkdir)

		jabbaOutput = "%s/jabba" % (outputdir)
		mkdir = "mkdir -p %s\n" % (jabbaOutput)
		file.write(mkdir)

		karectCommand = "/home/seanla/Software/karect/karect -correct -inputfile=%s -inputfile=%s -resultdir=%s -tempdir=%s -celltype=haploid -matchtype=hamming -threads=${PBS_NUM_PPN}\n\n" % (short1, short2, karectOutput, karectOutput)
		file.write(karectCommand)

		karectShort1="%s/karect_%s-short-paired-d%s1.fastq" % (karectOutput, species, shortCov)
		karectShort2="%s/karect_%s-short-paired-d%s2.fastq" % (karectOutput, species, shortCov)

		brownieCommand = "/home/seanla/Software/brownie/brownie graphCorrection -k 75 -p %s %s %s\n\n" % (brownieOutput, karectShort1, karectShort2)
		file.write(brownieCommand)

		dbgraph = "%s/DBGraph.fasta" % (brownieOutput)
		jabbaCommand = "/home/seanla/Software/jabba/jabba -t ${PBS_NUM_PPN} -l 20 -k 75 -o %s -g %s -fastq %s" % (jabbaOutput, dbgraph, long) 
		file.write(jabbaCommand)

	if program is "proovread":
		output = "%s/%s" % (outputdir, test)

		bwaIndex = "/home/seanla/Software/proovread/util/bwa/bwa-proovread index %s\n\n" % (long)
		file.write(bwaIndex)

		samPath = "%s/sam" %(outputdir)
		mkdir = "mkdir -p %s\n\n" % (samPath)
		file.write(mkdir)

		sam = "%s/%s-%sSx%sL.sam" % (samPath, species, shortCov, longCov)

		bwaMem = "/home/seanla/Software/proovread/util/bwa/bwa-proovread mem %s %s %s > %s\n\n" % (long, short1, short2, sam) 
		file.write(bwaMem)
			
		bam = "%s.bam" % (sam)
		samtools = "/global/software/samtools/samtools13/bin/samtools sort -T %s -o %s %s\n\n" % (samPath, bam, sam) 
		file.write(samtools)
			
		dir = "cd /home/seanla/Software/proovread/bin\n\n"
		command = "./proovread -t ${PBS_NUM_PPN} --lr-qv-offset 70 --bam %s -l %s -p %s" % (bam, long, output)
		file.write(dir)
		file.write(command)

	if program is "colormap":
		colormapPath = "colormap=/home/seanla/Software/colormap/runBoth.sh\n"
		short1path = "short1=%s\n" % (short1)
		short2path = "short2=%s\n" % (short2)
		output = "outputDir=%s\n" % (outputdir)
		mergedShortPath = "mergedShort=%s\n" % (mergedShort)
		longPath = "long=%s\n" % (long)
		cdCommand = "cd $outputDir\n"
		colormap = "$colormap $long $mergedShort $outputDir ${PBS_NUM_PPN}\n" 

		file.write(colormapPath)
		file.write(short1path)
		file.write(short2path)
		file.write(output)
		file.write(mergedShortPath)
		file.write(longPath)
		file.write('\n')
		file.write(cdCommand)
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
