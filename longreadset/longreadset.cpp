#include <iostream>
#include <string>
#include <algorithm>
#include <vector>
#include <sstream>

class LongReadSet
{
	public:
		LongReadSet(std::string referenceMaf, std::string uLongReadMaf, std::string cLongRead);
		std::string getRef();
		std::string getUlr();
		std::string getClr();
	private:
		std::string refMaf;
		std::string ulrMaf;
		std::string clr;	
};

LongReadSet::LongReadSet(std::string referenceMaf, std::string uLongReadMaf, std::string cLongRead)
{
	refMaf = referenceMaf;
	ulrMaf = uLongReadMaf;
	clr = cLongRead;
}

std::string LongReadSet::getRef()
{
	return refMaf;
}

std::string LongReadSet::getUlr()
{
	return ulrMaf;
}

std::string LongReadSet::getClr()
{
	return clr;
}
