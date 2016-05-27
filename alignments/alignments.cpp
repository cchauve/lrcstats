#include <iostream>
#include <string>
#include <algorithm>
#include <limits>
#include <cmath>
#include <

class OptimalAlignment
{
	public:
		OptimalAlignment(std::string refMaf, std::string ulrMaf, std::string cLR);
		~OptimalAlignment();
		std::string get_uAlignment();
		std::string get_cAlignment();
	private:
		std::string ulr;
		std::string clr;
		std::string ref;
		int rows;
		int columns;
		int** matrix;
		int del;
		int ins;
		int sub;
		std::string uAlignment;
		std::string cAlignment;
		int cost(int uIndex, int cIndex);
		void findAlignments();
};

OptimalAlignment::OptimalAlignment(std::string refMaf, std::string ulrMaf, std::string cLR)
{
	del = 1;
	ins = 1;
	sub = 1;
	ulr = ulrMaf;
	clr = cLR;
	rows = clr.length() + 1;
	columns = ulr.length() + 1;
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

	// Find the optimal edit distance such that all uncorrected segments of clr are aligned with uncorrected
 	// portions of ulr. 
	for (int rowIndex = 1; rowIndex < rows; rowIndex++) {
		for (int columnIndex = 1; columnIndex < columns; columnIndex++) {
			cIndex = rowIndex - 1;
			uIndex = columnIndex -  1;

			// Determine if the current letter in clr is lowercase and is followed by an upper case letter
			// i.e. if the current letter in clr is an ending lowercase letter
			if ( cIndex < clr.length() - 1 && islower(clr[cIndex]) && isupper(clr[cIndex+1]) ) {
				isEndingLC = true;	
			} else {
				isEndingLC = false;
			}

			if (isEndingLC) {
				// If both letters are the same, we can either keep both letters or delete the one from
				// clr. If they are different, keeping both violates the schema so we can only consider deleting the
				// one from clr.
				if ( toupper(ulr[uIndex]) == toupper(clr[cIndex]) ) {
					keep = matrix[rowIndex-1][columnIndex-1];
					deletion = std::abs( matrix[rowIndex][columnIndex-1] + del );
					matrix[rowIndex][columnIndex] = std::min(keep, deletion); 
				} else {
					matrix[rowIndex][columnIndex] = std::abs( matrix[rowIndex][columnIndex-1] + del );
				}
			} else if (islower(clr[cIndex])) {
				// Setting the position in the matrix to infinity ensures that we can never
				// find an alignment where the uncorrected segments are not perfectly aligned.
				if ( toupper( ulr[uIndex] ) == toupper( clr[cIndex] ) ) {
					matrix[rowIndex][columnIndex] = matrix[rowIndex-1][columnIndex-1];
				} else if ( ulr[uIndex] == '-' ) {
					matrix[rowIndex][columnIndex] = matrix[rowIndex][columnIndex-1]; //Constant deletion
				} else {
					matrix[rowIndex][columnIndex] = infinity;
				}
			} else {
				// Usual Levenshtein distance equations.
				matrix[rowIndex][columnIndex] = cost(uIndex, cIndex);
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

int OptimalAlignment::cost(int uIndex, int cIndex)
{
	if (islower(clr[cIndex])) {
		return 0
	}
	else if (toupper(ref[uIndex]) == clr[cIndex]) {
		return 2;
	} else {
		return 0;
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
	// This is equivalent to the optimal alignment between ulr and clr.
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
			substitution = matrix[rowIndex-1][columnIndex-1] + cost(uIndex, cIndex);	
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
		if ( cIndex < clr.length() - 1 && islower(clr[cIndex]) && isupper(clr[cIndex+1]) ) {
			isEndingLC = true;	
		} else {
			isEndingLC = false;
		}

		if (isEndingLC) {
			if ( toupper( ulr[uIndex] ) == toupper( clr[cIndex] ) ) {
				if (deletion == currentCost) {
					uAlignment = ulr[uIndex] + uAlignment;
					cAlignment = "-" + cAlignment;
					columnIndex--;
				} else if (substitution == currentCost) {
					uAlignment = ulr[uIndex] + uAlignment;
					cAlignment = clr[cIndex] + cAlignment;
					rowIndex--;
					columnIndex--;
				} else {
					std::cerr << "ERROR CODE 1: No paths found. Terminating backtracking.\n";	
					rowIndex = 0;
					columnIndex = 0;
				}
			} else {
				if (deletion == currentCost) {
					uAlignment = ulr[uIndex] + uAlignment;
					cAlignment = "-" + cAlignment;
					columnIndex--;
				} else {
					std::cerr << "ERROR CODE 2: No paths found. Terminating backtracking.\n";
					rowIndex = 0;
					columnIndex = 0;
				}
			}
		} else if (islower(clr[cIndex])) {
			if (substitution == currentCost) {
				uAlignment = ulr[uIndex] + uAlignment;
				cAlignment = clr[cIndex] + cAlignment;
				rowIndex--;
				columnIndex--;
			} else {
				std::cerr << "ERROR CODE 4: No paths found. Terminating backtracking.\n";
				rowIndex = 0;
				columnIndex = 0;
			}
		} else {
			if (deletion == currentCost) {
				uAlignment = ulr[uIndex] + uAlignment;
				cAlignment = "-" + cAlignment;
				columnIndex--;
			} else if (insertion == currentCost) {
				uAlignment = "-" + uAlignment;
				cAlignment = clr[cIndex] + cAlignment;
				rowIndex--;
			} else if (substitution == currentCost) {
				uAlignment = ulr[uIndex] + uAlignment;
				cAlignment = clr[cIndex] + cAlignment;
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
