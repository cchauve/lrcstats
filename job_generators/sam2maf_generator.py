import sys, getopt, datetime

def writeJob(species, coverage):
	filename = "%s-d%s_sam2maf.pbs" % (species, coverage)

	with open(filename, 'w') as file:
		resources = ["walltime=24:00:00", "mem=16gb", "nodes=1:ppn=1"]
		folder="/global/scratch/seanla/Data/%s" % (species)
		dir = "%s/simlord/long-d%s" % (folder, coverage)

		file.write("#!/bin/bash\n")

		for resource in resources:
			line = "#PBS -l %s\n" % (resource)
			file.write(line)

		file.write("#PBS -l epilogue=/home/seanla/Jobs/epilogue.script\n")
        	file.write("#PBS -M laseanl@sfu.ca\n")
        	file.write("#PBS -m ea\n")
        	file.write("#PBS -j oe\n")

       		outlog = "#PBS -o %s/%s-d%s_sam2maf.out\n" %(dir, species, coverage)
        	file.write(outlog)

        	jobName = "#PBS -N %s\n\n" % (test)
       	 	file.write(jobName)

		if species is "ecoli":
			ref = "ref=%s/escherichia-coli_reference.fasta\n" % (species)
		elif species is "yeast":
			ref = "ref=%s/saccharomyces-cerevisiae-chromosome1_sequence.fasta\n" % (species)
		else:
			ref = "ref=%s/%s_reference.fasta\n" % (species, species)

		file.write(ref)

		sam = "sam=%s/%s-long-d%s.fastq.sam\n" % (dir, species, coverage)
		file.write(sam)

		maf = "maf=%s.maf\n" % (sam)	
		file.write(maf)

		sam2maf = "sam2maf=/home/seanla/Projects/lrcstats/src/preprocessing/sam2maf\n"
		file.write(sam2maf)

		command = "$sam2maf -r $ref -s $sam -o $maf\n"
		file.write(command)
	

if __name__ == "__main__":
        helpMessage = "Generate PBS job scripts to convert sam files to maf files."
        usageMessage = "Usage: %s [-h help and usage] [-a do all coverages] [-e ecoli] [-y yeast] [-f fly] [-l long read coverage]" % (sys.argv[0])

        options = "heyfl:"

        try:
                opts, args = getopt.getopt(sys.argv[1:], options)
        except getopt.GetoptError:
                print "Error: unable to read command line arguments."
                sys.exit(2)

        if len(sys.argv) == 1:
                print usageMessage
                sys.exit(2)

	coverage = None
	allCov = False

	doYeast = False
	doEcoli = False
	doFly = False

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
		elif opt == '-l':
			coverage = str(arg)

	optsIncomplete = False

	if not doEcoli and not doYeast and not doFly:
		optsIncomplete = True
		print "Please select at least one species to convert sam to maf."
	if coverage is None and not allCov:
		optsIncomplete = True
		print "Please indicate which coverages you would like to do."

	# Do all long coverages
	if allCov:
		coverages = ['10', '20', '50', '75']
	else:
		coverages.append(coverage)

	# yes, specie is not the proper singular form of species, but im lazy
	for coverage in coverages:
		for specie in species:
			writeJob(specie, coverage)	

	submitFile = "/home/seanla/Jobs/lrcstats/sam2maf/submitjobs.sh" 

	# Create the shell script to execute all jobs
	with open(submitFile, 'w') as file:
		file.write("#!/bin/bash\n\n")
		for coverage in coverages:
			for specie in species:
				filename = "%s-d%s_sam2maf.pbs" % (specie, coverage)
				file.write( "qsub %s\n" % (filename) )
