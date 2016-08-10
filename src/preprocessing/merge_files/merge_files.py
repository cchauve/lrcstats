import sys
import os
import getopt

helpMessage = ( "Merge input files into output in the order it is given in the command line argument string.\n" 
			+ "Indicate each file name with -i argument in command line." )
usageMessage = ( "Usage: %s [-h help and usage] [-i input files] [-o output file]\n" % (sys.argv[0]) 
 			+ "Example: %s -i file1.txt -i file2.txt -o file_merged.txt" % (sys.argv[0]) )
options = "hi:o:"

try:
	opts, args = getopt.getopt(sys.argv[1:], options)
except getopt.GetoptError:
	print "Error: unable to read command line arguments."
	sys.exit(2)

if len(sys.argv) == 1:
	print usageMessage
	sys.exit(2)

inputs = [] 
output = ""

for opt, arg in opts:
	# Help message
	if opt == '-h':
	 	print helpMessage
		print usageMessage
		sys.exit()
	elif opt == '-i':
		inputs.append(arg)
	elif opt == '-o':
		output = arg

optsIncomplete = False

if len(inputs) < 2:
	print "Error: please provide at least two inputs."
	optsIncomplete = True

if output is None:
	print "Error: please provide an output path."
	optsIncomplete = True 

if optsIncomplete:
	print usageMessage
	sys.exit(2)

print "Merging files..."
print "Writing output to %s" % (output)

with open(output, 'w') as outfile:
	for input in inputs:
		print "Merging %s..." % (input)
		with open(input) as infile:
			for line in infile:
				outfile.write(line)
print "Done merging."
