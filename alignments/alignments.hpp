class OptimalAlignment
{
        public:
                OptimalAlignment(std::string refMaf, std::string ulrMaf, std::string cLR);
                ~OptimalAlignment();
                std::string get_cAlignment();
		int getDistance();
        private:
                std::string ref;
                std::string ulr;
                std::string clr;
                int rows;
                int columns;
                int** matrix;
                std::string cAlignment;
		int distance;
		void printMatrix();
		int cost(char refBase, char cBase);
                void findAlignments();
};

