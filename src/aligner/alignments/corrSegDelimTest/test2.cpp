#include <string>
#include <iostream>
#include <vector>
#include "alignments.hpp"

int main()
{
	std::cout << "Test Case 1\n";

	std::string ref = "TTTT";
	std::string ulr = "TTTT";
	std::string clr = "TTTT AAAA";

	TrimmedAlignments alignments(ref,ulr,clr);

	alignments.printMatrix();

	std::string obsRefMaf = alignments.getRef();
	std::string obsUlrMaf = alignments.getUlr();
	std::string obsClrMaf = alignments.getClr();
	
	std::cout << "Observed alignment:\n";
	std::cout << obsRefMaf << std::endl;
	std::cout << obsUlrMaf << std::endl;
	std::cout << obsClrMaf << std::endl;


	return 0;
}
