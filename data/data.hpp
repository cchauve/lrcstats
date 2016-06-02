#ifndef DATA_H
#define DATA_H

#include "../alignments/alignments.hpp"

std::vector<std::string> split(const std::string &str);

int gaplessLength(std::string read);

class ReadInfo
/* Carries information about uLR and reference parsed from source MAF file */
{
        public:
                ReadInfo(std::string readName, std::string refOrientation, std::string readOrientation, 
				std::string refStart, std::string refSrcSize);
		void reset(std::string readName, std::string refOrientation, std::string readOrientation,
				std::string refStart, std::string refSrcSize);
                std::string getName();
                std::string getRefOrient();
                std::string getReadOrient();
                std::string getStart();
                std::string getSrcSize();
        private:
                std::string name;
                std::string refOrient;
                std::string readOrient;
                std::string start;
                std::string srcSize;
};

class MafFile
/* Creates a MAF containing 3-way alignments between a reference, uLR and cLR */
{
	public:
		MafFile(std::string fileName);
		// Writes 3-way alignment to MAF file
		void addReads(Alignments alignments, ReadInfo readInfo);
	private:
		std::string filename;
};

#endif /* DATA_H */
