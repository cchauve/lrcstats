#include <iostream>
#include <string>
#include <algorithm>
#include <limits>
#include <cmath>
#include <assert.h>

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
		matrix[0][columnIndex] = 0;
	}

	for (int cIndex = 0; cIndex < cLR.length(); cIndex++)
	{
		for (int uIndex = 0; uIndex < uLR.length(); uIndex++)
		{
			int rowIndex = cIndex + 1;
			int columnIndex = uIndex + 1;
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

int OptimalAlignment::costSub(int uIndex, int cIndex)
{
	if (uLR[uIndex] == cLR[cIndex]) 
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
		if ( cLR[cIndex] == uLR[uIndex] )
		{
			keep = std::abs( matrix[rowIndex-1][columnIndex-1] );
			deletion = std::abs( matrix[rowIndex][columnIndex-1] + del );

			return std::min( keep, deletion ); 
		}
		else
		{
			return matrix[rowIndex][columnIndex-1] + del;
		}
	}
	else if (islower(cLR[cIndex]))
	{
		if ( cLR[cIndex] != uLR[uIndex] )
		{
			return infinity;
		}		
		else
		{
			return matrix[rowIndex-1][columnIndex-1];
		}
	}
	else
	{
		deletion = std::abs( matrix[rowIndex][columnIndex-1] + del );
		insertion = std::abs( matrix[rowIndex-1][columnIndex] + ins );
		substitution = std::abs( matrix[rowIndex-1][columnIndex-1] + costSub(uIndex, cIndex) );

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

		std::cout << "uLR == " << uLR << "\n";
		std::cout << "cLR == " << cLR << "\n";

		std::cout << "uIndex == " << uIndex << "\n";
		std::cout << "cIndex == " << cIndex << "\n";

		if (rowIndex > 0 && columnIndex > 0)
		{
			deletion = matrix[rowIndex][columnIndex-1] + ins;
			insertion = matrix[rowIndex-1][columnIndex] + del;
			substitution = matrix[rowIndex-1][columnIndex-1] + costSub(uIndex, cIndex);	
		}
		else if (rowIndex <= 0 && columnIndex > 0)
		{
			deletion = matrix[rowIndex][columnIndex-1] + ins;
			insertion = infinity;
			substitution = infinity;
		}
		else if (rowIndex > 0 && columnIndex <= 0)
		{
			deletion = infinity;
			insertion = matrix[rowIndex-1][columnIndex];
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

		if (deletion == currentCost)
		{
			std::cout << "Deletion\n";
			uAlignment = uLR[uIndex] + uAlignment;
			cAlignment = "-" + cAlignment;

			columnIndex--;
		}		 
		else if (insertion == currentCost)
		{
			std::cout << "Insertion\n";
			uAlignment = "-" + uAlignment;
			cAlignment = cLR[cIndex] + cAlignment;

			rowIndex--;
		}
		else if (substitution == currentCost)
		{
			std::cout << "Substitution\n";
			uAlignment = uLR[uIndex] + uAlignment;
			cAlignment = cLR[cIndex] + cAlignment;

			rowIndex--;
			columnIndex--;
		}

		std::cout << "uAlignment == " << uAlignment << "\n";
		std::cout << "cAlignment == " << cAlignment << "\n\n";
	}
}

















