class OptimalAlignment
{
        public:
                OptimalAlignment(std::string reference, std::string uLongRead, std::string cLongRead);
                ~OptimalAlignment();
                std::string getClrMaf();
                std::string getUlrMaf();
                std::string getRefMaf();
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
