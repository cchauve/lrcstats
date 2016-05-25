#include <iostream>
#include <string>
#include <algorithm>
#include <limits>
#include <cmath>

class OptimalAlignment
{
	public:
		OptimalAlignment(std::string uncorrectedLongRead, std::string correctedLongRead);
		~OptimalAlignment();
		std::string get_uAlignment();
		std::string get_cAlignment();
		int getDistance();
		void printMatrix();
	private:
		std::string uLR;
		std::string cLR;

		int rows;
		int columns;

		int** matrix;

		int del;
		int ins;
		int sub;
		int distance;

		std::string uAlignment;
		std::string cAlignment;

		bool areEqual(char uBase, char cBase);
		int costSub(int uIndex, int cIndex);
		int findDistance(int cIndex, int uIndex);
		void findAlignments();
};

OptimalAlignment::OptimalAlignment(std::string uncorrectedLongRead, std::string correctedLongRead)
{
	del = 1;
	ins = 1;
	sub = 1;

	uLR = uncorrectedLongRead;
	cLR = correctedLongRead;

	rows = cLR.length() + 1;
	columns = uLR.length() + 1;

	int cIndex;
	int uIndex;

	try
	{
		matrix = new int*[rows];
	}
	catch( std::bad_alloc& ba )
	{
		std::cerr << "Memory allocation failed; unable to create DP matrix.\n";
	}
	
	for (int rowIndex = 0; rowIndex < rows; rowIndex++)
	{
		try
		{
			matrix[rowIndex] = new int[columns];
		}	
		catch( std::bad_alloc& ba )
		{
			std::cerr << "Memory allocation failed; unable to create DP matrix.\n";
		}
	}

	for (int rowIndex = 0; rowIndex < rows; rowIndex++)
	{
		matrix[rowIndex][0] = rowIndex;	
	}

	for (int columnIndex = 1; columnIndex < columns; columnIndex++)
	{
		matrix[0][columnIndex] = columnIndex;
	}

	for (int rowIndex = 1; rowIndex < rows; rowIndex++)
	{
		for (int columnIndex = 1; columnIndex < columns; columnIndex++)
		{
			cIndex = rowIndex - 1;
			uIndex = columnIndex -  1;
			matrix[rowIndex][columnIndex] = findDistance(cIndex, uIndex);
		}		
	}

	distance = matrix[rows-1][columns-1];
	findAlignments();
}

OptimalAlignment::~OptimalAlignment(void)
{
	for (int rowIndex = 0; rowIndex < rows; rowIndex++)
	{
		delete matrix[rowIndex];
	}
	delete matrix;
}

std::string OptimalAlignment::get_uAlignment()
{
	return uAlignment;
}

std::string OptimalAlignment::get_cAlignment()
{
	return cAlignment;
}

int OptimalAlignment::getDistance()
{
	return distance;
}

void OptimalAlignment::printMatrix()
{
	for (int rowIndex = 0; rowIndex < rows; rowIndex++)
	{
		for (int columnIndex = 0; columnIndex < columns; columnIndex++)
		{
			std::cout << matrix[rowIndex][columnIndex] << " ";
		}
		std::cout << "\n";
	}	
}

bool OptimalAlignment::areEqual(char uBase, char cBase)
{
	return toupper(uBase) == toupper(cBase);
}

int OptimalAlignment::costSub(int uIndex, int cIndex)
{
	if ( areEqual(uLR[uIndex], cLR[cIndex]) ) 
	{
		return 0;
	}
	else
	{
		return sub;
	}
}

int OptimalAlignment::findDistance(int cIndex, int uIndex)
{
	bool isEndingLC;
	int rowIndex = cIndex + 1;
	int columnIndex = uIndex + 1;

	int keep;
	int substitution;
	int insertion;
	int deletion;

	int infinity = std::numeric_limits<int>::max();

	if ( cIndex < cLR.length() - 1 && islower(cLR[cIndex]) && isupper(cLR[cIndex+1]) )
	{
		isEndingLC = true;	
	} 
	else 
	{
		isEndingLC = false;
	}

	if (isEndingLC)
	{
		if ( areEqual(uLR[uIndex], cLR[cIndex]) )
		{
			keep = matrix[rowIndex-1][columnIndex-1];
			deletion = std::abs( matrix[rowIndex][columnIndex-1] + del );
			return std::min(keep, deletion); 
		}
		else
		{
			deletion = abs( matrix[rowIndex][columnIndex-1] + del );
			return deletion;
		}
	}
	else if (islower(cLR[cIndex]))
	{
		if ( !areEqual(uLR[uIndex], cLR[cIndex]) )
		{
			return infinity;
		}		
		else
		{
			keep = matrix[rowIndex-1][columnIndex-1];
			return keep;
		}
	}
	else
	{
		deletion = abs( matrix[rowIndex][columnIndex-1] + del );
		insertion = abs( matrix[rowIndex-1][columnIndex] + ins );
		substitution = abs( matrix[rowIndex-1][columnIndex-1] + costSub(uIndex, cIndex) );
		return std::min( deletion, std::min(insertion, substitution) ); 
	}
}

void OptimalAlignment::findAlignments()
{
	cAlignment = "";
	uAlignment = "";

	int rowIndex = rows - 1;
	int columnIndex = columns - 1;

	int cIndex;
	int uIndex;

	int insertion;
	int deletion;
	int substitution;
	int currentCost;

	bool isEndingLC;

	int infinity = std::numeric_limits<int>::max();

	while (rowIndex > 0 || columnIndex > 0)
	{
		uIndex = columnIndex - 1;
		cIndex = rowIndex - 1;
		currentCost = matrix[rowIndex][columnIndex];

		/*
		std::cout << "uLR == " << uLR << "\n";
		std::cout << "cLR == " << cLR << "\n";

		std::cout << "uIndex == " << uIndex << "\n";
		std::cout << "cIndex == " << cIndex << "\n";
		*/

		if (rowIndex > 0 && columnIndex > 0)
		{
			deletion = matrix[rowIndex][columnIndex-1] + del;
			insertion = matrix[rowIndex-1][columnIndex] + ins;
			substitution = matrix[rowIndex-1][columnIndex-1] + costSub(uIndex, cIndex);	
		}
		else if (rowIndex <= 0 && columnIndex > 0)
		{
			deletion = matrix[rowIndex][columnIndex-1] + del;
			insertion = infinity;
			substitution = infinity;
		}
		else if (rowIndex > 0 && columnIndex <= 0)
		{
			deletion = infinity;
			insertion = matrix[rowIndex-1][columnIndex] + ins;
			substitution = infinity;
		} 

		if ( cIndex < cLR.length() - 1 && islower(cLR[cIndex]) && isupper(cLR[cIndex+1]) )
		{
			isEndingLC = true;	
		} 
		else 
		{
			isEndingLC = false;
		}

		if (isEndingLC)
		{
			if ( areEqual(uLR[uIndex], cLR[cIndex]) )
			{
						
				if (deletion == currentCost)
				{
					//std::cout << "Deletion\n";
					uAlignment = uLR[uIndex] + uAlignment;
					cAlignment = "-" + cAlignment;
					columnIndex--;
				}		 
				else if (substitution == currentCost)
				{
					//std::cout << "Substitution\n";
					uAlignment = uLR[uIndex] + uAlignment;
					cAlignment = cLR[cIndex] + cAlignment;
					rowIndex--;
					columnIndex--;
				}
				else
				{
					std::cerr << "ERROR CODE 1: No paths found. Terminating backtracking.\n";	
					rowIndex = 0;
					columnIndex = 0;
				}
			}
			else
			{
				if (deletion == currentCost)
				{
					//std::cout << "Deletion\n";
					uAlignment = uLR[uIndex] + uAlignment;
					cAlignment = "-" + cAlignment;
					columnIndex--;
				}	
				else
				{
					std::cerr << "ERROR CODE 2: No paths found. Terminating backtracking.\n";
					rowIndex = 0;
					columnIndex = 0;
				}
			}
		}
		else if (islower(cLR[cIndex]))
		{
			if (substitution == currentCost)
			{
				//std::cout << "Substitution\n";
				uAlignment = uLR[uIndex] + uAlignment;
				cAlignment = cLR[cIndex] + cAlignment;
				rowIndex--;
				columnIndex--;
			}
			else
			{
				std::cerr << "ERROR CODE 4: No paths found. Terminating backtracking.\n";
				rowIndex = 0;
				columnIndex = 0;
			}
		}
		else
		{
			if (deletion == currentCost)
			{
				//std::cout << "Deletion\n";
				uAlignment = uLR[uIndex] + uAlignment;
				cAlignment = "-" + cAlignment;
				columnIndex--;
			}		 
			else if (insertion == currentCost)
			{
				//std::cout << "Insertion\n";
				uAlignment = "-" + uAlignment;
				cAlignment = cLR[cIndex] + cAlignment;
				rowIndex--;
			}
			else if (substitution == currentCost)
			{
				//std::cout << "Substitution\n";
				uAlignment = uLR[uIndex] + uAlignment;
				cAlignment = cLR[cIndex] + cAlignment;
				rowIndex--;
				columnIndex--;
			}
			else
			{
				std::cerr << "ERROR CODE 5: No paths found. Terminating backtracking.\n";
				rowIndex = 0;
				columnIndex = 0;
			}
		}

		//std::cout << "uAlignment == " << uAlignment << "\n";
		//std::cout << "cAlignment == " << cAlignment << "\n\n";
	}
}

















