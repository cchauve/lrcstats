#ifndef ALIGNMENTS_H
#define ALIGNMENTS_H

class Alignments
/* Is the parent class of UntrimmedAlignments and TrimmedAlignments - for ease of maintenance. */
{
	public:
		Alignments(std::string reference, std::string uLongRead, std::string cLongRead);
		~Alignments();
		// Returns the ref, uLR and cLR alignments
		std::string getClr();
		std::string getUlr();
		std::string getRef();
	protected:
		std::string clr;
		std::string ulr;
		std::string ref;
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
};

class UntrimmedAlignments : public Alignments
/* Class that returns the optimal alignments between cLR constructed by non-proovread programs 
 * and reference sequences. Performs a dynamic programming algorithm to find such alignments. */
{
        public:
                UntrimmedAlignments(std::string reference, std::string uLongRead, std::string cLongRead);
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
		// Fill the dynamic programming matrix
		void initialize();
		// Backtrack through the matrix to find the alignments
                void findAlignments();
};

class TrimmedAlignments: public Alignments
/* Processes and returns the optimal alignment between trimmed cLRs and the reference sequence. */
{
	public:
		TrimmedAlignments(std::string reference, std::string uLongRead, std::string cLongRead);
	protected:
		std::vector<int64_t> lastBaseIndices;
		bool isLastBase(int64_t cIndex);
		bool isFirstBase(int64_t cIndex);
		void initialize();
                void findAlignments();
};

#endif // ALIGNMENTS_H
