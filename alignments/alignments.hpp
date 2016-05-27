class OptimalAlignment
{
	public:
                OptimalAlignment(std::string refMaf, std::string ulrMaf, std::string cLR);
                ~OptimalAlignment();
                std::string get_uAlignment();
		std::string get_cAlignment();
        private:
                std::string ulr;
                std::string clr;
		std::string ref;
		int rows;
		int columns;
                int** matrix;
		int del;
		int ins;
		int sub;
                std::string uAlignment;
		std::string cAlignment;
		int cost(int uIndex, int cIndex);
		void findAlignments();
};
