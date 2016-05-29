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
		std::string getRefAlignment();
		int getDistance();
	private:
		std::string ref;
		std::string ulr;
		std::string clr;
		int rows;
		int columns;
		int** matrix;
		std::string cAlignment;
		std::string refAlignment;
		int distance;
		void printMatrix();
		int cost(char refBase, char cBase);
		void findAlignments();
		void processAlignments();
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
					keep = std::abs( matrix[rowIndex-1][columnIndex-1] + cost(ref[urIndex], clr[cIndex]) );
					deletion = std::abs( matrix[rowIndex][columnIndex-1] + cost(ref[urIndex], '-') );
					matrix[rowIndex][columnIndex] = std::min(keep, deletion); 
				} else {
					matrix[rowIndex][columnIndex] = std::abs( matrix[rowIndex][columnIndex-1] + cost(ref[urIndex], '-') ); 
				}
			} else if (islower(clr[cIndex])) {
				if ( toupper( ulr[urIndex] ) == toupper( clr[cIndex] ) ) {
					// Keep the characters if they are the same
					matrix[rowIndex][columnIndex] = std::abs( matrix[rowIndex-1][columnIndex-1] + cost(ref[urIndex], clr[cIndex]) );
				} else if (ulr[urIndex] == '-') {
					// If uLR has a dash, the optimal solution is just to call a deletion.
					matrix[rowIndex][columnIndex] = matrix[rowIndex][columnIndex-1]; //Zero cost deletion
				} else {
					// Setting the position in the matrix to infinity ensures that we can never
					// find an alignment where the uncorrected segments are not perfectly aligned.
					matrix[rowIndex][columnIndex] = infinity;
				}
			} else {
				// Usual Levenshtein distance equations.
				deletion = std::abs( matrix[rowIndex][columnIndex-1] + cost(ref[urIndex], '-') );
				insert = std::abs( matrix[rowIndex-1][columnIndex] + cost('-', clr[cIndex]) );
				substitute = std::abs( matrix[rowIndex-1][columnIndex-1] + cost(ref[urIndex], clr[cIndex]) );
				matrix[rowIndex][columnIndex] = std::min( deletion, std::min(insert, substitute) ); 
			}
		}		
	}
	findAlignments();
	processAlignments();
}

OptimalAlignment::~OptimalAlignment(void)
{
	for (int rowIndex = 0; rowIndex < rows; rowIndex++) {
		delete matrix[rowIndex];
	}
	delete matrix;
}

std::string OptimalAlignment::get_cAlignment()
{
	return cAlignment;
}

std::string OptimalAlignment::getRefAlignment()
{
	return refAlignment;
}

int OptimalAlignment::getDistance()
{
	return distance;
}

void OptimalAlignment::printMatrix()
{
	int columnIndex;
	int infinity = std::numeric_limits<int>::max();

	for (int rowIndex = 0; rowIndex < rows; rowIndex++) {
		for (columnIndex = 0; columnIndex < columns; columnIndex++) {
			if (matrix[rowIndex][columnIndex] == infinity) {
				std::cout << '-' << "  ";
			} else if (matrix[rowIndex][columnIndex] < 10) {
				std::cout << matrix[rowIndex][columnIndex] << "  ";
			} else {
				std::cout << matrix[rowIndex][columnIndex] << " ";
			}
		}
		std::cout << "\n";
	}
}

int OptimalAlignment::cost(char refBase, char cBase)
{
	if ( islower(cBase) ) {
		return 0;
	} else if ( toupper(refBase) == cBase ) {
		return 0;
	} else {
		// Ideally, in an alignment between cLR and ref we want to minimize the number of discrepancies
		// as much as possible, so if both bases are different, we assign a cost of 2.
		return 2;
	}
}

void OptimalAlignment::findAlignments()
{
	cAlignment = "";
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
			deletion = matrix[rowIndex][columnIndex-1] + cost(ref[urIndex], '-');
			insert = matrix[rowIndex-1][columnIndex] + cost('-', clr[cIndex]);
			substitute = matrix[rowIndex-1][columnIndex-1] + cost(ref[urIndex], clr[cIndex]);	
		} else if (rowIndex <= 0 && columnIndex > 0) {
			deletion = matrix[rowIndex][columnIndex-1] + cost(ref[urIndex], '-');
			insert = infinity;
			substitute = infinity;
		} else if (rowIndex > 0 && columnIndex <= 0) {
			deletion = infinity;
			insert = matrix[rowIndex-1][columnIndex] + cost('-', clr[cIndex]);
			substitute = infinity;
		} 

		// Make sure we follow the same path as dictated by the edit distance equations. 
		if ( cIndex < clr.length() - 1 && islower(clr[cIndex]) && isupper(clr[cIndex+1]) ) {
			isEndingLC = true;	
		} else {
			isEndingLC = false;
		}

		if (isEndingLC && rowIndex > 0 && columnIndex > 0) {
			if ( toupper( ulr[urIndex] ) == toupper( clr[cIndex] ) ) {
				if (deletion == currentCost) {
					cAlignment = '-' + cAlignment;
					refAlignment = ref[urIndex] + refAlignment;
					columnIndex--;
				} else if (substitute == currentCost) {
					cAlignment = clr[cIndex] + cAlignment;
					refAlignment = ref[urIndex] + refAlignment;
					rowIndex--;
					columnIndex--;
				} else {
					std::cerr << "ERROR CODE 1: No paths found. Terminating backtracking.\n";	
					rowIndex = 0;
					columnIndex = 0;
				}
			} else {
				if (deletion == currentCost) {
					cAlignment = '-' + cAlignment;
					refAlignment = ref[urIndex] + refAlignment;
					columnIndex--;
				} else {
					std::cerr << "ERROR CODE 2: No paths found. Terminating backtracking.\n";
					rowIndex = 0;
					columnIndex = 0;
				}
			}
		} else if (islower(clr[cIndex]) && rowIndex > 0 && columnIndex > 0) {
			if ( toupper( ulr[urIndex] ) == toupper( clr[cIndex] ) ) {
				if (substitute == currentCost) {
					cAlignment = clr[cIndex] + cAlignment;	
					refAlignment = ref[urIndex] + refAlignment;
					rowIndex--;
					columnIndex--;
				} else {
					std::cerr << "ERROR CODE 3: No paths found. Terminating backtracking.\n";
					rowIndex = 0;
					columnIndex = 0;
				}
			} else if (ulr[urIndex] == '-') {
				deletion = matrix[rowIndex][columnIndex-1];
				if (deletion == currentCost) {
					cAlignment = '-' + cAlignment;
					refAlignment = ref[urIndex] + refAlignment;
					columnIndex--;
				} else {
					std::cerr << "ERROR CODE 4: No paths found. Terminating backtracking.\n";
					rowIndex = 0;
					columnIndex = 0;
				}
			} else {
				std::cerr << "ERROR CODE 5: No paths found. Terminating backtracking.\n";
				rowIndex = 0;
				columnIndex = 0;
			}
		} else if (rowIndex > 0 && columnIndex > 0) {
			if (deletion == currentCost) {
				cAlignment = '-' + cAlignment;
				refAlignment = ref[urIndex] + refAlignment;
				columnIndex--;
			} else if (insert == currentCost) {
				cAlignment = clr[cIndex] + cAlignment;
				refAlignment = '-' + refAlignment;
				rowIndex--;
			} else if (substitute == currentCost) {
				cAlignment = clr[cIndex] + cAlignment;
				refAlignment = ref[urIndex] + refAlignment;
				rowIndex--;
				columnIndex--;
			} else {
				std::cerr << "ERROR CODE 6: No paths found. Terminating backtracking.\n";
				rowIndex = 0;
				columnIndex = 0;
			}
		} else {
			if (rowIndex == 0) {
				cAlignment = '-' + cAlignment;
				refAlignment = ref[urIndex] + refAlignment;
				columnIndex--;
			} else {
				cAlignment = clr[cIndex] + cAlignment;
				refAlignment = '-' + refAlignment;
				rowIndex--;
			}
		}
	}
}

void OptimalAlignment::processAlignments()
{
	// Remove all pairs of the form (-,-)
	std::string clrTemp = "";
	std::string refTemp = "";	
	int length = cAlignment.length();

	for (int i = 0; i < length; i++) {
		if (cAlignment[i] != '-' || refAlignment[i] != '-') {
			clrTemp = clrTemp + cAlignment[i];
			refTemp = refTemp + refAlignment[i];
		}
	}
	cAlignment = clrTemp;
	refAlignment = refTemp;
}
