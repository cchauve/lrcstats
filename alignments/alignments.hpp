class Alignments
{
        public:
                Alignments(std::string reference, std::string uLongRead, std::string cLongRead);
                ~Alignments();
		Alignments(const Alignments& alignments);
                std::string getClr();
                std::string getUlr();
                std::string getRef();
                std::string get_cAlignment();
                std::string getRefAlignment();
                int getDistance();
        private:
                std::string clr;
                std::string ulr;
                std::string ref;
                std::string clrMaf;
                std::string ulrMaf;
                std::string refMaf;
                std::string cAlignment;
                std::string refAlignment;
                int rows;
                int columns;
                int** matrix;
                int distance;
                void printMatrix();
                int cost(char refBase, char cBase);
                void findAlignments();
                void processAlignments();
};
