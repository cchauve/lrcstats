#ifndef ALIGNMENTS_H
#define ALIGNMENTS_H

class Alignments
/* Class that returns the optimal alignments between cLR and reference sequences.
 * Performs a dynamic programming algorithm to find such alignments. */
{
        public:
                Alignments(std::string reference, std::string uLongRead, std::string cLongRead);
		Alignments (const Alignments &alignments);
                ~Alignments();
		// In case of need to reassign values to object, reset
		void reset(std::string reference, std::string uLongRead, std::string cLongRead);
		// More explicity, get reads in MAF-ready format
                std::string getClr();
                std::string getUlr();
                std::string getRef();
		// Get cLR/ref without (-,-)
                std::string get_cAlignment();
                std::string getRefAlignment();
                void printMatrix();
	protected:
		// long reads and ref before processing
                std::string clr;
                std::string ulr;
                std::string ref;
		// Returns long reads and ref in format suitable for MAF file
                std::string clrMaf;
                std::string ulrMaf;
                std::string refMaf;
		// Similar to Maf format, but deletes pairs of the form (-,-)
                std::string cAlignment;
                std::string refAlignment;
		// Specs for matrix
                int rows;
                int columns;
                int** matrix;
                int cost(char refBase, char cBase);
		// Removes pairs of the form (-,-)
                void processAlignments();
		void deleteMatrix();
        private:
		// These methods are format specific - proovread files will need to use
		// the version provided by ProovreadAlignments
		void initialize();
                void findAlignments();
};

class ProovreadAlignments: public Alignments
/* Processes and returns the optimal alignment between proovread cLRs and the reference sequence. */
{
	public:
		ProovreadAlignments(std::string reference, std::string uLongRead, std::vector< std::string > cLongReads);
		void reset(std::string reference, std::string uLongRead, std::vector< std::string > cLongReads);
	private:
		// The trimmed components of the corrected long reads provided by proovread 
		std::vector< std::string > trimmedClrs; 
		// These methods are proovread format specific.
		void initialize();
                void findAlignments();
};

#endif // ALIGNMENTS_H
