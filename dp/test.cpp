#include <iostream>
#include <string>
#include "dp.hpp"

int main()
{
	std::string uLR = "atcgagggg"; // corrected long read
	std::string cLR = "atTTTcgaTTTTgggg"; // uncorrected long read

	OptimalAlignment alignments(uLR, cLR);

	std::cout << "uAlignment == " << alignments.get_uAlignment() << "\n";
	std::cout << "cAlignment == " << alignments.get_cAlignment() << "\n";
	
	return 0;	
}
