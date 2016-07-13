#include <iostream>
#include <vector>
#include <cstdint>
#include <fstream>
#include <string>
#include <unistd.h> // For getopts
#include <sstream> // for std::stringstream
#include <cctype> // For isdigit and isalpha
#include <queue>
#include <algorithm> // For std::remove and std::reverse
#include <cassert> // for assert

void displayHelp()
{
	std::cout << "Converts SAM (Sequence Alignment/Map) format outputted by SimLoRD to MAF (multiple alignment format), given the original reference sequence in FASTA format.\n";
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

	for (int64_t i = 0; i < cigar.length(); i++) {
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

std::string removeDelim(std::string read, char delim)
{
	read.erase(std::remove(read.begin(), read.end(), delim), read.end());
	return read;
}

int64_t gaplessLength(std::string read) 
/* Returns the gapless length of MAF formatted reads */
{
	std::string newRead = removeDelim(read, '-'); 
	assert(newRead.length() > 0);
        return newRead.length(); 
}

void printVector( std::vector< std::string > cigarVector )
{
	for (int i = 0; i < cigarVector.size(); i++) {
		std::cout << cigarVector.at(i) << " ";
	}
	std::cout << "\n";
}

void printIntVector( std::vector< int64_t > cigarVector )
{
	for (int i = 0; i < cigarVector.size(); i++) {
		std::cout << std::to_string( cigarVector.at(i) ) << " ";
	}
	std::cout << "\n";
}

std::queue< std::string > getCigarQueue( std::vector< std::string > cigarOps ) 
/* Create a queue out of cigar operators */
{
	// Stores number of each operation e.g. if the cigar string is 5=10D, then
	// this vector stores the 5 and 10
	std::vector< int64_t > numOps;
	// Likewise, this vector would store the = and D symbols
	std::vector< std::string > ops;	

	for (int64_t index = 0; index < cigarOps.size(); index++) {
		// Elements at even indices are integers,
		// odd indices are operators
		if (index % 2 == 0) {
			int64_t num = atoi( cigarOps.at(index).c_str() );
			numOps.push_back(num);
		} else {
			std::string op = cigarOps.at(index);
			ops.push_back(op);
		}
	}

	assert( numOps.size() == ops.size() );

	std::queue< std::string > cigarQueue;

	for (int64_t opsIndex = 0; opsIndex < numOps.size(); opsIndex++) {
		// The number of the current operation at opsIndex in ops
		int64_t numOp = numOps.at(opsIndex);

		// If there are x ops, then add x ops to the queue e.g.
		// if the cigar string is 3D, then the queue will be
		// ['D', 'D', 'D']
		for (int64_t opIndex = 0; opIndex < numOp; opIndex++) {
			cigarQueue.push( ops.at(opsIndex) );	
		} 
	}

	return cigarQueue;
}

std::string getRef(std::string refPath)
/* Find the reference sequence from the FASTA file */
{
	std::ifstream file (refPath, std::ios::in);

	std::string reference = "";

	std::string line;
	// Skip the first header line
	std::getline(file, line);

	// Read the reference sequence
	while (std::getline(file,line)) {
		reference = reference + line;
	}

	file.close();

	reference = removeDelim(reference, '\n');	

	return reference;
} 

char nextBase(char base, int64_t flag)
/* Returns the appropriate base depending on if the flag indicates reverse complemented */
{
	if (flag == 16) {
		if (base == 'A') {
			return 'T';
		} else if (base == 'T') {
			return 'A';
		} else if (base == 'G') {
			return 'C';
		} else if (base == 'C') {
			return 'G';
		}
	} else {
		return base;
	}
}

std::string getRefSeq(std::string ref, int64_t refPos, std::queue< std::string > cigarQueue)
/* Find the reference subsequence that aligns with the read from the reference and cigar queue */
{
	std::string refSeq = "";

	while( !cigarQueue.empty() ) {
		std::string currentOp = cigarQueue.front();
		if (currentOp != "I") {
			refSeq = refSeq + ref[refPos]; 
			refPos++;
		}
	}

	return refSeq;
}

std::string reverseSeq(std::string sequence)
/* Reverse the inputted sequence. */
{
	std::reverse(sequence.begin(), sequence.end());
	return sequence;	
}

std::string getRefAlignment(std::string ref, int64_t refPos, std::queue< std::string > cigarQueue, int64_t flag)
/* Find the reference sequence alignment */
{
	std::string refSeq = getRefSeq(ref, refPos, cigarQueue);

	// This may change; reverse the reference sequence
	refSeq = reverseSeq(refSeq);

	// The leftmost position in the reference where the read aligns to 
	int index = 0;

	std::string refAlignment = "";

	while ( !cigarQueue.empty() ) {
		std::string currentOp = cigarQueue.front();
		if (currentOp == "I") {
			refAlignment = refAlignment + "-";			
		} else {
			refAlignment = refAlignment + nextBase( refSeq[index], flag );
			index++;
		}
		cigarQueue.pop();
	}	

	return refAlignment;
}

std::string getReadAlignment(std::string read, std::queue< std::string > cigarQueue)
/* Find the read sequence alignment */
{
	assert( !cigarQueue.empty() );
	assert( read.length() > 0 );

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

	assert(readAlignment.length() > 0);

	return readAlignment;
}

void convertSam2Maf(std::string ref, std::string samPath, std::string mafPath)
/* Create the MAF file from SAM data */
{
	std::ifstream sam (samPath, std::ios::in);
	std::ofstream maf (mafPath, std::ios::out | std::ios::trunc);

	// Write the MAF header
	maf << "##maf version=1\n";

	// Length of the genome
	int64_t srcSize = ref.length();
	// Read numbers start at 0 for simlord data
	int64_t readNumber = 0;

	std::string line;

	// Skip the SAM header line
	std::getline(sam, line);

	while ( std::getline(sam, line) ) {
		// For flying spaghetti monster knows why, SAM files outputted by SimLoRD 
		// use tabs to separate columns
		std::vector< std::string > tokens = split(line, '	');

		// A flag of 16 indicates the sequence is reverse complemented;
		// 0 indicates that it is regular
		int64_t flag = atoi( tokens.at(1).c_str() );
		std::string refPos = tokens.at(3);
		std::string unprocessedCigar = tokens.at(5);
		std::string read = tokens.at(9);

		assert(refPos != "");
		assert(unprocessedCigar != "");
		assert(read != "");

		int64_t start = atoi( refPos.c_str() ) - 1;

		// Preprocess cigar string
		std::string cigar = addSpaces(unprocessedCigar);
		
		std::vector< std::string > cigarOps = split(cigar, ' ');
		assert( cigarOps.size() > 0 );

		std::queue< std::string > cigarQueue = getCigarQueue(cigarOps);
		assert( !cigarQueue.empty() );

		// Find the reference and read alignments
		std::string refAlignment = getRefAlignment(ref, start, cigarQueue, flag);
		std::cout << "Ref Alignment found successfully\n";
		std::string readAlignment = getReadAlignment(read, cigarQueue);
		std::cout << "Read Alignment found successfully\n\n";

		assert(refAlignment.length() > 0);
		assert(readAlignment.length() > 0);

		// More column data
		int64_t readSize = gaplessLength(readAlignment);	
		int64_t refSize = gaplessLength(refAlignment);
		// Writing int datatypes to files doesn't seem to work, so 
		// instead we convert to string beforehand
		std::string readNumberString = std::to_string(readNumber);

		assert(readSize > 0);
		assert(refSize > 0);

		std::string strand;

		if (flag == 16) {
			strand = "-";
		} else {
			strand = "+";
		}

		// Write data into MAF file
		maf << "a\n";
		maf << "s ref " << start <<  " " << refSize << " " << strand << " " << srcSize << " " << refAlignment << "\n";
		maf << "s read" << readNumberString << " 0 " << refSize << " " << strand << " " << srcSize << " " 
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
