#include <iostream>
#include <vector>
#include "data.hpp"

int main()
{
	std::string refMaf = "ACGT-ACGT";	
	std::string ulrMaf = "ACGTTACGT";
	std::string clr = "acGTACgt";

	std::string readName = "test";
	std::string refOrientation = "+";
	std::string readOrientation = "-";
	std::string refStart = "0";
	std::string refSrcSize = "100";
	
	std::string mafFileName = "test.maf";

	Alignments alignments (refMaf, ulrMaf, clr);
	ReadInfo readInfo (readName, refOrientation, readOrientation, refStart, refSrcSize);

	MafFile mafFile (mafFileName);
	
	mafFile.addReads(alignments, readInfo);

	mafFile.addReads(alignments, readInfo);

	return 0;	
}
