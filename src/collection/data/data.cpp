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
	return read.length(); 
}

ReadInfo::ReadInfo(std::string readName, std::string refOrientation, std::string readOrientation, 
			std::string refStart, std::string refSrcSize)
/* Constructor - just holds the read alignment information */
{
	name = readName;
	refOrient = refOrientation;
	readOrient = readOrientation;
	start = refStart;
	srcSize = refSrcSize;
}

void ReadInfo::reset(std::string readName, std::string refOrientation, std::string readOrientation,
			std::string refStart, std::string refSrcSize)
/* Reinitialize values of ReadInfo object */
{
	name = readName;
	refOrient = refOrientation;
	readOrient = readOrientation;
	start = refStart;
	srcSize = refSrcSize;
}

std::string ReadInfo::getName()
{
	return name;
}

std::string ReadInfo::getRefOrient()
{
	return refOrient;
}

std::string ReadInfo::getReadOrient()
{
	return readOrient;
}

std::string ReadInfo::getStart()
{
	return start;
}

std::string ReadInfo::getSrcSize()
{
	return srcSize;
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

void MafFile::addReads(TrimmedAlignments alignments, ReadInfo readInfo)
/* Reads data from alignment and readInfo objects and writes to file in MAF format 
 * as described in https://genome.ucsc.edu/FAQ/FAQformat.html */
{
	std::string ref = alignments.getRef();
	std::string ulr = alignments.getUlr();
	std::string clr = alignments.getClr();

	std::string refName = "reference"; 
	std::string uName = readInfo.getName() + ".uncorrected";
	std::string cName = readInfo.getName() + ".corrected";

	// The position in the original genome from which the read originates.
	// The start position in PacBio reads are 0 since the the read is considered
	// to be the "original" genome.
	std::string refStart = readInfo.getStart();
	int64_t uStart = 0;
	int64_t cStart = 0;
 
	// Read size, sans gaps
	int64_t refSize = gaplessLength(ref);
	int64_t uSize = gaplessLength(ulr);
	int64_t cSize = gaplessLength(clr);

	// The original size of the source genome. Since PacBio reads are the
	// "original" genome, the source size is simply the size of the read.
	std::string refSrcSize = readInfo.getSrcSize();
	int64_t uSrcSize = uSize;
	int64_t cSrcSize = cSize;

	std::string refOrient = readInfo.getRefOrient();
	std::string readOrient = readInfo.getReadOrient();

	std::ofstream file (filename, std::ios::out | std::ios::app);

	if (file.is_open()) {
		file << "a\n";
		file << "s " << refName << " " << refStart << " " << refSize << " " << refOrient << " " 
			<< refSrcSize << " " << ref << "\n";
		file << "s " << uName << " " << uStart << " " << uSize << " " << readOrient << " " << uSrcSize << " " << ulr << "\n";
		file << "s " << cName << " " << cStart << " " << cSize << " " << readOrient << " " << cSrcSize << " " << clr << "\n";
		file << "\n";
		file.close();
	} else {
		std::cerr << "Unable to add reads to MAF file\n";
	}
}

void MafFile::addReads(UntrimmedAlignments alignments, ReadInfo readInfo)
/* Reads data from alignment and readInfo objects and writes to file in MAF format 
 * as described in https://genome.ucsc.edu/FAQ/FAQformat.html */
{
	std::string ref = alignments.getRef();
	std::string ulr = alignments.getUlr();
	std::string clr = alignments.getClr();

	std::string refName = "reference"; 
	std::string uName = readInfo.getName() + ".uncorrected";
	std::string cName = readInfo.getName() + ".corrected";

	// The position in the original genome from which the read originates.
	// The start position in PacBio reads are 0 since the the read is considered
	// to be the "original" genome.
	std::string refStart = readInfo.getStart();
	int64_t uStart = 0;
	int64_t cStart = 0;
 
	// Read size, sans gaps
	int64_t refSize = gaplessLength(ref);
	int64_t uSize = gaplessLength(ulr);
	int64_t cSize = gaplessLength(clr);

	// The original size of the source genome. Since PacBio reads are the
	// "original" genome, the source size is simply the size of the read.
	std::string refSrcSize = readInfo.getSrcSize();
	int64_t uSrcSize = uSize;
	int64_t cSrcSize = cSize;

	std::string refOrient = readInfo.getRefOrient();
	std::string readOrient = readInfo.getReadOrient();

	std::ofstream file (filename, std::ios::out | std::ios::app);

	if (file.is_open()) {
		file << "a\n";
		file << "s " << refName << " " << refStart << " " << refSize << " " << refOrient << " " 
			<< refSrcSize << " " << ref << "\n";
		file << "s " << uName << " " << uStart << " " << uSize << " " << readOrient << " " << uSrcSize << " " << ulr << "\n";
		file << "s " << cName << " " << cStart << " " << cSize << " " << readOrient << " " << cSrcSize << " " << clr << "\n";
		file << "\n";
		file.close();
	} else {
		std::cerr << "Unable to add reads to MAF file\n";
	}
}
