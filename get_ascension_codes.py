inputFilename = "peru_tuberculosis_strains.txt"
outputFilename = "peru_ascension_codes.txt"

inputFile = open(inputFilename, 'r')
outputFile = open(outputFilename, 'w')

ascension_codes = []

for line in inputFile:
	line = line.split()

	if len(line) == 2:
		code = line[1][1:-1]
	elif len(line) == 1 and line[0] != 'pending':
		code = line[0]

	if code not in ascension_codes:
		ascension_codes.append(code)	
		outputFile.write(code)
		outputFile.write('\n')

inputFile.close()
outputFile.close()
