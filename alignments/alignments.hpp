#ifndef ALIGNMENTS_H
#define ALIGNMENTS_H

class Alignments
{
        public:
                Alignments(std::string reference, std::string uLongRead, std::string cLongRead);
		Alignments (const Alignments &alignments);
                ~Alignments();
                std::string getClr();
                std::string getUlr();
                std::string getRef();
                std::string get_cAlignment();
                std::string getRefAlignment();
        private:
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
		// Holds matrix
                int** matrix;
		// Member functions
                void printMatrix();
                int cost(char refBase, char cBase);
                void findAlignments();
                void processAlignments();
};

#endif // ALIGNMENTS_H
