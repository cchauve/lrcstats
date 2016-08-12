#include <iostream>
#include <vector>
#include <string>
#include "alignments.hpp"

int main()
{
	std::string ref = "ATCGAAAA";
	std::string uRead = "ATCGAAAA";
	std::string cRead = "ATCG";
	TrimmedAlignments alignments(ref, uRead, cRead);
	std::cout << "cAlignment: " << alignments.getClr() << "\n";
	alignments.printMatrix();
	return 0;
}
