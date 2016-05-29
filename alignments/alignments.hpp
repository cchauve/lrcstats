class OptimalAlignment
{
        public:
                OptimalAlignment(std::string refMaf, std::string ulrMaf, std::string cLR);
                ~OptimalAlignment();
                std::string get_cAlignment();
		std::string getRefAlignment();
		int getDistance();
        private:
                std::string ref;
                std::string ulr;
                std::string clr;
                int rows;
                int columns;
                int** matrix;
                std::string cAlignment;
		std::string refAlignment;
		int distance;
		void printMatrix();
		int cost(char refBase, char cBase);
                void findAlignments();
		void processAlignments();
};

