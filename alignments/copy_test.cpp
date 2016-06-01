#include <iostream>
#include <string>
#include "alignments.hpp"

void testFunction (Alignments alignments)
{
	alignments.printMatrix();
}

int main()
{
	std::string clr = "gTAACTccCTGGC";
        std::string ulrMaf = "G----CTCCCT-GC";
        std::string refMaf = "GTAAAAT--CTGGC";		

	Alignments alignments (refMaf, ulrMaf, clr);
	alignments.printMatrix();

	testFunction(alignments);
	
	return 0;
}
