#include <iostream>
#include <vector>
#include <cstdint>
#include <fstream>
#include <string>
#include <unistd.h> // For getopts
#include <sstream> // for std::stringstream
#include <cctype> // For isdigit and isalpha
#include <queue>
#include <algorithm> // For std::remove

void displayHelp()
{
	std::cout << "Converts SAM (Sequence Alignment/Map) format outputted by SimLoRD to MAF (multiple alignment format), given the original reference sequence in FASTA format.\n";
	std::cout << "The FASTA file must contain the entire reference sequence on a single line.\n";
	std::cout << "This program stores the entire reference sequence in a std::string object. Thus, the maximum reference size"
			<< " this program accepts is the return value of std::string::max_size, which is system dependent.\n";
}

void displayUsage()
{
	std::cout << "Usage: [-h help] [-r FASTA reference path] [-s SAM alignment file path] [-o MAF output prefix]\n";
}


std::string addSpaces(std::string cigar)
/* Add spaces before every number and letter in CIGAR string
 * e.g. "11M3D" -> "11 M 3 D" */
{
	std::string newCigar = "";
	bool lastWasAlpha = false;
	bool lastWasDigit = false;

	for (int i = 0; i < cigar.length(); i++) {
		if ( (lastWasAlpha and std::isdigit( cigar[i] )) or (lastWasDigit and !std::isdigit( cigar[i] )) ) {
			newCigar = newCigar + " " + cigar[i];
		} else {
			newCigar = newCigar + cigar[i];
		}
		if (std::isdigit( cigar[i] )) {
			lastWasDigit = true;
			lastWasAlpha = false;
		} else {
			lastWasDigit = false;
			lastWasAlpha = true;
		}
	}	

	return newCigar;
}

std::vector<std::string> split(const std::string &s, char delim)
/* Tokenizes (i.e. isolates words in sentences and adds to vector) similar 
 *  * to .split() function in python */ 
{
        std::vector<std::string> elems;
        std::stringstream ss(s);
        std::string item;

        while (std::getline(ss, item, delim)) {
                if (!item.empty()) {
                        elems.push_back(item);
		} 
	}

        return elems;
}

int gaplessLength(std::string read) 
/* Returns the gapless length of MAF formatted reads */
{
        read.erase(std::remove(read.begin(), read.end(), '-'), read.end());
        return read.length(); 
}

std::queue< std::string > getCigarQueue( std::vector< std::string > cigarOps ) 
/* Create a queue out of cigar operators */
{
	// Stores number of each operation e.g. if the cigar string is 5=10D, then
	// this vector stores the 5 and 10
	std::vector< int8_t > numOps;
	// Likewise, this vector would store the = and D symbols
	std::vector< std::string > ops;	

	for (int index = 0; index < cigarOps.size(); index++) {
		// Elements at even indices are integers,
		// odd indices are operators
		if (index % 2 == 0) {
			int num = atoi( cigarOps.at(index).c_str() );
			numOps.push_back(num);
		} else {
			std::string op = cigarOps.at(index);
			ops.push_back(op);
		}
	}

	std::queue< std::string > cigarQueue;

	for (int vectorIndex = 0; vectorIndex < numOps.size(); vectorIndex++) {
		// The number of the current operation at vectorIndex in ops
		int numOp = numOps.at(vectorIndex);
		// If there are x ops, then add x ops to the queue e.g.
		// if the cigar string is 3D, then the queue will be
		// ['D', 'D', 'D']
		for (int opIndex = 0; opIndex < numOp; opIndex++) {
			cigarQueue.push( ops.at(vectorIndex) );	
		} 
	}

	return cigarQueue;
}

std::string getRef(std::string refPath)
/* Find the reference sequence from the FASTA file */
{
	std::ifstream file (refPath, std::ios::in);

	std::string line;
	// Skip the first header line
	std::getline(file, line);
	// Read the reference sequence
	std::getline(file, line);

	file.close();

	return line;
} 

std::string getRefAlignment(std::string ref, std::string start, std::queue< std::string > cigarQueue)
/* Find the reference sequence alignment */
{
	// The leftmost position in the reference where the read aligns to 
	std::string refAlignment = "";
	int64_t refPos = atoi( start.c_str() ) - 1;

	while ( !cigarQueue.empty() and refPos < ref.length() ) {
		std::string currentOp = cigarQueue.front();
		if (currentOp == "I") {
			refAlignment = refAlignment + "-";			
		} else {
			refAlignment = refAlignment + ref[ refPos ];
			refPos++;
		}
		cigarQueue.pop();
	}	

	return refAlignment;
}

std::string getReadAlignment(std::string read, std::queue< std::string > cigarQueue)
/* Find the read sequence alignment */
{
	std::string readAlignment = "";
	int64_t readIndex = 0;

	while ( !cigarQueue.empty() and readIndex < read.length() ) {
		std::string currentOp = cigarQueue.front();
		if (currentOp == "D") {
			readAlignment = readAlignment + "-";
		} else {
			readAlignment = readAlignment + read[readIndex];
			readIndex++;
		}
		cigarQueue.pop();
	}

	return readAlignment;
}

void convertSam2Maf(std::string ref, std::string samPath, std::string mafPath)
/* Create the MAF file from SAM data */
{
	std::ifstream sam (samPath, std::ios::in);
	std::ofstream maf (mafPath, std::ios::out | std::ios::app);

	// Length of the genome
	int64_t srcSize = ref.length();
	// Read numbers start at 0 for simlord data
	int8_t readNumber = 0;

	std::string line;

	// Skip the SAM header line
	std::getline(sam, line);

	while ( std::getline(sam, line) ) {
		// For flying spaghetti monster knows why, SAM files outputted by SimLoRD 
		// use tabs to separate columns
		std::vector< std::string > tokens = split(line, '	');

		// Get MAF column data
		std::string start = tokens.at(3);
		std::string cigar = tokens.at(5);
		std::string read = tokens.at(9);

		// Preprocess cigar string
		cigar = addSpaces(cigar);
		std::vector< std::string > cigarOps = split(cigar, ' ');
		std::queue< std::string > cigarQueue = getCigarQueue(cigarOps);

		// Find the reference and read alignments
		std::string refAlignment = getRefAlignment(ref, start, cigarQueue);
		std::string readAlignment = getReadAlignment(read, cigarQueue);

		// More column data
		int8_t readSize = read.length();	
		int64_t refSize = gaplessLength(refAlignment);

		// Write data into MAF file
		maf << "a\n";
		maf << "s ref " << start <<  " " << refSize << " + " << srcSize << " " << refAlignment << "\n";
		maf << "s read" << readNumber << " 0 " << refSize << " + " << srcSize << " " 
			<< readAlignment << "\n";
		maf << "\n";

		// Increment read number
		readNumber = readNumber + 1;
	}

	sam.close();
	maf.close();	
} 

int main(int argc, char* argv[])
{
	std::string refPath = "";
	std::string samPath = "";
	std::string mafPrefix = "";

	int opt;

	while ( (opt = getopt(argc, argv, "hr:s:o:") ) != -1 ) {
		switch (opt) {
			case 'h':
				displayHelp();
				displayUsage();
				return 0;
			case 'r':
				refPath = optarg;
				break;
			case 's':
				samPath = optarg;
				break;
			case 'o':
				mafPrefix = optarg;
				break;
			default:
				std::cerr << "Error: unknown argument.\n";
				displayUsage();
				return 1;	
		}
	}	

	bool optsIncomplete = false;

	if (refPath == "") {
		std::cerr << "Error: please input the path to the reference FASTA sequence.\n";
		optsIncomplete = true;
	}
	if (samPath == "") {
		std::cerr << "Error: please input the path to the SAM alignment file.\n";
		optsIncomplete = true;
	}

	if (optsIncomplete) {
		displayUsage();
		return 1;
	}	

	std::string mafPath;

	if (mafPrefix == "") {
		mafPath = samPath + ".maf";
	} else {
		mafPath = mafPrefix + ".maf";
	}

	std::string ref = getRef(refPath);

	convertSam2Maf(ref, samPath, mafPath);

	return 0;
}
