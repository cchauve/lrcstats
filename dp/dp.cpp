#include <iostream>
#include <string>
#include <algorithm>
#include <limits>
#include <assert.h>

class OptimalAlignment
{
	public:
		OptimalAlignment(std::string uLR, std::string cLR);
		~OptimalAlignment();
		std::string getAlignment();
		int getDistance();
		void printMatrix();
	private:
		std::string uLR;
		std::string cLR;
		int rows;
		int columns;
		int**  memo;
		std::string alignment;
		int distance;
		int findDistance(int cIndex, int uIndex);
};

OptimalAlignment::OptimalAlignment(std::string uLR, std::string cLR)
{
	uLR = uLR;
	cLR = cLR;

	rows = cLR.length() + 1;
	columns = uLR.length() + 1;

	memo = new int*[rows];

	assert(memo);
	
	for (int cIndex = 0; cIndex < rows; cIndex++)
	{
			memo[cIndex] = new int[columns];
			assert(memo[cIndex]);
	}

	for (int cIndex = 0; cIndex < rows; cIndex++)
	{
		memo[cIndex][0] = cIndex;	
	}

	for (int uIndex = 0; uIndex < columns; uIndex++)
	{
		memo[0][uIndex] = 0;
	}

	for (int cIndex = 1; cIndex < rows; cIndex++)
	{
		for (int uIndex = 1; uIndex < columns; uIndex++)
		{
			memo[cIndex][uIndex] = findDistance(cIndex, uIndex);
		}		
	}

	distance = memo[rows-1][columns-1];
}

OptimalAlignment::~OptimalAlignment(void)
{
	for (int cIndex = 0; cIndex < cLR.length() + 1; cIndex++)
	{
		delete memo[cIndex];
	}
	delete memo;
}

std::string OptimalAlignment::getAlignment()
{
	alignment = "atcg";
	return alignment;
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
			std::cout << memo[rowIndex][columnIndex] << " ";
		}
		std::cout << "\n";
	}	
}

int OptimalAlignment::findDistance(int cIndex, int uIndex)
{
	int del = 1;
	int ins = 1;
	int sub = 1;
	bool isEndingLC;

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
			return std::min( memo[cIndex-1][uIndex-1], memo[cIndex][uIndex-1] + del );
		}
		else
		{
			return memo[cIndex][uIndex-1] + del;
		}
	}
	else if (islower(cLR[cIndex]))
	{
		if ( cLR[cIndex] != uLR[uIndex] )
		{
			int infinity = std::numeric_limits<int>::max();
			return infinity;
		}		
		else
		{
			return memo[cIndex-1][uIndex-1];
		}
	}
	else
	{
		if ( cLR[cIndex] == uLR[uIndex] )
		{
			return memo[cIndex-1][uIndex-1];
		}
		else
		{
			return std::min( memo[cIndex-1][uIndex] + del, 
				    std::min( memo[cIndex][uIndex-1] + ins, memo[cIndex-1][uIndex-1] + sub) );
		}
	}
}
