#ifndef ALIGNMENTS_H
#define ALIGNMENTS_H

class Alignments
/* Is the parent class of UntrimmedAlignments and TrimmedAlignments - for ease of maintenance. */
{
	public:
		Alignments(std::string reference, std::string uLongRead, std::string cLongRead);
		Alignments(const Alignments &reads);
		~Alignments();
		void reset(std::string reference, std::string uLongRead, std::string cLongRead);
		std::string getClr();
		std::string getUlr();
		std::string getRef();
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
		void printMatrix();	
};

class UntrimmedAlignments : public Alignments
/* Class that returns the optimal alignments between cLR constructed by non-proovread programs 
 * and reference sequences. Performs a dynamic programming algorithm to find such alignments. */
{
        public:
                UntrimmedAlignments(std::string reference, std::string uLongRead, std::string cLongRead);
		// In case of need to reassign values to object, reset
		void reset(std::string reference, std::string uLongRead, std::string cLongRead);
	private:
		// Specs for matrix
		bool checkIfEndingLowerCase(int64_t cIndex);
		void initialize();
                void findAlignments();
};

class TrimmedAlignments: public Alignments
/* Processes and returns the optimal alignment between proovread cLRs and the reference sequence. */
{
	public:
		TrimmedAlignments(std::string reference, std::string uLongRead, std::string cLongRead);
		void reset(std::string reference, std::string uLongRead, std::string cLongRead);
	private:
		// The trimmed components of the corrected long reads provided by proovread 
		std::vector<int> lastBaseIndices;
		// These methods are proovread format specific.
		void initialize();
                void findAlignments();
};

#endif // ALIGNMENTS_H
