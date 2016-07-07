#include <iostream>
#include <vector>
#include <algorithm> // For std::sort
#include <cstdint>
#include <fstream>
#include <unistd.h> // For getopts
#include <sstream> // for std::stringstream

struct Read 
{
	int64_t number;
	std::string sequence;
};

std::vector<std::string> split(const std::string &s)
/* Tokenizes (i.e. isolates words in sentences and adds to vector) similar 
 *  * to .split() function in python */ 
{
        
        std::vector<std::string> elems;
        std::stringstream ss(s);
        std::string item;

        while (std::getline(ss, item, '_')) {
                if (!item.empty()) {
                        elems.push_back(item);
                }
        }

        return elems;
}

bool readsSorter(Read const& lhs, Read const& rhs)	
{
	return lhs.number < rhs.number;
}

std::vector< Read > getReads(std::string inputPath)
{
	std::ifstream input (inputPath, std::ios::in);
	std::string line;
	std::vector< std::string > header;
	std::vector< Read > reads;
	Read read;
	int64_t readNumber;

	while (!input.eof()) {
		readNumber = 0;

		// Read header of sequence
		std::getline(input, line);

		if (line != "") {
			header = split(line);
			readNumber = stoi( header.at(1) );	
		}

		// Read sequence
		std::getline(input, line);	

		if (line != "" && readNumber != 0) {
			read.number = readNumber;
			read.sequence = line;
		}

		// Add read to reads
		reads.push_back(read);
	}

	input.close();

	return reads;
}

void writeSortedReads(std::vector< Read > reads, std::string outputPath)
{
	std::ofstream output (outputPath, std::ios::out);

	for (int index = 0; index < reads.size(); index++) {
		output << ">" << reads.at(index).number << "\n";
		output << reads.at(index).sequence << "\n";
	}

	output.close();
}

int main(int argc, char *argv[])
{
	std::string help = "Sort reads in FASTA file based on read number.\n";
	std::string usage = "Usage: sortfasta [-i input path][-o output path]\n";

	int opt;

	if (argc == 1) {
		std::cerr << usage;
		return 1;
	}

	std::string inputPath = "";
	std::string outputPath = "";

	while ((opt = getopt(argc, argv, "hi:o:")) != -1) {
		switch (opt) {
			case 'h':
				std::cout << help << usage;	
				return 0;
			case 'i':
				// Source maf file name
				inputPath = optarg;
				break;
			case 'o':
				// maf output file name
				outputPath = optarg;
				break;
		}
	}

	bool optsIncomplete = false;

	if (inputPath == "") {
		std::cerr << "Please provide an input path.\n";
		optsIncomplete = true;	
	}
	if (outputPath == "") {
		std::cerr << "Please provide an output path.\n";
		optsIncomplete = true;
	}
	if (optsIncomplete) {
		std::cerr << usage;
		return 1;
	}

	std::cout << "Reading input file...\n";
	std::vector< Read > reads = getReads(inputPath);

	std::cout << "Sorting reads...\n";
	std::sort(reads.begin(), reads.end(), &readsSorter);

	std::cout << "Writing to output file...\n";
	writeSortedReads(reads, outputPath);

	return 0;
}
