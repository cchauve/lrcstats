import job_header

def writeResources(file):
	'''
	Write the resources
	'''
	resources = ['walltime=12:00:00', 'mem=8gb', 'nodes=1:ppn=4']
	for resource in resources:
		line = "PBS -l %s\n" % (resource)
		file.write(line)

def simulateArtShortReads(genome, coverage):
	'''
	Given the genome and coverage, make PBS script to simulate short reads
	'''
	scriptPath = "%s/scripts/simulate/simulate_%s_short_d%s.pbs" % (variables["lrcstats"], genome, coverage) 
	with open(scriptPath, 'w') as file:
		job_header.writeGenericHeader(file)

		# Epilogue script output path
		line = "#PBS -o %s.out\n" % (scriptPath)
		file.write(line)

		writeResources(file)

		# Name of the job
		line = "#PBS -N simulate_%s_short_d%s\n" % (genome, coverage)
		file.write(line)

		file.write('\n')

		coverage = "cov=%s\n" % (coverage)

		genome = "genome=%s\n" % (genome)

		genomeDir = "genomeDir=%s/${genome}\n" % (variables["data"], genome)

		artPath = "art=%s\n" % (variables["art"])

		fq2fastqPath = "fq2fastq=%s/src/preprocessing/fq2fastq.py\n" % (variables["lrcstats"])

		merge_files = "merge_files=%s/src/preprocessing/merge_files/merge_files.py\n" % (variables["lrcstats"])

		line = coverage + genome + genomeDir + artPath + fq2fastqPath + merge_files
		file.write(line)

		line = "outputDir=$genomeDir/art/short-d%{cov}\n" \
			"outputPrefix=$outputDir/${genome}-short-paired-d${cov}\n" \
			"ref=$genomeDir/${genome}_reference.fasta\n" \
			"\n" \
			"mkdir -p $outputDir\n" \
			"$art -p -i $ref -l 100 -f $cov -o $outputPrefix\n" \
			"\n" \
			"python $fq2fastq -i $outputDir\n"
			"\n" \
			"short1=${outputPrefix}1.fastq\n" \
			"short2=${outputPrefix}2.fastq\n" \
			"shortMerged=${outputPrefix}-merged.fastq\n" \
			"\n" \
			"python $merge_files -i $short1 -i $short2 -o $shortMerged\n"
		file.write(line)

def simulateSimlordLongReads(genome, coverage):
	# Given the genome and coverage, make PBS script to simulate short reads
	scriptPath = "%s/scripts/simulate/simulate_%s_long_%s.pbs" % (variables["lrcstats"], genome, coverage) 
	with open(scriptPath, 'w') as file:
		writeGenericHeader(file, scriptPath)

		# Name of the job
		line = "#PBS -N simulate_%s_long_%s\n" % (genome, coverage)
		file.write(line)

		file.write('\n')

		# Write genome name and coverage
		coverage = "cov=%s\n" % (coverage)

		genome = "genome=%s\n" % (genome)

		genomeDir = "genomeDir=%s/${genome}\n" % (variables["data"])

		simlord = "simlord=%s\n" % ( variables["simlord"] )

		lrcstats = "lrcstats=%s\n" % ( variables["lrcstats"] )

		line = coverage + genome + genomeDir + simlord + lrcstats

		line = "sam2maf=$lrcstats/src/preprocessing/sam2maf/sam2maf.py\n" \
			"reads4coverage=$lrcstats/src/preprocessing/reads4coverage.py\n" \
			"outputDir=$genomeDir/simlord/long-d${cov}\n" \
			"outputPrefix=$outputDir/${genome}-long-d${cov}\n" \
			"ref=$genomeDir/${genome}_reference.fasta\n" \
		file.write(line)

		# Get the name of the real PacBio FASTQ file
		key = "%s_fastq" % (genome)
		fastq = variables[key]

		fastqPath = "fastq=$genomeDir/%s\n" % (fastq)
		file.write(fastqPath)

		file.write('\n')

		line = "mkdir -p $outputDir\n" \
			"reads=$(python $reads4coverage -c $cov -i $fastq -r $ref)\n" \
			"$simlord -n $reads -sf $fastq -rr $ref $outputPrefix\n" \
			"\n" \
			"sam=${outputPrefix}.sam\n" \
			"maf=${sam}.maf\n" \
			"\n"
			"python $sam2maf -r $ref -s $sam -o $maf\n"
		file.write(line)
