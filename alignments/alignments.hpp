class OptimalAlignment
{
	public:
                OptimalAlignment(std::string uncorrectedLongRead, std::string correctedLongRead);
                ~OptimalAlignment();
                std::string get_uAlignment();
		std::string get_cAlignment();
        private:
                std::string uLR;
                std::string cLR;
		int rows;
		int columns;
                int** matrix;
		int del;
		int ins;
		int sub;
                std::string uAlignment;
		std::string cAlignment;
		int costSub(int uIndex, int cIndex);
		void findAlignments();
};
