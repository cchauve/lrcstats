import sys, os, getopt

if __name__ == "__main__":
        helpMessage = "Merge input files 1 and 2 into output."
        usageMessage = "Usage: %s [-h help and usage] [-1 input file 1] [-2 input file 2] [-o output file]" % (sys.argv[0])
        options = "h1:2:o:"

        try:
                opts, args = getopt.getopt(sys.argv[1:], options)
        except getopt.GetoptError:
                print "Error: unable to read command line arguments."
                sys.exit(2)

        if len(sys.argv) == 1:
                print usageMessage
                sys.exit(2)

	input1 = ""
	input2 = ""
	output = ""

        for opt, arg in opts:
                # Help message
                if opt == '-h':
                        print helpMessage
                        print usageMessage
                        sys.exit()
                elif opt == '-1':
                        input1 = arg
                elif opt == '-2':
                        input2 = arg
                elif opt == '-o':
                        output = arg
		else:
			print "Error: unknown argument"
			sys.exit(2)

	optsIncomplete = False

	if input1 == "":
		print "Error: please provide input1."
		optsIncomplete = True
	if input2 == "":
		print "Error: please provide input2."
		optsIncomplete = True

	if optsIncomplete:
		print usageMessage
		sys.exit(2)

	inputs = [input1, input2]

	with open(output, 'w') as outfile:
		for input in inputs:
			with open(input) as infile:
				print "Merging %s..." % (input)
				for line in infile:
					outfile.write(line)
