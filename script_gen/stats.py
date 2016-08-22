import job_header

def writeRemoveExtended(file):
	'''
	Write the commands to remove extended regions in the
	three way MAF file.
	'''
	line = "############### Removing extended regions #############\n" \
		"echo 'Removing extended regions...'\n" \
		"unextend=${lrcstats}/src/preprocessing/unextend_alignments/unextend_alignments.py\n" \
		"unextendOutput=$outputdir/${test}_unextended.maf\n" \
		"python $unextend -i $maf-m $unextendOutput\n" \
		"maf=$unextendOutput\n" 
	file.write(line)

def generateStatsJob(testDetails):
	'''
	Write the statistics job script.
	'''
	testName = "%s-%s-%sSx%sL" \
		% (testDetails["program"], testDetails["genome"], \
			testDetails["shortCov"], testDetails["longCov"])

	# Reminder: experimentName is a global variable initialized in lrcstats.py
        scriptPath = "%s/scripts/%s/stats/%s/%s-correct.pbs" \
		% (paths["lrcstats"], experimentName, testDetails["program"], testName)

	with open(scriptPath,'w') as file:
		job_header.writeHeader()

		# Reminder: experimentName is a global variable initialized in lrcstats.py
		jobOutputPath = "#PBS -o %s/%s/%s/statistics/%s/%s/%s.out" \
                        % (paths["data"], testDetails["genome"], experimentName \
				testDetails["program"], testName, testName)
                file.write(jobOutputPath)

		jobName = "#PBS -N %s-stats\n\n" % (testName)
                file.write(jobName)

		# Reminder: experimentName is a global variable initialized in lrcstats.py
		experiment = "experiment=%s\n" % (experimentName)
		
		# Reminder: paths is a global variable initialized in lrcstats.py
		lrcstats = "lrcstats=%s\n" % (paths["lrcstats"])

		program = "program=%s\n" % (testDetails["program"])

		genome = "genome=%s\n" % (testDetails["genome"])

		longCov = "longCov=%s\n" % (testDetails["longCov"])
		
		shortCov = "shortCov=%s\n" % (testDetails["shortCov"])

		prefix = "prefix=%s/${genome}/${experiment}\n" % (paths["data"])

		test = "test=${program}-${genome}-${shortCov}Sx${longCov}L\n"

		line = lrcstats + program + genome + longCov + prefix + test 
		file.write(line)

		line = "input=${prefix}/align/${test}/${test}.maf\n" \
			"outputDir=${prefix}/stats/${program}/${test}\n" \
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
			"align=${lrcstats}/src/collection/align\n" \
			"statsOutput=${outputDir}/${test}.stats\n" \
			"\n"
		file.write(line)

		if testDetails["program"] in ["jabba", "proovread"]:
			command = "$align stats -m $mafOutput -o $statsOutput -t\n\n"
		else:
			command = "$align stats -m $mafOutput -o $statsOutput\n\n"
		file.write(command)

		line = "input=${statsOutput}\n" \
			"\n"
		file.write(line)

		line = "############## Finding global statistics ############\n" \
			"echo 'Finding global statistics...'\n" \
			"\n" \
			"summarize_stats=${lrcstats}/src/statistics/summarize_stats.py\n" \
			"statsOutput=${prefix}/stats/${program}/${test}/${test}_stats.txt\n" \
			"\n"

		program = testDetails["program"]

		if program in ["proovread", "jabba"]:
			line = "python ${summarize_stats} -i ${input} -b -o ${statsOutput}\n" \
		elif program in ["lordec", "colormap", "colormap_oea"]:
			line = "python ${summarize_stats} -i ${input} -o ${statsOutput}\n" \

		file.write(line)
