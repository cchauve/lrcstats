def readConfig(configPath):
	'''
	Reads a configuration file and outputs a dict of user variables
	to the necessary programs.
	''' 
	with open(configPath, 'r') as config:
		variables = {}
		for line in config:
			tokens = line.split()
			# hashtags are comments
			if len(tokens) == 3 and line[0] != "#":
				key = tokens[0]
				path = tokens[2]
				variables[key] = path				
	return variables
