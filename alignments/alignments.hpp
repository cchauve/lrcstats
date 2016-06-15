#ifndef ALIGNMENTS_H
#define ALIGNMENTS_H

class Reads
{
	public:
		Reads(std::string reference, std::string uLongRead, std::string cLongRead);
		Reads(const Reads &reads);
		~Reads();
		void reset(std::string reference, std::string uLongRead, std::string cLongRead);
		std::string getClr();
		std::string getUlr();
		std::string getRef();
	protected:
		std::string clr;
		std::string ulr;
		std::string ref;
                int rows;
                int columns;
                int** matrix;
		void createMatrix();
		void deleteMatrix();
                int cost(char refBase, char cBase);
		void processAlignments();
};

class GenericAlignments : public Reads
/* Class that returns the optimal alignments between cLR and reference sequences.
 * Performs a dynamic programming algorithm to find such alignments. */
{
        public:
                GenericAlignments(std::string reference, std::string uLongRead, std::string cLongRead);
		// In case of need to reassign values to object, reset
		void reset(std::string reference, std::string uLongRead, std::string cLongRead);
	private:
		// Specs for matrix
		void initialize();
                void findAlignments();
};

class ProovreadAlignments: public Reads
/* Processes and returns the optimal alignment between proovread cLRs and the reference sequence. */
{
	public:
		ProovreadAlignments(std::string reference, std::string uLongRead, std::string cLongRead);
		void reset(std::string reference, std::string uLongRead, std::string cLongRead);
	private:
		// The trimmed components of the corrected long reads provided by proovread 
		std::vector<int> lastBaseIndices;
		// These methods are proovread format specific.
		void initialize();
                void findAlignments();
};

#endif // ALIGNMENTS_H
