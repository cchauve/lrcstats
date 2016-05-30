#include <string>
#include <sstream>
#include <ifstream>
#include <vector>

std::vector<std::string> &split(const std::string &s, char delim, std::vector<std::string> &elems) {
	std::stringstream ss(s);
	std::string item;
	while (std::getline(ss, item, delim)) {
		if (!item.empty()) {
            	elems.push_back(item);
        	}
    	}
	return elems;
}

std::vector<std::string> split(const std::string &s, char delim) {
	std::vector<std::string> elems;
	split(s, delim, elems);
	return elems;
}

std::vector<std::string> readMaf(std::string mafFileName) {
	std::vector<std::string> reads;
	std::string line;
	std::ifstream mafFile;
	mafFile.open(mafFilename, ios::in);
	
	if (mafFile.is_open()) {
		
	}	
}
