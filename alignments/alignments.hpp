class OptimalAlignment
{
        public:
                OptimalAlignment(std::string refMaf, std::string ulrMaf, std::string cLR);
                ~OptimalAlignment();
                std::string get_cAlignment();
        private:
                std::string ref;
                std::string ulr;
                std::string clr;
                int rows;
                int columns;
                int** matrix;
                std::string cAlignment;
                int cost(int urIndex, int cIndex);
                void findAlignments();
};

