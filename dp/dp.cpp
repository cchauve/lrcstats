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

	matrix = new int*[rows];

	assert(matrix);
	
	for (int rowIndex = 0; rowIndex < rows; rowIndex++)
	{
			matrix[rowIndex] = new int[columns];
			assert(matrix[rowIndex]);
	}

	for (int rowIndex = 0; rowIndex < rows; rowIndex++)
	{
		matrix[rowIndex][0] = rowIndex;	
	}

	for (int columnIndex = 0; columnIndex < columns; columnIndex++)
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
		if ( cLR[cIndex] == uLR[uIndex] )
		{
			return matrix[rowIndex-1][columnIndex-1];
		}
		else
		{
			deletion = std::abs( matrix[rowIndex-1][columnIndex] + del );
			insertion = std::abs( matrix[rowIndex][columnIndex-1] + ins );
			substitution = std::abs( matrix[rowIndex-1][columnIndex-1] + sub );

			return std::min( deletion, std::min(insertion, substitution) ); 
		}
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

	int infinity = std::numeric_limits<int>::max();

	int minimum;

	bool lastWasInserted = false;
	bool lastWasDeleted = false;
	bool lastWasSubbed = false;

	while (rowIndex > 0 || columnIndex > 0)
	{
		uIndex = columnIndex - 1;
		cIndex = rowIndex - 1;

		if (rowIndex > 0 && columnIndex > 0)
		{
			insertion = matrix[rowIndex][columnIndex-1];
			deletion = matrix[rowIndex-1][columnIndex];
			substitution = matrix[rowIndex-1][columnIndex-1];	
		}
		else if (rowIndex <= 0 && columnIndex > 0)
		{
			insertion = matrix[rowIndex][columnIndex-1];
			deletion = infinity;
			substitution = infinity;
		}
		else if (rowIndex > 0 && columnIndex <= 0)
		{
			insertion = infinity;
			deletion = matrix[rowIndex-1][columnIndex];
			substitution = infinity;
		} 

		minimum = std::min( insertion, std::min(deletion, substitution) );

		if (insertion == minimum)
		{
			uAlignment = "-" + uAlignment;

			if (!lastWasInserted || lastWasSubbed)
			{
				cAlignment = cLR[cIndex] + cAlignment;
				lastWasInserted = true;
			}

			lastWasDeleted = false;
			lastWasSubbed = false;

			columnIndex--;
		}		 
		else if (deletion == minimum)
		{
			if (!lastWasDeleted || lastWasSubbed)
			{
				uAlignment = uLR[uIndex] + uAlignment;
				lastWasDeleted = true;
			}

			lastWasInserted = false;
			lastWasSubbed = false;

			cAlignment = "-" + cAlignment;
			rowIndex--;
		}
		else if (substitution == minimum)
		{
			if (!lastWasDeleted || lastWasSubbed)
			{
				uAlignment = uLR[uIndex] + uAlignment;
			}
			
			if (!lastWasInserted || lastWasSubbed)
			{
				cAlignment = cLR[cIndex] + cAlignment;
			}

			lastWasInserted = false;
			lastWasDeleted = false;
			lastWasSubbed = true;

			rowIndex--;
			columnIndex--;
		}
	}
}

















