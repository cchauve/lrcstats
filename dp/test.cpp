#include <iostream>
#include <string>
#include "dp.hpp"

int main()
{
	std::string uLR = "ggggatcgtttt"; // uncorrected long read
	std::string cLR = "ggggatcgtttt"; // corrected long read

	OptimalAlignment alignment(uLR, cLR);

	alignment.printMatrix();
	
	return 0;	
}
