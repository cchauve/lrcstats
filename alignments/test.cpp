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
	std::cout << clrMaf << "\n";
	return 0;

}
