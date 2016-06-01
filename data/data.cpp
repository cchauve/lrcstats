#include <iostream>
#include <string>
#include <sstream>
#include <fstream>
#include <vector>
#include "data.hpp"

std::vector<std::string> &split(const std::string &s, char delim, std::vector<std::string> &elems)
{
	std::stringstream ss(s);
	std::string item;
	while (std::getline(ss, item, delim)) {
		if (!item.empty()) {
            	elems.push_back(item);
        	}
    	}
	return elems;
}

std::vector<std::string> split(const std::string &s, char delim)
{
	std::vector<std::string> elems;
	split(s, delim, elems);
	return elems;
}

ReadInfo::ReadInfo(std::string readName, std::string refOrientation, std::string readOrientation, int refStart, int refSrcSize)
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

int ReadInfo::getStart()
{
	return start;
}

int ReadInfo::getSrcSize()
{
	return srcSize;
}

MafFile::MafFile(std::string fileName)
{
	filename = fileName;
	std::ofstream file (filename, std::ios::out | std::ios::trunc);
	
	if (file.is_open()) {
		file << "track name=" << filename << "\n";	
		file << "maf version=1\n";
		file.close();
	} else {
		std::cerr << "Unable to create MAF file.\n";
	}
}

void MafFile::addReads(Alignments alignments, ReadInfo readInfo)
{
	std::string ref = alignments.getRef();
	std::string ulr = alignments.getUlr();
	std::string clr = alignments.getClr();

	std::string refName = "reference"; 
	std::string uName = readInfo.getName() + ".uncorrected";
	std::string cName = readInfo.getName() + ".corrected";

	int refStart = readInfo.getStart();
	int uStart = 0;
	int cStart = 0;
 
	int size = ref.length();

	int refSrcSize = readInfo.getSrcSize();
	int uSrcSize = size;
	int cSrcSize = size;

	std::string refOrient = readInfo.getRefOrient();
	std::string readOrient = readInfo.getReadOrient();

	std::ofstream file (filename, std::ios::out | std::ios::app);


	if (file.is_open())
	{
		file << "a\n";
		file << "s " << refName << " " << refStart << " " << size << " " << refOrient << " " 
			<< refSrcSize << " " << ref << "\n";
		file << "s " << uName << " " << uStart << " " << size << " " << readOrient << " " << uSrcSize << " " << ulr << "\n";
		file << "s " << cName << " " << cStart << " " << size << " " << readOrient << " " << cSrcSize << " " << clr << "\n";
		file << "\n";
		file.close();
	} else {
		std::cerr << "Unable to add reads to MAF file\n";
	}
}
