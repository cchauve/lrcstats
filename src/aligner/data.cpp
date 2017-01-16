#include <iostream>
#include <string>
#include <sstream>
#include <fstream>
#include <vector>
#include <algorithm>
#include "data.hpp"

std::vector<std::string> split(const std::string &s)
/* Tokenizes (i.e. isolates words in sentences and adds to vector) similar 
 * to .split() function in python */ 
{
	
	std::vector<std::string> elems;
	std::stringstream ss(s);
	std::string item;

	while (std::getline(ss, item, ' ')) {
		if (!item.empty()) {
            		elems.push_back(item);
        	}
    	}

	return elems;
}

int64_t gaplessLength(std::string read) 
/* Returns the gapless length of MAF formatted reads */
{
	read.erase(std::remove(read.begin(), read.end(), '-'), read.end());
	read.erase(std::remove(read.begin(), read.end(), 'X'), read.end());
	return read.length(); 
}

int64_t boundarylessLength(std::string read)
/* Returns the length of MAF formatted reads without the 'X' boundaries */
{
	read.erase(std::remove(read.begin(), read.end(), 'X'), read.end());
	return read.length(); 
}

MafFile::MafFile(std::string fileName)
/* Constructor - holds the MAF file name */
{
	filename = fileName;
	std::ofstream file (filename, std::ios::out | std::ios::trunc);
	
	// Write the header in the file upon first opening
	if (file.is_open()) {
		file << "track name=" << filename << "\n";	
		file << "##maf version=1\n";
		file << "# tba.v8\n";
		file << "\n";
		file.close();
	} else {
		std::cerr << "Unable to create MAF file.\n";
	}
}

void MafFile::addReads(Read_t reads)
/* Reads data from alignment and readInfo objects and writes to file in MAF format 
 * as described in https://genome.ucsc.edu/FAQ/FAQformat.html */
{
	std::string ref = reads.ref;
	std::string ulr = reads.ulr;
	std::string clr = reads.clr;
	ReadInfo readInfo = reads.readInfo;
	bool alignmentSuccessful = reads.alignmentSuccessful;

	std::string refName = "ref"; 
	std::string uName = readInfo.name + ".uLR";
	std::string cName = readInfo.name + ".cLR";

	// The position in the original genome from which the read originates.
	// The start position in PacBio reads are 0 since the the read is considered
	// to be the "original" genome.
	std::string refStart = readInfo.start;
	int64_t uStart = 0;
	int64_t cStart = 0;
 
	// Read size, sans gaps
	int64_t refSize = gaplessLength(ref);
	int64_t uSize = gaplessLength(ulr);
	int64_t cSize = gaplessLength(clr);

	// The original size of the source genome. Since PacBio reads are the
	// "original" genome, the source size is simply the size of the read.
	std::string refSrcSize = readInfo.srcSize;
	int64_t uSrcSize = uSize;
	int64_t cSrcSize = cSize;

	std::string refOrient = readInfo.refOrient;
	std::string readOrient = readInfo.readOrient;

	std::ofstream file (filename, std::ios::out | std::ios::app);

	if (file.is_open() and alignmentSuccessful) {
		file << "a\n";
		file << "s " << refName << " " << refStart << " " << refSize << " " << refOrient << " " 
			<< refSrcSize << " " << ref << "\n";
		file << "s " << uName << " " << uStart << " " << uSize << " " << readOrient << " " << uSrcSize << " " << ulr << "\n";
		file << "s " << cName << " " << cStart << " " << cSize << " " << readOrient << " " << cSrcSize << " " << clr << "\n";
		file << "\n";
	} else if ( not alignmentSuccessful ) {
		std::cout << "Failed to align read " << readInfo.name << ".\n";
	} else {
		std::cerr << "Failed to open MAF file.\n";
	}

	file.close();
}
