#include <iostream>
#include <string>
#include <algorithm>
#include <limits>
#include <cmath>

class OptimalAlignment
{
	public:
		OptimalAlignment(std::string refMaf, std::string ulrMaf, std::string cLR);
		~OptimalAlignment();
		std::string get_cAlignment();
	private:
		std::string ref;
		std::string ulr;
		std::string clr;
		int rows;
		int columns;
		int** matrix;
		std::string cAlignment;
		int cost(int urIndex, int cIndex);
		void findAlignments();
};

OptimalAlignment::OptimalAlignment(std::string refMaf, std::string ulrMaf, std::string cLR)
{
	ref = refMaf;
	ulr = ulrMaf;
	clr = cLR;
	rows = clr.length() + 1;
	columns = ulr.length() + 1;
	int cIndex;
	int urIndex;
	bool isEndingLC;
	int keep;
	int substitute;
	int insert;
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
			urIndex = columnIndex -  1;

			// Determine if the current letter in clr is lowercase and is followed by an upper case letter
			// i.e. if the current letter in clr is an ending lowercase letter
			if ( cIndex < clr.length() - 1 && islower(clr[cIndex]) && isupper(clr[cIndex+1]) ) {
				isEndingLC = true;	
			} else {
				isEndingLC = false;
			}

			if (isEndingLC) {
				// If both letters are the same, we can either keep both letters or deletion the one from
				// clr. If they are different, we can't keep both so we can only consider deleting the
				// one from clr.
				if ( toupper(ulr[urIndex]) == toupper(clr[cIndex]) ) {
					keep = std::abs( matrix[rowIndex-1][columnIndex-1] + cost(urIndex, cIndex) );
					deletion = std::abs( matrix[rowIndex][columnIndex-1] + cost(urIndex, cIndex) );
					matrix[rowIndex][columnIndex] = std::min(keep, deletion); 
				} else {
					matrix[rowIndex][columnIndex] = std::abs( matrix[rowIndex][columnIndex-1] 
									+ cost(urIndex, cIndex) );
				}
			} else if (islower(clr[cIndex])) {
				// Setting the position in the matrix to infinity ensures that we can never
				// find an alignment where the uncorrected segments are not perfectly aligned.
				if ( toupper( ulr[urIndex] ) == toupper( clr[cIndex] ) ) {
					matrix[rowIndex][columnIndex] = std::abs( matrix[rowIndex-1][columnIndex-1] 
									+ cost(urIndex, cIndex) );
				} else if (ulr[urIndex] == '-') {
					matrix[rowIndex][columnIndex] = matrix[rowIndex-1][columnIndex-1]; //Zero cost deletion
				} else {
					matrix[rowIndex][columnIndex] = infinity;
				}
			} else {
				// Usual Levenshtein distance equations.
				deletion = std::abs( matrix[rowIndex][columnIndex-1] + cost(urIndex, cIndex) );
				insert = std::abs( matrix[rowIndex-1][columnIndex] + cost(urIndex, cIndex) );
				substitute = std::abs( matrix[rowIndex-1][columnIndex-1] + cost(urIndex, cIndex) );
				matrix[rowIndex][columnIndex] = std::min( deletion, std::min(insert, substitute) ); 
			}
		}		
	}
	findAlignments();
}

OptimalAlignment::~OptimalAlignment(void)
{
	for (int rowIndex = 0; rowIndex < rows; rowIndex++) {
		deletion matrix[rowIndex];
	}
	deletion matrix;
}

std::string OptimalAlignment::get_uAlignment()
{
	return uAlignment;
}

std::string OptimalAlignment::get_cAlignment()
{
	return cAlignment;
}

int OptimalAlignment::cost(int urIndex, int cIndex)
{
	if ( islower(clr[cIndex]) ) {
		return 0;
	} else if ( toupper( ulr[urIndex] ) == toupper( clr[cIndex] ) ) {
		return 0;
	} else {
		return 2;
	}
}

void OptimalAlignment::findAlignments()
{
	cAlignment = "";
	uAlignment = "";
	int rowIndex = rows - 1;
	int columnIndex = columns - 1;
	int cIndex;
	int urIndex;
	int insert;
	int deletion;
	int substitute;
	int currentCost;
	bool isEndingLC;
	int infinity = std::numeric_limits<int>::max();

	// Follow the best path from the bottom right to the top left of the matrix.
	// This is equivalent to the optimal alignment between ulr and clr.
	// The path we follow is restricted to the conditions set when computing the matrix,
	// i.e. we can never follow a path that the edit distance equations do not allow.
	while (rowIndex > 0 || columnIndex > 0) {
		urIndex = columnIndex - 1;
		cIndex = rowIndex - 1;
		currentCost = matrix[rowIndex][columnIndex];
		// Set the costs of the different operations, 
		// ensuring we don't go out of bounds of the matrix.
		if (rowIndex > 0 && columnIndex > 0) {
			deletion = matrix[rowIndex][columnIndex-1] + del;
			insert = matrix[rowIndex-1][columnIndex] + ins;
			substitute = matrix[rowIndex-1][columnIndex-1] + cost(urIndex, cIndex);	
		} else if (rowIndex <= 0 && columnIndex > 0) {
			deletion = matrix[rowIndex][columnIndex-1] + del;
			insert = infinity;
			substitute = infinity;
		} else if (rowIndex > 0 && columnIndex <= 0) {
			deletion = infinity;
			insert = matrix[rowIndex-1][columnIndex] + ins;
			substitute = infinity;
		} 

		// Make sure we follow the same path as dictated by the edit distance equations. 
		if ( cIndex < clr.length() - 1 && islower(clr[cIndex]) && isupper(clr[cIndex+1]) ) {
			isEndingLC = true;	
		} else {
			isEndingLC = false;
		}

		if (isEndingLC) {
			if ( toupper( ulr[urIndex] ) == toupper( clr[cIndex] ) ) {
				if (deletion == currentCost) {
					uAlignment = ulr[urIndex] + uAlignment;
					cAlignment = "-" + cAlignment;
					columnIndex--;
				} else if (substitute == currentCost) {
					uAlignment = ulr[urIndex] + uAlignment;
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
					uAlignment = ulr[urIndex] + uAlignment;
					cAlignment = "-" + cAlignment;
					columnIndex--;
				} else {
					std::cerr << "ERROR CODE 2: No paths found. Terminating backtracking.\n";
					rowIndex = 0;
					columnIndex = 0;
				}
			}
		} else if (islower(clr[cIndex])) {
			if (substitute == currentCost) {
				uAlignment = ulr[urIndex] + uAlignment;
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
				uAlignment = ulr[urIndex] + uAlignment;
				cAlignment = "-" + cAlignment;
				columnIndex--;
			} else if (insert == currentCost) {
				uAlignment = "-" + uAlignment;
				cAlignment = clr[cIndex] + cAlignment;
				rowIndex--;
			} else if (substitute == currentCost) {
				uAlignment = ulr[urIndex] + uAlignment;
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
