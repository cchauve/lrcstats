#include <iostream>
#include <string>
#include <algorithm>

int editScore(std::string ref, std::string uLR)
{
/* Since maf files give the true alignment, we can find the true "edit distance"
 * (or edit score, as we call it) without trying to find an approximation. */
	int score = 0;
	int del = 1;
	int ins = 1;
	int sub = 1;
	int length = ref.length();
	char refBase;
	char uBase;

	for (int seqIndex = 0; seqIndex < length; seqIndex++) {
		refBase = ref[seqIndex];
		uBase = uLR[seqIndex];

		if (refBase != uBase) {
			if (refBase == '-') {
				score = score + ins;
			} else if (uBase == '-') {
				score = score + del;
			} else {
				score = score + sub;
			}
		}
	}		
	return score;
}

int editDistance(std::string ref, std::string cLR)
{
/* Usual Levenshtein edit distance function */
	int delCost = 1;
	int insCost = 1;
	int subCost = 1;
	int rows = cLR.length() + 1;
	int columns = ref.length() + 1;
	int cIndex;
	int refIndex;
	int deletion;
	int insertion;
	int substitution;
	int matrix[rows][columns];
	char cBase;
	char refBase;

        for (int rowIndex = 0; rowIndex < rows; rowIndex++) {
                matrix[rowIndex][0] = rowIndex;
        }

        for (int columnIndex = 1; columnIndex < columns; columnIndex++) {
                matrix[0][columnIndex] = columnIndex;
        }

	for (int rowIndex = 1; rowIndex < rows; rowIndex++) {
		for (int columnIndex = 1; columnIndex < columns; columnIndex++) {
			cIndex = rowIndex - 1;
			refIndex = columnIndex - 1;
			cBase = toupper( cLR[cIndex] );
			refBase = toupper( ref[refIndex] );

			if (cBase == refBase) {
				matrix[rowIndex][columnIndex] = matrix[rowIndex-1][columnIndex-1];				
			} else {
				deletion = matrix[rowIndex][columnIndex-1] + delCost;
				insertion = matrix[rowIndex-1][columnIndex] + insCost; 
				substitution = matrix[rowIndex-1][columnIndex-1] + subCost;
				matrix[rowIndex][columnIndex] = std::min( deletion, std::min(insertion, substitution) ); 
			}
		}
	}
	return matrix[rows-1][columns-1];
}








