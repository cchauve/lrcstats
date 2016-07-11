import sys, os, getopt

if __name__ == "__main__":
        helpMessage = "Merge input files into output in the order it is given in the command line argument string. Separate file names with space."
        usageMessage = "Usage: %s [-h help and usage] [-i input files] [-o output file]" % (sys.argv[0])
        options = "hi:o:"

        try:
                opts, args = getopt.getopt(sys.argv[1:], options)
        except getopt.GetoptError:
                print "Error: unable to read command line arguments."
                sys.exit(2)

        if len(sys.argv) == 1:
                print usageMessage
                sys.exit(2)

	inputs = ""
	output = ""

        for opt, arg in opts:
                # Help message
                if opt == '-h':
                        print helpMessage
                        print usageMessage
                        sys.exit()
                elif opt == '-i':
                        inputs = arg
                elif opt == '-o':
                        output = arg

	optsIncomplete = False

	if inputs == "":
		print "Error: please provide input1."
		optsIncomplete = True

	if optsIncomplete:
		print usageMessage
		sys.exit(2)

	inputs = inputs.split()

	print "Writing output to %s" % (output)

	with open(output, 'w') as outfile:
		for input in inputs:
			print "Merging %s..." % (input)
			'''
			with open(input) as infile:
				for line in infile:
					outfile.write(line)
			'''
	print "Done merging."
