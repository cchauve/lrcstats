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
	private:
		std::string uLR;
		std::string cLR;
		int rows;
		int columns;
		int** matrix;
		int del;
		int ins;
		int sub;
		std::string uAlignment;
		std::string cAlignment;
		int costSub(int uIndex, int cIndex);
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
	bool isEndingLC;
	int keep;
	int substitution;
	int insertion;
	int deletion;
	int infinity = std::numeric_limits<int>::max();

	try {
		matrix = new int*[rows];
	} catch( std::bad_alloc& ba ) {
		std::cerr << "Memory allocation failed; unable to create DP matrix.\n";
	}
	
	for (int rowIndex = 0; rowIndex < rows; rowIndex++) {
		try {
			matrix[rowIndex] = new int[columns];
		} catch( std::bad_alloc& ba ) {
			std::cerr << "Memory allocation failed; unable to create DP matrix.\n";
		}
	}

	// Set the base cases for the DP matrix
	for (int rowIndex = 0; rowIndex < rows; rowIndex++) {
		matrix[rowIndex][0] = rowIndex;	
	}
	for (int columnIndex = 1; columnIndex < columns; columnIndex++) {
		matrix[0][columnIndex] = columnIndex;
	}

	// Find the optimal edit distance such that all uncorrected segments of cLR are aligned with uncorrected
 	// portions of uLR. 
	for (int rowIndex = 1; rowIndex < rows; rowIndex++) {
		for (int columnIndex = 1; columnIndex < columns; columnIndex++) {
			cIndex = rowIndex - 1;
			uIndex = columnIndex -  1;

			// Determine if the current letter in cLR is lowercase and is followed by an upper case letter
			// i.e. if the current letter in cLR is an ending lowercase letter
			if ( cIndex < cLR.length() - 1 && islower(cLR[cIndex]) && isupper(cLR[cIndex+1]) ) {
				isEndingLC = true;	
			} else {
				isEndingLC = false;
			}

			if (isEndingLC) {
				// If both letters are the same, we can either keep both letters or delete the one from
				// cLR. If they are different, we can't keep both so we can only consider deleting the
				// one from cLR.
				if ( toupper(uLR[uIndex]) == toupper(cLR[cIndex]) ) {
					keep = matrix[rowIndex-1][columnIndex-1];
					deletion = std::abs( matrix[rowIndex][columnIndex-1] + del );
					matrix[rowIndex][columnIndex] = std::min(keep, deletion); 
				} else {
					matrix[rowIndex][columnIndex] = std::abs( matrix[rowIndex][columnIndex-1] + del );
				}
			} else if (islower(cLR[cIndex])) {
				// Setting the position in the matrix to infinity ensures that we can never
				// find an alignment where the uncorrected segments are not perfectly aligned.
				if ( toupper( uLR[uIndex] ) != toupper( cLR[cIndex] ) ) {
					matrix[rowIndex][columnIndex] = infinity;
				} else {
					matrix[rowIndex][columnIndex] = matrix[rowIndex-1][columnIndex-1];
				}
			} else {
				// Usual Levenshtein distance equations.
				deletion = std::abs( matrix[rowIndex][columnIndex-1] + del );
				insertion = std::abs( matrix[rowIndex-1][columnIndex] + ins );
				substitution = std::abs( matrix[rowIndex-1][columnIndex-1] + costSub(uIndex, cIndex) );
				matrix[rowIndex][columnIndex] = std::min( deletion, std::min(insertion, substitution) ); 
			}
		}		
	}
	findAlignments();
}

OptimalAlignment::~OptimalAlignment(void)
{
	for (int rowIndex = 0; rowIndex < rows; rowIndex++) {
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

int OptimalAlignment::costSub(int uIndex, int cIndex)
{
	if ( toupper( uLR[uIndex] ) == toupper( cLR[cIndex] ) ) {
		return 0;
	} else {
		return sub;
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

	// Follow the best path from the bottom right to the top left of the matrix.
	// This is equivalent to the optimal alignment between uLR and cLR.
	// The path we follow is restricted to the conditions set when computing the matrix,
	// i.e. we can never follow a path that the edit distance equations do not allow.
	while (rowIndex > 0 || columnIndex > 0) {
		uIndex = columnIndex - 1;
		cIndex = rowIndex - 1;
		currentCost = matrix[rowIndex][columnIndex];
		// Set the costs of the different operations, 
		// ensuring we don't go out of bounds of the matrix.
		if (rowIndex > 0 && columnIndex > 0) {
			deletion = matrix[rowIndex][columnIndex-1] + del;
			insertion = matrix[rowIndex-1][columnIndex] + ins;
			substitution = matrix[rowIndex-1][columnIndex-1] + costSub(uIndex, cIndex);	
		} else if (rowIndex <= 0 && columnIndex > 0) {
			deletion = matrix[rowIndex][columnIndex-1] + del;
			insertion = infinity;
			substitution = infinity;
		} else if (rowIndex > 0 && columnIndex <= 0) {
			deletion = infinity;
			insertion = matrix[rowIndex-1][columnIndex] + ins;
			substitution = infinity;
		} 

		// Make sure we follow the same path as dictated by the edit distance equations. 
		if ( cIndex < cLR.length() - 1 && islower(cLR[cIndex]) && isupper(cLR[cIndex+1]) ) {
			isEndingLC = true;	
		} else {
			isEndingLC = false;
		}

		if (isEndingLC) {
			if ( toupper( uLR[uIndex] ) == toupper( cLR[cIndex] ) ) {
				if (deletion == currentCost) {
					uAlignment = uLR[uIndex] + uAlignment;
					cAlignment = "-" + cAlignment;
					columnIndex--;
				} else if (substitution == currentCost) {
					uAlignment = uLR[uIndex] + uAlignment;
					cAlignment = cLR[cIndex] + cAlignment;
					rowIndex--;
					columnIndex--;
				} else {
					std::cerr << "ERROR CODE 1: No paths found. Terminating backtracking.\n";	
					rowIndex = 0;
					columnIndex = 0;
				}
			} else {
				if (deletion == currentCost) {
					uAlignment = uLR[uIndex] + uAlignment;
					cAlignment = "-" + cAlignment;
					columnIndex--;
				} else {
					std::cerr << "ERROR CODE 2: No paths found. Terminating backtracking.\n";
					rowIndex = 0;
					columnIndex = 0;
				}
			}
		} else if (islower(cLR[cIndex])) {
			if (substitution == currentCost) {
				uAlignment = uLR[uIndex] + uAlignment;
				cAlignment = cLR[cIndex] + cAlignment;
				rowIndex--;
				columnIndex--;
			} else {
				std::cerr << "ERROR CODE 4: No paths found. Terminating backtracking.\n";
				rowIndex = 0;
				columnIndex = 0;
			}
		} else {
			if (deletion == currentCost) {
				uAlignment = uLR[uIndex] + uAlignment;
				cAlignment = "-" + cAlignment;
				columnIndex--;
			} else if (insertion == currentCost) {
				uAlignment = "-" + uAlignment;
				cAlignment = cLR[cIndex] + cAlignment;
				rowIndex--;
			} else if (substitution == currentCost) {
				uAlignment = uLR[uIndex] + uAlignment;
				cAlignment = cLR[cIndex] + cAlignment;
				rowIndex--;
				columnIndex--;
			} else {
				std::cerr << "ERROR CODE 5: No paths found. Terminating backtracking.\n";
				rowIndex = 0;
				columnIndex = 0;
			}
		}
	}
}
