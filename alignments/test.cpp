#include <iostream>
#include <string>
#include "alignments.hpp"

int main()
{
	std::string uLR = "agatcgggg";
	std::string cLR = "agaTTTtcAGGg";

	OptimalAlignment alignments(uLR, cLR);

	std::cout << "uLR = " << uLR << "\n";
	std::cout << "cLR = " << cLR << "\n";

	std::cout << "uAlignment == " << alignments.get_uAlignment() << "\n";
	std::cout << "cAlignment == " << alignments.get_cAlignment() << "\n\n";

	uLR = "atgctatgc";
	cLR = "aGGGGTtaGC";

	OptimalAlignment alignments2(uLR, cLR);

	std::cout << "uLR = " << uLR << "\n";
	std::cout << "cLR = " << cLR << "\n";

	std::cout << "uAlignment == " << alignments2.get_uAlignment() << "\n";
	std::cout << "cAlignment == " << alignments2.get_cAlignment() << "\n\n";

	return 0;	
}
