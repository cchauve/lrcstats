#include <iostream>
#include <string>
#include "dp.hpp"

int main()
{
	std::string uLR = "atcgagggg";
	std::string cLR = "atTTTcgaTTTTgggg";

	OptimalAlignment alignments(uLR, cLR);

	std::cout << "uAlignment == " << alignments.get_uAlignment() << "\n";
	std::cout << "cAlignment == " << alignments.get_cAlignment() << "\n";
	
	return 0;	
}
