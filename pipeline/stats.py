import job_header

def writeRemoveExtended(file):
	'''
	Write the commands to remove extended regions in the
	three way MAF file.
	'''
	line = "############### Removing extended regions #############\n" \
		"echo 'Removing extended regions...'\n" \
		"unextend=${lrcstats}/src/preprocessing/unextend_alignments/unextend_alignments.py\n" \
		"unextendOutput=$outputDir/${testName}_unextended.maf\n" \
		"python $unextend -i $maf -m $unextendOutput\n" \
		"maf=$unextendOutput\n" \
		"\n" 
	file.write(line)

def generateStatsJob(testDetails, paths):
	'''
	Write the statistics job script.
	Inputs
	- (dict of strings) testDetails: contains the test parameters
	- (dict of strings) paths: contains the paths to the programs in the user's machine
	'''
	testName = "%s-%s-%sSx%sL" \
		% (testDetails["program"], testDetails["genome"], \
			testDetails["shortCov"], testDetails["longCov"])

        scriptPath = "%s/scripts/%s/stats/%s/%s-stats.pbs" \
		% (paths["lrcstats"], testDetails["experimentName"], testDetails["program"], testName)

	with open(scriptPath,'w') as file:
		job_header.writeHeader(file, paths)
	
		# Write the resources
		resources = ["walltime=10:00:00", "mem=8gb", "nodes=1:ppn=1"]

		for resource in resources:
			line = "#PBS -l %s\n" % (resource)
			file.write(line)

		jobOutputPath = "#PBS -o %s/%s/stats/%s/%s/%s.out\n" \
                        % (paths["data"], testDetails["experimentName"], \
				testDetails["program"], testName, testName)
                file.write(jobOutputPath)

		jobName = "#PBS -N %s-%s-stats\n\n" % (testDetails["experimentName"], testName)
                file.write(jobName)

		experiment = "experiment=%s\n" % (testDetails["experimentName"])
		
		# Reminder: paths is a global variable initialized in lrcstats.py
		lrcstats = "lrcstats=%s\n" % (paths["lrcstats"])

		program = "program=%s\n" % (testDetails["program"])

		genome = "genome=%s\n" % (testDetails["genome"])

		longCov = "longCov=%s\n" % (testDetails["longCov"])
		
		shortCov = "shortCov=%s\n" % (testDetails["shortCov"])

		prefix = "prefix=%s/${experiment}\n" % (paths["data"])

		test = "testName=${program}-${genome}-${shortCov}Sx${longCov}L\n"

		line = experiment + lrcstats + program + genome + longCov + shortCov + prefix + test 
		file.write(line)

		line = "maf=${prefix}/align/${program}/${testName}/${testName}.maf\n" \
			"outputDir=${prefix}/stats/${program}/${testName}\n" \
			"\n"
		file.write(line)

		line = "set -e\n" \
			"mkdir -p ${outputDir}\n" \
                        "\n"
                file.write(line)


		if testDetails["program"] in ["colormap", "colormap_oea", "jabba"]:
			writeRemoveExtended(file)

		line = "############### Collecting data ###########\n" \
			"echo 'Collecting data...'\n" \
			"\n" \
			"align=${lrcstats}/src/aligner/aligner\n" \
			"statsOutput=${outputDir}/${testName}.stats\n" \
			"\n"
		file.write(line)

		if testDetails["program"] in ["jabba", "proovread"]:
			command = "$align stats -m $maf -o $statsOutput -t\n\n"
		else:
			command = "$align stats -m $maf -o $statsOutput\n\n"
		file.write(command)

		line = "input=${statsOutput}\n" \
			"\n"
		file.write(line)

		line = "############## Summarizing statistics ############\n" \
			"echo 'Summarizing statistics...'\n" \
			"\n" \
			"summarize_stats=${lrcstats}/src/statistics/summarize_stats.py\n" \
			"statsOutput=${prefix}/stats/${program}/${testName}/${testName}_stats.txt\n" \
			"\n"
		file.write(line)

		program = testDetails["program"]

		if program in ["proovread", "jabba"]:
			line = "python ${summarize_stats} -i ${input} -o ${statsOutput}\n"
		elif program in ["lordec", "colormap", "colormap_oea"]:
			line = "python ${summarize_stats} -i ${input} -b -o ${statsOutput}\n"

		file.write(line)

def createQuickQsubScript(testDetails, paths, experimentName):
	'''
	Create a quick-qsub script for the alignment jobs
	'''
	scriptPaths = []
        for testDetail in testDetails:
		testName = "%s-%s-%sSx%sL" \
			% (testDetail["program"], testDetail["genome"], testDetail["shortCov"], testDetail["longCov"])
	        scriptPath = "%s/scripts/%s/stats/%s/%s-stats.pbs" \
			% (paths["lrcstats"], testDetail["experimentName"], testDetail["program"], testName)
		scriptPaths.append(scriptPath)

        path = "%s/scripts/%s/quick-qsub-stats.sh" % (paths["lrcstats"], experimentName)
        with open(path,'w') as file:
		file.write("#!/bin/bash\n")
                for scriptPath in scriptPaths:
                        line = "qsub %s\n" % (scriptPath)
                        file.write(line)	
