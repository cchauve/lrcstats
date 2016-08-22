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

def generateStatsJob(test_details):
	'''
	Write the statistics job script.
	'''
	test_name = "%s-%s-%sSx%sL" \
		% (test_details["program"], test_details["genome"], \
			test_details["short_cov"], test_details["long_cov"])
        scriptPath = "%s/scripts/stats/%s/%s-correct.pbs" \
		% (paths["lrcstats"], test_details["program"], test_name)
	with open(scriptPath,'w') as file:
		job_header.writeHeader()

		jobOutputPath = "#PBS -o %s/%s/statistics/%s/%s/%s.out" \
                        % (paths["data"], test_details["genome"], \
				test_details["program"], test_name, test_name)
                file.write(jobOutputPath)

		jobName = "#PBS -N %s-stats\n\n" % (test_name)
                file.write(jobName)
		
		lrcstats = "lrcstats=%s\n" % (paths["lrcstats"])

		program = "program=%s\n" % (test_details["program"])

		genome = "genome=%s\n" % (test_details["genome"])

		long_cov = "long_cov=%s\n" % (test_details["long_cov"])
		
		short_cov = "short_cov=%s\n" % (test_details["short_cov"])

		prefix = "prefix=%s/${genome}\n" % (paths["data"])

		test = "test=${program}-${genome}-${short_cov}Sx${long_cov}L\n"

		line = lrcstats + program + genome + long_cov + prefix + test 
		file.write(line)

		line = "set -e\n" \
                        "\n"
                file.write(line)

		line = "input=${prefix}/align/${test}/${test}.maf\n" \
			"outputDir=${prefix}/stats/${program}/${test}\n"
		file.write(line)

		if test_details["program"] in ["colormap", "colormap_oea", "jabba"]:
			writeRemoveExtended(file)

		line = "############### Collecting data ###########\n" \
			"echo 'Collecting data...'\n" \
			"\n" \
			"statsOutput=${outputDir}/${test}.stats\n" \
			"\n"
		file.write(line)

		if test_details["program"] in ["jabba", "proovread"]:
			command = "$lrcstats stats -m $mafOutput -o $statsOutput -t\n\n"
		else:
			command = "$lrcstats stats -m $mafOutput -o $statsOutput\n\n"
		file.write(command)

		line = "input=${statsOutput}\n" \
			"\n"
		file.write(line)

		line = "############## Finding global statistics ############\n" \
			"echo 'Finding global statistics...'\n" \
			"\n" \
			"statsOutput=${prefix}/stats/${program}/${test}/${test}_stats.txt\n" \
			"summarize_stats=${lrcstats}/src/statistics/summarize_stats.py\n" \
			"\n"

		if test_details["program"] in ["proovread", "jabba"]:
			line = "python $summarize_stats -i ${input} -b -o ${statsOutput}\n" \
		elif test_details["program"] in ["lordec", "colormap", "colormap_oea"]:
			line = "python $summarize_stats -i ${input} -o ${statsOutput}\n" \

		file.write(line)
