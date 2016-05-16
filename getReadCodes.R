get_codes <- function() {
	inputFileName = 'peru_ascension_codes.txt';
	inputFile = file(inputFileName, open='r');
	outputFileName = 'peru_read_codes.txt'
	outputFile = file(outputFileName, open='w');

	library(SRAdb);
	sqlfile = getSRAdbFile();

	library(DBI);
	dbcon = dbConnect(RSQLite::SQLite(), sqlfile);

	codes = readLines(inputFile);
	numCodes = length(codes);
	
	for (i in 1:numCodes) {
		reads = sraConvert(codes[i], 'run', dbcon);
		numReads = length(reads);

		line1 = c('-',codes[i]);
		
		writeLines(line1, outputFile);

		for (u in 1:numReads) {
			line2 = c(toString(reads[u]));
			writeLines(line2, outputFile);
		}
	}
	
	close(inputFile);
	close(outputFile);
}
