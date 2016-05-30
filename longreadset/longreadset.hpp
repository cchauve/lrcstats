class LongReadData
{
        public:
                LongReadData(std::string referenceMaf, std::string uLongReadMaf, std::string cLongRead);
                std::string getRef();
                std::string getRefMaf();
                std::string getUlr();
                std::string getUlrMaf();
                std::string getClr();
        private:
                std::string ref;
                std::string refMaf;
                std::string ulr;
                std::string ulrMaf;
                std::string clr;        
                std::string stripMaf(std::string seq);
};


