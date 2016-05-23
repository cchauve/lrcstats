class OptimalAlignment
{
	public:
                OptimalAlignment(std::string uncorrectedLongRead, std::string correctedLongRead);
                ~OptimalAlignment();
                std::string get_uAlignment();
		std::string get_cAlignment();
                int getDistance();
		void printMatrix();
        private:
                std::string uLR;
                std::string cLR;
		int rows;
		int columns;
                int** matrix;
		int del;
		int ins;
		int sub;
                int distance;
                std::string uAlignment;
		std::string cAlignment;
                int findDistance(int cIndex, int uIndex);
		void findAlignments();
};
