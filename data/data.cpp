#include <iostream>
#include <string>
#include <algorithm>

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

LongReadData::LongReadData(std::string referenceMaf, std::string uLongReadMaf, std::string cLongRead)
{
	refMaf = referenceMaf;
	ulrMaf = uLongReadMaf;
	clr = cLongRead;
	ref = stripMaf(refMaf);
	ulr = stripMaf(ulrMaf);
}

std::string LongReadData::stripMaf(std::string seq)
{
	seq.erase( std::remove(seq.begin(), seq.end(), '-'), seq.end() );
	return seq;
}

std::string LongReadData::getRef()
{
	return ref;
}

std::string LongReadData::getRefMaf()
{
	return refMaf;
} 

std::string LongReadData::getUlr()
{
	return ulr;
}

std::string LongReadData::getUlrMaf()
{
	return ulrMaf;
}

std::string LongReadData::getClr()
{
	return clr;
}
