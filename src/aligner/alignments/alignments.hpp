#ifndef ALIGNMENTS_H
#define ALIGNMENTS_H

class Alignments
/* Is the parent class of UntrimmedAlignments and TrimmedAlignments - for ease of maintenance. */
{
	public:
		Alignments(std::string reference, std::string uLongRead, std::string cLongRead);
		Alignments(const Alignments &reads);
		~Alignments();
		std::string getClr();
		std::string getUlr();
		std::string getRef();
		void printMatrix();	
	protected:
		std::string clr;
		std::string ulr;
		std::string ref;
                int64_t rows;
                int64_t columns;
                int** matrix;
		void createMatrix();
		void deleteMatrix();
                int64_t cost(char refBase, char cBase);
		void processAlignments();
};

class UntrimmedAlignments : public Alignments
/* Class that returns the optimal alignments between cLR constructed by non-proovread programs 
 * and reference sequences. Performs a dynamic programming algorithm to find such alignments. */
{
        public:
                UntrimmedAlignments(std::string reference, std::string uLongRead, std::string cLongRead);
	private:
		std::vector< int64_t > correctedBeginningBoundaries;
		std::vector< int64_t > correctedEndingBoundaries;
		bool checkIfBeginningBoundary(int64_t cIndex);
		bool checkIfEndingBoundary(int64_t cIndex);
		// Specs for matrix
		bool checkIfEndingLowerCase(int64_t cIndex);
		void initialize();
                void findAlignments();
};

class TrimmedAlignments: public Alignments
/* Processes and returns the optimal alignment between trimmed cLRs and the reference sequence. */
{
	public:
		TrimmedAlignments(std::string reference, std::string uLongRead, std::string cLongRead);
	private:
		std::vector<int> lastBaseIndices;
		void initialize();
                void findAlignments();
};

#endif // ALIGNMENTS_H
