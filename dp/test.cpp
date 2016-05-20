#include <iostream>
#include <string>
#include <limits>
#include "dp.hpp"

int main()
{
	std::string uLR = "ggggatcAAAAgtttt"; // uncorrected long read
	std::string cLR = "ggggatcgtttt"; // corrected long read

	OptimalAlignment alignment(uLR, cLR);

	alignment.printMatrix();
	
	return 0;	
}
