import sys
import os
import getopt

if __name__ == "__main__":
        helpMessage = "Changes the extension of every file with extension .fq to .fastq in the input directory."
        usageMessage = "Usage: %s [-h help and usage] [-i directory]" % (sys.argv[0])
        options = "hi:"

        try:
                opts, args = getopt.getopt(sys.argv[1:], options)
        except getopt.GetoptError:
                print "Error: unable to read command line arguments."
                sys.exit(2)

        if len(sys.argv) == 1:
                print usageMessage
                sys.exit(2)

	inputDir = None

        for opt, arg in opts:
                # Help message
                if opt == '-h':
                        print helpMessage
                        print usageMessage
                        sys.exit()
                elif opt == '-i':
                        inputDir = arg
		else:
			print "Error: unknown argument"
			sys.exit(2)

	if inputDir is None:
		print "Error: please provide an input directory."
		print usageMessage
		sys.exit(2)

	print "Converting files with extension .fq to .fastq..."
	print "Input directory is %s." % (inputDir)

	# Walk through the directory, changing fq extensions to fastq
	for root, dir, files in os.walk(inputDir):
		for file in files:
			if file.endswith(".fq"):
				print "Changing extension of %s to fastq..." % (file)
				absPath = os.path.realpath(os.path.join(root,file))
				base = os.path.splitext(absPath)[0]
				os.rename(absPath, base + ".fastq")	
