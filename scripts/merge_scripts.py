import sys, getopt, datetime

def writeMergeShortScript(species, shortcov):
	filePath = "/home/seanla/Jobs/lrcstats/merge/merge-%s-short-d%s.pbs" % (species, shortcov)
	file = open(filePath, 'w')

	resources = ["walltime=00:30:00", "mem=4gb", "nodes=1:ppn=1"]

	file.write("#!/bin/bash\n")
	for resource in resources:
		line = "#PBS -l %s\n" %(resource)
		file.write(line)

	file.write("#PBS -l epilogue=/home/seanla/Jobs/epilogue.script\n")
	file.write("#PBS -M laseanl@sfu.ca\n")
	file.write("#PBS -m ea\n")
	file.write("#PBS -j oe\n")

	jobName = "merge-%s-short-d%s" % (species, shortcov)
	shortDir = "/global/scratch/seanla/Data/%s/art/short-paired-d%s" % (species, shortcov)

	outlog = "#PBS -o %s/%s.out\n" %(shortDir, jobName) 
	file.write(outlog)

	jobLine = "#PBS -N %s\n\n" % (jobName)
	file.write(jobLine)


	short1 = "short1=%s/%s-short-paired-d%s1.fastq\n" % (shortDir, species, shortcov)
	file.write(short1)

	short2 = "short2=%s/%s-short-paired-d%s2.fastq\n" % (shortDir, species, shortcov)
	file.write(short2)

	mergeOutput = "mergeOutput=%s/%s-short-paired-d%s-merged.fastq\n" % (shortDir, species, shortcov)
	file.write(mergeOutput)

	mergeScript = "mergeScript=/home/seanla/Projects/lrcstats/scripts/mergefiles.py\n\n"
	file.write(mergeScript)

	command = "python $mergeScript -1 $short1 -2 $short2 -o $mergeOutput\n"	
	file.write(command)

	file.close()

species = ['ecoli', 'yeast']
shortCovs = ['50', '100', '200']

for specie in species:
	for shortCov in shortCovs:
		writeMergeShortScript(specie, shortCov)

shellScriptPath = "/home/seanla/Jobs/lrcstats/merge/merge_shorts.sh"

file = open(shellScriptPath, 'w')
file.write("#!/bin/bash\n\n")

for specie in species:
	for shortCov in shortCovs:
		qsub = "qsub merge-%s-short-d%s.pbs\n" % (specie, shortCov)
		file.write(qsub)	
