#include <iostream>
#include <string>
#include "alignments.hpp"

int main()
{
	
	std::string cLR = "gTAACTccCTGGC";
	std::string clrMaf = "gTAA-CTccCTGGC";
	std::string ulrMaf = "G----CTCCCT-GC";
	std::string refMaf = "GTAAAAT--CTGGC";
	
	int score = 6; 

	OptimalAlignment alignments(refMaf, ulrMaf, cLR);
	std::string refAlignment = alignments.getRefAlignment();
	std::string cAlignment = alignments.get_cAlignment();

	std::cout << cAlignment << "\n";
	std::cout << refAlignment << "\n";
	return 0;

}
