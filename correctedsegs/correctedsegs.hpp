class CorrectedSegments
{
        public:
                CorrectedSegments(std::string clr, std::string ulr, std::string ulrMaf, std::string refMaf);
                std::vector< std::string > getRefSegments();
                std::vector< std::string > getcSegments();
        private:
                std::vector< std::string > refSegs;
                std::vector< std::string > cSegs;
};
