#ifndef ALIGNMENTS_H
#define ALIGNMENTS_H

#include "data.hpp"

class Alignments
/* Is the parent class of UntrimmedAlignments and TrimmedAlignments - for ease of maintenance. */
{
	public:
		Alignments();
		~Alignments();
		// Returns the ref, uLR and cLR alignments
		Read_t align(std::string reference, std::string uRead, std::string cRead);
	protected:
		std::string clr;
		std::string ulr;
		std::string ref;
		std::string refAlignment;
		std::string ulrAlignment;
		std::string clrAlignment;
                int64_t rows;
                int64_t columns;
                int64_t** matrix;
		// Allocate and delete the dynamic programming matrix in the heap
		void createMatrix();
		void deleteMatrix();
		// Cost function for dynamic programming matrix
                int64_t cost(char refBase, char cBase);
		// Print the matrix - debugging purposes only
		void printMatrix();	
		virtual void preprocessReads();
		virtual int64_t rowBaseCase(int64_t rowIndex);
		virtual int64_t columnBaseCase(int64_t columnIndex);
		virtual int64_t editDistance(int64_t rowIndex, int64_t columnIndex);
		virtual void findAlignments();
};

class UntrimmedAlignments : public Alignments
/* Class that returns the optimal alignments between cLR constructed by non-proovread programs 
 * and reference sequences. Performs a dynamic programming algorithm to find such alignments. */
{
        public:
                UntrimmedAlignments();
	protected:
		// Returns true if the current base is an uncorrected, lower case base that precedes 
		// a corrected, upper case base or the end of the read
		bool checkIfEndingLowerCase(int64_t cIndex);
		// Returns true if the current base in the cLR is the first base of a corrected segment;
		// false otherwise
		bool isBeginningCorrectedIndex(int64_t cIndex);
		// Returns true if the current base in the cLR is the last base of a corrected segment;
		// false otherwise
		bool isEndingCorrectedIndex(int64_t cIndex);
		// Returns the conventional levenshtein distance for alignments, sans the base case
		virtual int64_t levenshteinDistance(int64_t rowIndex, int64_t columnIndex);
		// Fill the dynamic programming matrix
		int64_t editDistance(int64_t rowIndex, int64_t columnIndex) override;
		// Returns the operations costs for insertion, deletion and substitute by reference
		virtual void operationCosts(int64_t rowIndex, int64_t columnIndex,
                                    int64_t& deletion, int64_t& insert, int64_t& substitute);
		// Backtrack through the matrix to find the alignments
                void findAlignments() override;
};

class TrimmedAlignments: public Alignments
/* Processes and returns the optimal alignment between trimmed cLRs and the reference sequence. */
{
	public:
		TrimmedAlignments();
	protected:
		int64_t columnBaseCase(int64_t columnIndex) override;
		std::vector<int64_t> lastBaseIndices;
		bool isLastBase(int64_t cIndex);
		bool isFirstBase(int64_t cIndex);
		void preprocessReads() override;
		virtual int64_t editDistance(int64_t rowIndex, int64_t columnIndex) override;
		// Returns the operations costs for insertion, deletion and substitute by reference
		virtual void operationCosts(int64_t rowIndex, int64_t columnIndex,
                                    int64_t& deletion, int64_t& insert, int64_t& substitute);
                void findAlignments() override;
};

class ExtendedUntrimmedAlignments : public UntrimmedAlignments
{
	public:
		ExtendedUntrimmedAlignments();
	protected: 
		int64_t rowBaseCase(int64_t rowIndex) override;
		// modified levenshtein distance to allow for zero cost insertions at the end of reads
		int64_t levenshteinDistance(int64_t rowIndex, int64_t columnIndex) override;
		void operationCosts(int64_t rowIndex, int64_t columnIndex,
                                    int64_t& deletion, int64_t& insert, int64_t& substitute) override;
};

class ExtendedTrimmedAlignments : public TrimmedAlignments
{
	public:
		ExtendedTrimmedAlignments();
	protected:
		int64_t rowBaseCase(int64_t rowIndex) override;
		int64_t editDistance(int64_t rowIndex, int64_t columnIndex) override;
		void operationCosts(int64_t rowIndex, int64_t columnIndex,
                                    int64_t& deletion, int64_t& insert, int64_t& substitute) override;
};

#endif // ALIGNMENTS_H
