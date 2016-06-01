#include <iostream>
#include <string>
#include <algorithm>
#include <limits>
#include <cmath>
#include "alignments.hpp"

Alignments::Alignments(std::string reference, std::string uLongRead, std::string cLongRead)
{
	ref = reference;
	ulr = uLongRead;
	clr = cLongRead;
	rows = clr.length() + 1;
	columns = ulr.length() + 1;
	initialize();
}

Alignments::Alignments(const Alignments &alignments)
{
	// First, copy all member fields
	clr = alignments.clr;
	ulr = alignments.ulr;
	ref = alignments.ref;
	clrMaf = alignments.refMaf;
	ulrMaf = alignments.ulrMaf;
	refMaf = alignments.refMaf;
	cAlignment = alignments.cAlignment;
	refAlignment = alignments.refAlignment;
	rows = alignments.rows;
	columns = alignments.columns;
	distance = alignments.distance;
	
	// Next, copy the matrix
	// Allocate memory for the matrix
	
	try {
		matrix = new int*[rows];
	} catch (std::bad_alloc& b) {
		std::cerr << "Memory allocation failed; unable to copy DP matrix.\n";
	}

	for (int rowIndex = 0; rowIndex < rows; rowIndex++) {
		try {
			matrix[rowIndex] = new int[columns];
		} catch (std::bad_alloc& ba) {
			std::cerr << "Memory allocation failed; unable to copy DP matrix.\n";
		}
	}

	int columnIndex;
	
	for (int rowIndex = 0; rowIndex < rows; rowIndex++) {
		for (columnIndex = 0; columnIndex < columns; columnIndex++) {
			matrix[rowIndex][columnIndex] = alignments.matrix[rowIndex][columnIndex];
		}
	}
}

Alignments::~Alignments(void)
{
	deleteMatrix();
}

void Alignments::reset(std::string reference, std::string uLongRead, std::string cLongRead)
{
	// Resets in case of need to reassign values of object
	deleteMatrix();
	ref = reference;
	ulr = uLongRead;
	clr = cLongRead;
	rows = clr.length() + 1;
	columns = ulr.length() + 1;
	initialize();
}

void Alignments::initialize()
{
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
	distance = matrix[rows-1][columns-1];
	findAlignments();
	processAlignments();
}

void Alignments::deleteMatrix()
{
	for (int rowIndex = 0; rowIndex < rows; rowIndex++) {
		delete matrix[rowIndex]; // In the future, add check to see if not null
	}
	delete matrix;
}

std::string Alignments::getClr()
{
	return clrMaf;
}


std::string Alignments::getUlr()
{
	return ulrMaf;
}

std::string Alignments::getRef()
{
	return refMaf;
}

std::string Alignments::get_cAlignment()
{
	return cAlignment;
}

std::string Alignments::getRefAlignment()
{
	return refAlignment;
}

int Alignments::getDistance()
{
	return distance;
}

void Alignments::printMatrix()
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

int Alignments::cost(char refBase, char cBase)
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

void Alignments::findAlignments()
{
	clrMaf = "";
	ulrMaf = "";
	refMaf = "";
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
		/*
		std::cout << "rowIndex == " << rowIndex << "\n";
		std::cout << "columnIndex == " << columnIndex << "\n";
		std::cout << "Before\n";
		std::cout << "clrMaf == " << clrMaf << "\n";
		std::cout << "ulrMaf == " << ulrMaf << "\n";
		std::cout << "refMaf == " << refMaf << "\n";
		*/

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
		if (rowIndex == 0 || columnIndex == 0) {
				//std::cout << "Path 6\n";
				if (rowIndex == 0) {
					//std::cout << "Deletion\n";
					clrMaf = '-' + clrMaf;
					ulrMaf = ulr[urIndex] + ulrMaf;
					refMaf = ref[urIndex] + refMaf;
					columnIndex--;
				} else {
					//std::cout << "Insertion\n";
					clrMaf = clr[cIndex] + clrMaf;
					ulrMaf = '-' + ulrMaf;
					refMaf = '-' + refMaf;
					rowIndex--;
				}
		} else if (isEndingLC) {
			if ( toupper( ulr[urIndex] ) == toupper( clr[cIndex] ) ) {
				//std::cout << "Path 1\n";
				if (deletion == currentCost) {
					//std::cout << "Deletion\n";
					clrMaf = '-' + clrMaf;
					ulrMaf = ulr[urIndex] + ulrMaf;
					refMaf = ref[urIndex] + refMaf;
					columnIndex--;
				} else if (substitute == currentCost) {
					//std::cout << "Substitution\n";
					clrMaf = clr[cIndex] + clrMaf;
					ulrMaf = ulr[urIndex] + ulrMaf;
					refMaf = ref[urIndex] + refMaf;
					rowIndex--;
					columnIndex--;
				} else {
					std::cerr << "ERROR CODE 1: No paths found. Terminating backtracking.\n";	
					rowIndex = 0;
					columnIndex = 0;
				}
			} else {
				//std::cout << "Path 2\n";
				if (deletion == currentCost) {
					//std::cout << "Deletion\n";
					clrMaf = '-' + clrMaf;
					ulrMaf = ulr[urIndex] + ulrMaf;
					refMaf = ref[urIndex] + refMaf;
					columnIndex--;
				} else {
					std::cerr << "ERROR CODE 2: No paths found. Terminating backtracking.\n";
					rowIndex = 0;
					columnIndex = 0;
				}
			}
		} else if (islower(clr[cIndex]) && rowIndex > 0 && columnIndex > 0) {
			if ( toupper( ulr[urIndex] ) == toupper( clr[cIndex] ) ) {
				//std::cout << "Path 3\n";
				if (substitute == currentCost) {
					//std::cout << "Substitution\n";
					clrMaf = clr[cIndex] + clrMaf;	
					ulrMaf = ulr[urIndex] + ulrMaf;
					refMaf = ref[urIndex] + refMaf;
					rowIndex--;
					columnIndex--;
				} else {
					std::cerr << "ERROR CODE 3: No paths found. Terminating backtracking.\n";
					rowIndex = 0;
					columnIndex = 0;
				}
			} else if (ulr[urIndex] == '-') {
				//std::cout << "Path 4\n";
				deletion = matrix[rowIndex][columnIndex-1];
				if (deletion == currentCost) {
					//std::cout << "Deletion\n";
					clrMaf = '-' + clrMaf;
					ulrMaf = ulr[urIndex] + ulrMaf;
					refMaf = ref[urIndex] + refMaf;
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
		} else {
			//std::cout << "Path 5\n";
			if (deletion == currentCost) {
				//std::cout << "Deletion\n";
				clrMaf = '-' + clrMaf;
				ulrMaf = ulr[urIndex] + ulrMaf;
				refMaf = ref[urIndex] + refMaf;
				columnIndex--;
			} else if (insert == currentCost) {
				//std::cout << "Insertion\n";
				clrMaf = clr[cIndex] + clrMaf;
				ulrMaf = '-' + ulrMaf;
				refMaf = '-' + refMaf;
				rowIndex--;
			} else if (substitute == currentCost) {
				//std::cout << "Substitution\n";
				clrMaf = clr[cIndex] + clrMaf;
				ulrMaf = ulr[urIndex] + ulrMaf;
				refMaf = ref[urIndex] + refMaf;
				rowIndex--;
				columnIndex--;
			} else {
				std::cerr << "ERROR CODE 6: No paths found. Terminating backtracking.\n";
				rowIndex = 0;
				columnIndex = 0;
			}
		} 		
		/*
		std::cout << "After\n";
		std::cout << "clrMaf == " << clrMaf << "\n";
		std::cout << "ulrMaf == " << ulrMaf << "\n";
		std::cout << "refMaf == " << refMaf << "\n\n";
		*/
	}
}

void Alignments::processAlignments()
{
	// Remove all pairs of the form (-,-)
	cAlignment = "";
	refAlignment = "";	
	int length = clrMaf.length();

	for (int i = 0; i < length; i++) {
		if (clrMaf[i] != '-' || refMaf[i] != '-') {
			cAlignment = cAlignment + clrMaf[i];
			refAlignment = refAlignment + refMaf[i];
		}
	}
}
