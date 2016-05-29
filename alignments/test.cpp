#include <iostream>
#include <string>
#include "alignments.hpp"

int main()
{
	
	std::string cLR = "gTCctctGgc";
	std::string clrMaf = "gT-C-ct--ctGgc";
	std::string ulrMaf = "G----CTCCCT-GC";
	std::string refMaf = "GTAAAAT--CTGGC";
	
	int score = 6; 

	OptimalAlignment alignments(refMaf, ulrMaf, cLR);

	return 0;

}
