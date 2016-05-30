#include <iostream>
#include <string>
#include <sstream>
#include <fstream>
#include <vector>

std::vector<std::string> &split(const std::string &s, char delim, std::vector<std::string> &elems)
{
	std::stringstream ss(s);
	std::string item;
	while (std::getline(ss, item, delim)) {
		if (!item.empty()) {
            	elems.push_back(item);
        	}
    	}
	return elems;
}

std::vector<std::string> split(const std::string &s, char delim)
{
	std::vector<std::string> elems;
	split(s, delim, elems);
	return elems;
}

struct Reads
{
	std::string readName;
	std::string cAlignment;
	std::string uAlignment;
	std::string refAlignment; 
};

class MafFile
{
	public:
		MafFile(std::string fileName);	
		void addReads(Reads reads);
	private:
		std::string filename;
};

MafFile::MafFile(std::string fileName)
{
	filename = fileName;
	ofstream file (filename, ios::out | ios::trunc);
	
	if (file.is_open()) {
		file << "track name=" << filename << "\n";	
		file << "maf version=1\n";
		file.close();
	} else {
		std::cerr << "Unable to create MAF file.\n";
	}
}

void MafFile::addReads(Reads reads)
{
	std::string ref = reads.refAlignment();
	std::string ulr = reads.uAlignment();
	std::string clr = reads.cAlignment();

	std::string refName = "reference"; 
	std::string uName = reads.readName + ".uncorrected";
	std::string cName = reads.readName + ".corrected";

	int refStart = 0;
	int uStart = 0;
	int cStart = 0;
 
	int size = ref.length();

	int refSrcSize = size;
	int uSrcSize = size;
	int cSrcSize = size;

	ifstream file (filename, ios::out | ios::app);

	if (file.is_open())
	{
		file << "a\n";
		file << "s " << refName << " " << refStart << " " << refSize << " + " << refSrcSize << " " << ref << "\n";
		file << "s " << uName << " " << uStart << " " << uSize << " + " << uSrcSize << " " << ulr << "\n";
		file << "s " << cName << " " << cStart << " " << cSize << " + " << cSrcSize << " " << clr << "\n";
		file << "\n";
		file.close();
	} else {
		std::cerr << "Unable to add reads to MAF file\n";
	}
}
