struct cSeg
{
	std::string clr;
	std::string reference;
};

class CorrectedSegments
{
	public:
		CorrectedSegments(std::string cLongRead, std::string uLongReadMaf, std::string referenceMaf);
		std::vector<cSeg> getSegments();
	private:
		std::string clr;
		std::string ulrMaf;
		std::string refMaf;
		std::vector<cSeg> segments;
};
