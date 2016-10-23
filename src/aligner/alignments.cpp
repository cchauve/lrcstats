#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <limits>
#include <cmath>
#include <cassert>
#include <cstdint>
// for std::exit
#include <cstdlib>

#include "alignments.hpp"
#include "data.hpp"

Alignments::Alignments()
/* Constructor for general reads class - is the parent of UntrimmedAlignments and TrimmedAlignments */
{
	ref = "";
	ulr = "";
	clr = "";
	refAlignment = "";
	ulrAlignment = "";
	clrAlignment = "";
	matrix = NULL;
}

Alignments::~Alignments()
/* Delete the matrix when calling the destructor */
{
	deleteMatrix();
}

Read_t Alignments::align(std::string reference, std::string uRead, std::string cRead)
{
	ref = reference;
	ulr = uRead;
	clr = cRead;
	deleteMatrix();
	preprocessReads();
	createMatrix();
	findAlignments();
	Read_t alignedReads;
	alignedReads.ref = refAlignment;
	alignedReads.ulr = ulrAlignment;
	alignedReads.clr = clrAlignment;
	return alignedReads;
}

void Alignments::preprocessReads()
{
	rows = clr.length() + 1;
	columns = ulr.length() + 1;
}

void Alignments::createMatrix()
/* Preconstruct the matrix */
{
	try {
		matrix = new int64_t*[rows];
	} catch( std::bad_alloc& ba ) {
		std::cout << "Memory allocation failed; unable to create DP matrix.\n";
	}
	for (int64_t rowIndex = 0; rowIndex < rows; rowIndex++) {
		try {
			matrix[rowIndex] = new int64_t[columns];
		} catch( std::bad_alloc& ba ) {
			std::cout << "Memory allocation failed; unable to create DP matrix.\n";
		}
	}
	// Set the base cases for the DP matrix
	for (int64_t rowIndex = 0; rowIndex < rows; rowIndex++) {
		matrix[rowIndex][0] = rowBaseCase(rowIndex);	
	}
	for (int64_t columnIndex = 1; columnIndex < columns; columnIndex++) {
		matrix[0][columnIndex] = columnBaseCase(columnIndex);
	}
	for (int64_t rowIndex = 1; rowIndex < rows; rowIndex++) {
		for (int64_t columnIndex = 1; columnIndex < columns; columnIndex++) {
			matrix[rowIndex][columnIndex] = editDistance(rowIndex,columnIndex);
		}
	}
}

void Alignments::deleteMatrix()
/* Delete the matrix allocated in the heap */
{
	if (matrix != NULL) {
		for (int64_t rowIndex = 0; rowIndex < rows; rowIndex++) {
			if (matrix[rowIndex] != NULL) {
				delete matrix[rowIndex];
			} 	
		}
		delete matrix;
	}
}

int64_t Alignments::rowBaseCase(int64_t rowIndex)
{
	return rowIndex*10;
}

int64_t Alignments::columnBaseCase(int64_t columnIndex)
{
	return columnIndex*10;
}	

int64_t Alignments::editDistance(int64_t rowIndex, int64_t columnIndex) {}


void Alignments::findAlignments() {}

int64_t Alignments::cost(char refBase, char cBase)
/* Cost function for dynamic programming algorithm */
{
	if ( toupper(refBase) == toupper(cBase) ) {
		return 0;
	} else {
		return 10;
	}
}

void Alignments::printMatrix()
/* Print the matrix */
{
	int64_t infinity = std::numeric_limits<int64_t>::max();
	for (int64_t rowIndex = 0; rowIndex < rows; rowIndex++) {
		for (int64_t columnIndex = 0; columnIndex < columns; columnIndex++) {
			int64_t val = matrix[rowIndex][columnIndex];
			if (val == infinity) {
				std::cout << "- ";
			} else {
				std::cout << val << " ";
			}
		}
		std::cout << "\n";
	}
}

/*--------------------------------------------------------------------------------------------------------*/

UntrimmedAlignments::UntrimmedAlignments() : Alignments() {}

bool UntrimmedAlignments::checkIfEndingLowerCase(int64_t cIndex)
/* Determine if we're at an ending lower case i.e. if the current base
 * in cLR is lowercase and the following base is uppercase or the
 * current base is lowercase and the last base in the sequene.
 */
{
	if ( (cIndex < clr.length() - 1 and islower(clr[cIndex]) and isupper(clr[cIndex+1])) or 
	     (cIndex == clr.length() - 1 and islower(clr[cIndex])) ) {
		return true;
	} else {
		return false;
	}
}

bool UntrimmedAlignments::isBeginningCorrectedIndex(int64_t cIndex)
{
	// The current base is the beginning base of a corrected segment is
	// it is the very first base of the entire cLR and it is uppercase or
	// the previous base is an ending lowercase base
	if ( (cIndex == 0 and isupper(clr[cIndex])) or checkIfEndingLowerCase(cIndex-1) ) {
		return true;
	} else {
		return false;
	}
}

bool UntrimmedAlignments::isEndingCorrectedIndex(int64_t cIndex)
{
	if ( isupper(clr[cIndex]) and (cIndex == clr.length() - 1 or islower(clr[cIndex+1])) ) {
		return true;
	} else {
		return false;
	} 
}

int64_t UntrimmedAlignments::levenshteinDistance(int64_t rowIndex, int64_t columnIndex)
{
	int64_t cIndex = rowIndex - 1;
	int64_t urIndex = columnIndex - 1;
	int64_t deletion = std::abs( matrix[rowIndex][columnIndex-1] + cost(ref[urIndex], '-') );
	int64_t insert = std::abs( matrix[rowIndex-1][columnIndex] + cost('-', clr[cIndex]) );
	int64_t substitute = std::abs( matrix[rowIndex-1][columnIndex-1] + cost(ref[urIndex], clr[cIndex]) );
	return std::min( deletion, std::min(insert,substitute) );
}


int64_t UntrimmedAlignments::editDistance(int64_t rowIndex, int64_t columnIndex)
/* Given cLR, uLR and ref sequences, construct the DP matrix for the optimal alignments. 
 * Requires these member variables to be set before use. */
{
	int64_t infinity = std::numeric_limits<int64_t>::max();
	int64_t cIndex = rowIndex - 1;
	int64_t urIndex = columnIndex -  1;
	bool isEndingLC = checkIfEndingLowerCase(cIndex);

	if (isEndingLC) {
		// If both letters are the same, we can either keep both letters or deletion the one from
		// clr. If they are different, we can't keep both so we can only consider deleting the
		// one from clr.
		if ( toupper(ulr[urIndex]) == toupper(clr[cIndex]) ) {
			int64_t keep = std::abs(matrix[rowIndex-1][columnIndex-1] + cost(ref[urIndex], clr[cIndex]));
			int64_t deletion = std::abs( matrix[rowIndex][columnIndex-1] + cost(ref[urIndex], '-') );
			return std::min(keep, deletion); 
		} else {
			return std::abs( matrix[rowIndex][columnIndex-1] + cost(ref[urIndex], '-') ); 
		}
	} else if (islower(clr[cIndex])) {
		if ( toupper( ulr[urIndex] ) == toupper( clr[cIndex] ) ) {
			// Keep the characters if they are the same
			return std::abs( matrix[rowIndex-1][columnIndex-1] + cost(ref[urIndex], clr[cIndex]) );
		} else if (ulr[urIndex] == '-') {
			// If uLR has a dash, the optimal solution is just to call a deletion.
			return matrix[rowIndex][columnIndex-1]; //Zero cost deletion
		} else {
			// Setting the position in the matrix to infinity ensures that we can never
			// find an alignment where the uncorrected segments are not perfectly aligned.
			return infinity;
		}
	} else {
		return levenshteinDistance(rowIndex,columnIndex);
	}
}

void UntrimmedAlignments::operationCosts(int64_t rowIndex, int64_t columnIndex, 
                                         int64_t& deletion, int64_t& insert, int64_t& substitute)
{
	int64_t infinity = std::numeric_limits<int64_t>::max();
	int64_t cIndex = rowIndex - 1;
	int64_t urIndex = columnIndex - 1;
	if (rowIndex > 0 and columnIndex > 0) {
		deletion = std::abs(matrix[rowIndex][columnIndex-1] + cost(ref[urIndex], '-'));
		insert = std::abs(matrix[rowIndex-1][columnIndex] + cost('-', clr[cIndex]));
		substitute = std::abs(matrix[rowIndex-1][columnIndex-1] + cost(ref[urIndex], clr[cIndex]));
	} else if (rowIndex <= 0 and columnIndex > 0) {
		deletion = std::abs(matrix[rowIndex][columnIndex-1] + cost(ref[urIndex], '-'));
		insert = infinity;
		substitute = infinity;
	} else if (rowIndex > 0 and columnIndex <= 0) {
		deletion = infinity;
		insert = std::abs(matrix[rowIndex-1][columnIndex] + cost('-', clr[cIndex]));
		substitute = infinity;
	} 
}

void UntrimmedAlignments::findAlignments()
/* Backtracks through the DP matrix to find the optimal alignments. 
 * Follows same schema as the DP algorithm for untrimmed corrected long reads. 
 * Inserts X chars around corrected sequences in the alignment
 * to indicate the start and end of corrected sequences. 
 */
{
	int64_t rowIndex = rows - 1;
	int64_t columnIndex = columns - 1;
	std::string clrMaf = "";
	std::string ulrMaf = "";
	std::string refMaf = "";
	// Follow the best path from the bottom right to the top left of the matrix.
	// This is equivalent to the optimal alignment between ulr and clr.
	// The path we follow is restricted to the conditions set when computing the matrix,
	// i.e. we can never follow a path that the edit distance equations do not allow.
	while (rowIndex > 0 or columnIndex > 0) {
		int64_t urIndex = columnIndex - 1;
		int64_t cIndex = rowIndex - 1;
		int64_t currentCost = matrix[rowIndex][columnIndex];
		int64_t deletion;
		int64_t insert;
		int64_t substitute;
		// Set the costs of the different operations, 
		// also ensuring we don't go out of bounds of the matrix.
		operationCosts(rowIndex,columnIndex,deletion,insert,substitute);
		// check to see if the current base in the corrected long read is lowercase
		bool isEndingLC = checkIfEndingLowerCase(cIndex);
		bool endingCorrectedBase = isEndingCorrectedIndex(cIndex);
		bool beginningCorrectedBase = isBeginningCorrectedIndex(cIndex);

		if (rowIndex == 0) {
			clrMaf = '-' + clrMaf;
			ulrMaf = ulr[urIndex] + ulrMaf;
			refMaf = ref[urIndex] + refMaf;
			columnIndex--;
		} else if (columnIndex == 0) {
			// Insert the right boundary of the corrected segment
			if (endingCorrectedBase) {
				refMaf = '-' + refMaf;
				ulrMaf = 'X' + ulrMaf;
				clrMaf = 'X' + clrMaf;	
			}
			clrMaf = clr[cIndex] + clrMaf;
			ulrMaf = '-' + ulrMaf;
			refMaf = '-' + refMaf;
			// Insert the left and right boundaries of the corrected segments
			if (beginningCorrectedBase) {
				refMaf = '-' + refMaf;
				ulrMaf = 'X' + ulrMaf;
				clrMaf = 'X' + clrMaf;	
			}
			rowIndex--;
		} else if (isEndingLC) {
			if ( toupper( ulr[urIndex] ) == toupper( clr[cIndex] ) ) {
				if (deletion == currentCost) {
					clrMaf = '-' + clrMaf;
					ulrMaf = ulr[urIndex] + ulrMaf;
					refMaf = ref[urIndex] + refMaf;
					columnIndex--;
				} else if (substitute == currentCost) {
					// Insert the right boundary of a corrected segment
					if (endingCorrectedBase) {
						refMaf = '-' + refMaf;
						ulrMaf = 'X' + ulrMaf;
						clrMaf = 'X' + clrMaf;	
					}
					clrMaf = clr[cIndex] + clrMaf;
					ulrMaf = ulr[urIndex] + ulrMaf;
					refMaf = ref[urIndex] + refMaf;
					// Insert the left boundary of the corrected segment
					if (beginningCorrectedBase) {
						refMaf = '-' + refMaf;
						ulrMaf = 'X' + ulrMaf;
						clrMaf = 'X' + clrMaf;	
					}
					rowIndex--;
					columnIndex--;
				} else {
					std::cout << "ERROR CODE 1: No paths found. Terminating backtracking.\n";
					std::cout << "cIndex is " << cIndex << "\n";
					std::cout << "urIndex is " << urIndex << "\n";
					std::exit(1);
				}
			} else {
				if (deletion == currentCost) {
					clrMaf = '-' + clrMaf;
					ulrMaf = ulr[urIndex] + ulrMaf;
					refMaf = ref[urIndex] + refMaf;
					columnIndex--;
				} else {
					std::cout << "ERROR CODE 2: No paths found. Terminating backtracking.\n";
					std::cout << "cIndex is " << cIndex << "\n";
					std::cout << "urIndex is " << urIndex << "\n";
					std::exit(1);
				}
			}
		} else if (islower(clr[cIndex])) {
			if ( toupper( ulr[urIndex] ) == toupper( clr[cIndex] ) ) {
				if (substitute == currentCost) {
					// Insert the right boundary of the corrected segment
					if (endingCorrectedBase) {
						refMaf = '-' + refMaf;
						ulrMaf = 'X' + ulrMaf;
						clrMaf = 'X' + clrMaf;
					}
					clrMaf = clr[cIndex] + clrMaf;	
					ulrMaf = ulr[urIndex] + ulrMaf;
					refMaf = ref[urIndex] + refMaf;
					// Insert the right boundary of a corrected segment
					if (beginningCorrectedBase) {
						refMaf = '-' + refMaf;
						ulrMaf = 'X' + ulrMaf;
						clrMaf = 'X' + clrMaf;
					}
					rowIndex--;
					columnIndex--;
				} else {
					std::cout << "ERROR CODE 3: No paths found. Terminating backtracking.\n";
					std::cout << "cIndex is " << cIndex << "\n";
					std::cout << "urIndex is " << urIndex << "\n";
					std::exit(1);
				}
			} else if (ulr[urIndex] == '-') {
				deletion = matrix[rowIndex][columnIndex-1];
				if (deletion == currentCost) {
					clrMaf = '-' + clrMaf;
					ulrMaf = ulr[urIndex] + ulrMaf;
					refMaf = ref[urIndex] + refMaf;
					columnIndex--;
				} else {
					std::cout << "ERROR CODE 4: No paths found. Terminating backtracking.\n";
					std::cout << "cIndex is " << cIndex << "\n";
					std::cout << "urIndex is " << urIndex << "\n";
					std::exit(1);
				}
			} else {
				std::cout << "ERROR CODE 5: No paths found. Terminating backtracking.\n";
				std::cout << "cIndex is " << cIndex << "\n";
				std::cout << "urIndex is " << urIndex << "\n";
				std::exit(1);	
			}
		// This condition is performed if the current corrected long read base is uppercase
		} else {
			if (deletion == currentCost) {
				clrMaf = '-' + clrMaf;
				ulrMaf = ulr[urIndex] + ulrMaf;
				refMaf = ref[urIndex] + refMaf;
				columnIndex--;
			} else if (insert == currentCost) {
				// Insert the right boundary of the corrected segment
				if (endingCorrectedBase) {
					refMaf = '-' + refMaf;
					ulrMaf = 'X' + ulrMaf;
					clrMaf = 'X' + clrMaf;
				}
				clrMaf = clr[cIndex] + clrMaf;
				ulrMaf = '-' + ulrMaf;
				refMaf = '-' + refMaf;
				// Insert the left boundary of the corrected segment
				if (beginningCorrectedBase) {
					refMaf = '-' + refMaf;
					ulrMaf = 'X' + ulrMaf;
					clrMaf = 'X' + clrMaf;
				}
				rowIndex--;
			} else if (substitute == currentCost) {
				// Insert the right boundary of the corrected segment
				if (endingCorrectedBase) {
					refMaf = '-' + refMaf;
					ulrMaf = 'X' + ulrMaf;
					clrMaf = 'X' + clrMaf;
				}
				clrMaf = clr[cIndex] + clrMaf;
				ulrMaf = ulr[urIndex] + ulrMaf;
				refMaf = ref[urIndex] + refMaf;
				// Insert the left boundary of the corrected segment
				if (beginningCorrectedBase) {
					refMaf = '-' + refMaf;
					ulrMaf = 'X' + ulrMaf;
					clrMaf = 'X' + clrMaf;
				}
				rowIndex--;
				columnIndex--;
			} else {
				std::cout << "ERROR CODE 6: No paths found. Terminating backtracking.\n";
				std::cout << "cIndex is " << cIndex << "\n";
				std::cout << "urIndex is " << urIndex << "\n";
				std::exit(1);	
			}
		} 		
	}
	// Store the alignments in the UntrimmedAlignment object
	clrAlignment = clrMaf;
	ulrAlignment = ulrMaf;
	refAlignment = refMaf;
}

/* --------------------------------------------------------------------------------------------- */

TrimmedAlignments::TrimmedAlignments() : Alignments() {}

int64_t TrimmedAlignments::columnBaseCase(int64_t columnIndex)
{
	return 0;
}

bool TrimmedAlignments::isLastBase(int64_t cIndex)
/* Returns true if the current index is the index of a last base of a trimmed segment, false otherwise
 */
{
	// Check if cIndex is the first base of a read
	if (std::find( lastBaseIndices.begin(), lastBaseIndices.end(), cIndex ) != lastBaseIndices.end()) {
		return true;
	} else {
		return false;
	} 
} 

bool TrimmedAlignments::isFirstBase(int64_t cIndex)
/* Returns true if current corrected long read base is the first base of trimmed segment, false otherwise
 */
{
	// Check if cIndex is the first base of a read
	if (cIndex == 0 or std::find( lastBaseIndices.begin(), lastBaseIndices.end(), cIndex-1 ) != lastBaseIndices.end()) {
		return true;
	} else {
		return false;
	} 

}

void TrimmedAlignments::preprocessReads()
{
	// Split the clr into its corrected parts
	std::vector< std::string > trimmedClrs = split(clr);

	// Record the indices of the first bases of all the reads
	int64_t lastBaseIndex = -1;
	for (int64_t index = 0; index < trimmedClrs.size(); index++) {
		lastBaseIndex = lastBaseIndex + trimmedClrs.at(index).length();
		lastBaseIndices.push_back(lastBaseIndex);	
	}

	// Remove spaces in clr
	clr.erase(std::remove(clr.begin(), clr.end(), ' '), clr.end());

	rows = clr.length() + 1;
	columns = ref.length() + 1;
}

int64_t TrimmedAlignments::editDistance(int64_t rowIndex, int64_t columnIndex)
/* Constructs the DP matrix for trimmed corrected long reads
 */
{
	int64_t substitute;
	int64_t insert;
	int64_t deletion;
	int64_t cIndex = rowIndex - 1;
	int64_t urIndex = columnIndex - 1;
	bool lastBase = isLastBase(cIndex);

	if (lastBase) {
		deletion = matrix[rowIndex][columnIndex-1];
	} else {
		deletion = matrix[rowIndex][columnIndex-1] + cost(ref[urIndex], '-');
	}	
	insert = matrix[rowIndex-1][columnIndex] + cost('-', clr[cIndex]);
	substitute = matrix[rowIndex-1][columnIndex-1] + cost(clr[cIndex], ref[urIndex]);
	return std::min( deletion, std::min( insert, substitute ) );
}

void TrimmedAlignments::operationCosts(int64_t rowIndex, int64_t columnIndex, int64_t& deletion, int64_t& insert,
                                       int64_t& substitute)
{
	int64_t infinity = std::numeric_limits<int64_t>::max();
	int64_t cIndex = rowIndex - 1;
	int64_t urIndex = columnIndex - 1;
	bool lastBase = isLastBase(cIndex);
	// Set the costs of the different operations, 
	// ensuring we don't go out of bounds of the matrix.
	if (rowIndex > 0 and columnIndex > 0) {
		// if we're at the end of the read, zero cost deletion
		if (lastBase) {
			deletion = matrix[rowIndex][columnIndex-1]; 
		} else {
			deletion = matrix[rowIndex][columnIndex-1] + cost(ref[urIndex], '-');
		}
		insert = matrix[rowIndex-1][columnIndex] + cost('-', clr[cIndex]);
		substitute = matrix[rowIndex-1][columnIndex-1] + cost(ref[urIndex], clr[cIndex]);	
	} else if (rowIndex <= 0 and columnIndex > 0) {
		// if we're at the end of the read, zero cost deletion
		if (lastBase) {
			deletion = matrix[rowIndex][columnIndex-1];
		} else {
			deletion = matrix[rowIndex][columnIndex-1] + cost(ref[urIndex], '-');
		}
		insert = infinity;
		substitute = infinity;
	} else if (rowIndex > 0 and columnIndex <= 0) {
		deletion = infinity;
		insert = matrix[rowIndex-1][columnIndex] + cost('-', clr[cIndex]);
		substitute = infinity;
	}	
}

void TrimmedAlignments::findAlignments()
/* Construct the optimal alignments between the trimmed corrected long reads, 
 * uncorrected long read and reference sequence. These algorithm indicates the boundaries
 * of the original trimmed long reads by placing X's immediately left and right
 * of the trimmed long reads.
 */
{
	std::string clrMaf = "";
	std::string ulrMaf = "";
	std::string refMaf = "";
	int64_t rowIndex = rows - 1;
	int64_t columnIndex = columns - 1;
	int64_t infinity = std::numeric_limits<int64_t>::max();
	// Follow the best path from the bottom right to the top left of the matrix.
	// This is equivalent to the optimal alignment between ulr and clr.
	// The path we follow is restricted to the conditions set when computing the matrix,
	// i.e. we can never follow a path that the edit distance equations do not allow.
	while (rowIndex > 0 or columnIndex > 0) {
		int64_t urIndex = columnIndex - 1;
		int64_t cIndex = rowIndex - 1;
		int64_t currentCost = matrix[rowIndex][columnIndex];

		// Check if cIndex is the last base of a read, if it is then that means
		// we're either at the beginning or the end of a read
		bool lastBase = isLastBase(cIndex);
		bool firstBase = isFirstBase(cIndex);
		int64_t insert;
		int64_t deletion;
		int64_t substitute;
		operationCosts(rowIndex,columnIndex,deletion,insert,substitute);

		if (rowIndex == 0 or currentCost == deletion) {
			refMaf = ref[urIndex] + refMaf;
			ulrMaf = ulr[urIndex] + ulrMaf;
			clrMaf = '-' + clrMaf;

			columnIndex--;
		} else if (columnIndex == 0 or currentCost == insert) {
			// Mark the end of a trimmed long read
			if (lastBase) {
				refMaf = '-' + refMaf;
				ulrMaf = 'X' + ulrMaf;
				clrMaf = 'X' + clrMaf;
			}	

			refMaf = '-' + refMaf;
			ulrMaf = '-' + ulrMaf;
			clrMaf = clr[cIndex] + clrMaf;

			// Mark the beginning of a trimmed long read
			if (firstBase) {
				refMaf = '-' + refMaf;
				ulrMaf = 'X' + ulrMaf;
				clrMaf = 'X' + clrMaf;
			}

			rowIndex--;
		} else if (currentCost == substitute) {
			// Mark the end of a trimmed long read
			if (lastBase) {
				refMaf = '-' + refMaf;
				ulrMaf = 'X' + ulrMaf;
				clrMaf = 'X' + clrMaf;
			}	

			refMaf = ref[urIndex] + refMaf;
			ulrMaf = ulr[urIndex] + ulrMaf;
			clrMaf = clr[cIndex] + clrMaf;

			// Mark the beginning of a trimmed long read
			// We only place this beginning boundary when we're
			// at the very first base of a read
			if (firstBase) {
				refMaf = '-' + refMaf;
				ulrMaf = 'X' + ulrMaf;
				clrMaf = 'X' + clrMaf;
			}

			rowIndex--;
			columnIndex--;
		} else {
			std::cout << "ERROR: No paths found. Terminating backtracking.\n";
			std::cout << "cIndex is " << cIndex << "\n";
			std::cout << "urIndex is " << urIndex << "\n";
			std::exit(1);
		}
	}

	// Store the alignments in the TrimmedAlignment object
	clrAlignment = clrMaf;
	ulrAlignment = ulrMaf;
	refAlignment = refMaf;
}

ExtendedUntrimmedAlignments::ExtendedUntrimmedAlignments() : UntrimmedAlignments() {};

int64_t ExtendedUntrimmedAlignments::rowBaseCase(int64_t rowIndex)
{
	return 0;
}

int64_t ExtendedUntrimmedAlignments::levenshteinDistance(int64_t rowIndex, int64_t columnIndex)
{
	int64_t cIndex = rowIndex - 1;
	int64_t urIndex = columnIndex - 1;
	int64_t deletion = std::abs( matrix[rowIndex][columnIndex-1] + cost(ref[urIndex], '-') );
	int64_t insert;
	if (columnIndex == columns - 1) {
		insert = matrix[rowIndex-1][columnIndex];
	} else {
		insert = std::abs( matrix[rowIndex-1][columnIndex] + cost('-', clr[cIndex]) );
	}
	int64_t substitute = std::abs( matrix[rowIndex-1][columnIndex-1] + cost(ref[urIndex], clr[cIndex]) );
	return std::min( deletion, std::min(insert, substitute) );
}

void ExtendedUntrimmedAlignments::operationCosts(int64_t rowIndex, int64_t columnIndex, int64_t& deletion,
                                                 int64_t& insert, int64_t& substitute)
{
	int64_t infinity = std::numeric_limits<int64_t>::max();
	int64_t cIndex = rowIndex - 1;
	int64_t urIndex = columnIndex - 1;
	// Set the costs of the different operations, 
	// also ensuring we don't go out of bounds of the matrix.
	if (rowIndex > 0 and columnIndex > 0) {
		deletion = std::abs(matrix[rowIndex][columnIndex-1] + cost(ref[urIndex], '-'));
		if (columnIndex == columns - 1) {
			insert = matrix[rowIndex-1][columnIndex];
		} else {
			insert = std::abs(matrix[rowIndex-1][columnIndex] + cost('-', clr[cIndex]));
		}
		substitute = std::abs(matrix[rowIndex-1][columnIndex-1] + cost(ref[urIndex], clr[cIndex]));
	} else if (rowIndex <= 0 and columnIndex > 0) {
		deletion = std::abs(matrix[rowIndex][columnIndex-1] + cost(ref[urIndex], '-'));
		insert = infinity;
		substitute = infinity;
	} else if (rowIndex > 0 and columnIndex <= 0) {
		deletion = infinity;
		if (columnIndex == columns - 1) {
			insert = matrix[rowIndex-1][columnIndex];
		} else {
			insert = std::abs(matrix[rowIndex-1][columnIndex] + cost('-', clr[cIndex]));
		}
		substitute = infinity;
	} 
}

ExtendedTrimmedAlignments::ExtendedTrimmedAlignments() : TrimmedAlignments() {}

int64_t ExtendedTrimmedAlignments::rowBaseCase(int64_t rowIndex)
{
	return rowIndex;
}

int64_t ExtendedTrimmedAlignments::editDistance(int64_t rowIndex, int64_t columnIndex)
{
	int64_t substitute;
	int64_t insert;
	int64_t deletion;
	int64_t cIndex = rowIndex - 1;
	int64_t urIndex = columnIndex - 1;
	bool lastBase = isLastBase(cIndex);

	if (lastBase) {
		deletion = matrix[rowIndex][columnIndex-1];
	} else {
		deletion = matrix[rowIndex][columnIndex-1] + cost(ref[urIndex], '-');
	}	
	if (columnIndex == columns - 1) {
		insert = matrix[rowIndex-1][columnIndex] + 1;
	} else {
		insert = matrix[rowIndex-1][columnIndex] + cost('-', clr[cIndex]);
	}
	substitute = matrix[rowIndex-1][columnIndex-1] + cost(clr[cIndex], ref[urIndex]);
	return std::min( deletion, std::min( insert, substitute ) );
}

void ExtendedTrimmedAlignments::operationCosts(int64_t rowIndex, int64_t columnIndex, int64_t& deletion,
                                                int64_t& insert, int64_t& substitute)
{
	int64_t infinity = std::numeric_limits<int64_t>::max();
	int64_t cIndex = rowIndex - 1;
	int64_t urIndex = columnIndex - 1;
	bool lastBase = isLastBase(cIndex);
	// Set the costs of the different operations, 
	// ensuring we don't go out of bounds of the matrix.
	if (rowIndex > 0 and columnIndex > 0) {
		// if we're at the end of the read, zero cost deletion
		if (lastBase) {
			deletion = matrix[rowIndex][columnIndex-1]; 
		} else {
			deletion = matrix[rowIndex][columnIndex-1] + cost(ref[urIndex], '-');
		}
		insert = matrix[rowIndex-1][columnIndex] + cost('-', clr[cIndex]);
		substitute = matrix[rowIndex-1][columnIndex-1] + cost(ref[urIndex], clr[cIndex]);	
	} else if (rowIndex <= 0 and columnIndex > 0) {
		// if we're at the end of the read, zero cost deletion
		if (lastBase) {
			deletion = matrix[rowIndex][columnIndex-1];
		} else {
			deletion = matrix[rowIndex][columnIndex-1] + cost(ref[urIndex], '-');
		}
		insert = infinity;
		substitute = infinity;
	} else if (rowIndex > 0 and columnIndex <= 0) {
		deletion = infinity;
		insert = matrix[rowIndex-1][columnIndex] + cost('-', clr[cIndex]);
		substitute = infinity;
	}	
}
