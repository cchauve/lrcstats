#include <iostream>
#include <string>
#include <../alignments/alignments.hpp>
#include <vector>

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

CorrectedSegments::CorrectedSegments(std::string clr, std::string ulr, std::string ulrMaf, std::string refMaf)
{
	OptimalAlignment alignments(ulr, clr);
	std::string uAlignment = alignments.get_uAlignment();
	std::string cAlignment = alignments.get_cAlignment();

	int alignLength = uAlignment.length();
	bool cSegZone = false;
	int numIns = 0;
	std::vector<int> beginIndices;
	std::vector<int> endingIndices;
	std::string cseg = "";	

	for (int index = 0; index < alignLength; index++) {
		if  (!cSegZone && (isupper(cAlignment[index]) || cAlignment[index] == '-'))  {
			cSegZone = true;
			beginIndices.push_back(index-numIns);
		} else if ( cSegZone && islower(cAlignment[index])) {
			cSegZone = false;
			endingIndices.push_back(index-numIns);
			cSegs.push_back(cseg);
			cseg = "";
		} 

		if (cSegZone && cAlignment[index] != '-') {
			cseg = cseg + cAlignment[index];
		}
		
		if (uAlignment[index] == '-') {
			numIns++;	
		}
	}

	if (cSegZone) {
		endingIndices.push_back(index-numIns);
		cSegs.push_back(cseg);
	}

	std::string refseg = "";
	bool refSegZone = false;
	int mafLength = refMaf.length();
	int indicesLength = beginIndices.size();
	int baseIndex = 0;
	int vectorIndex = 0;
	int mafIndex = 0;
	int segBegin;
	int segEnd;

	while (vectorIndex < indicesLength && mafIndex < mafLength) {
		
		if (baseIndex == segBegin) {
			refSegZone = true;
		} else if (baseIndex = segEnd) {
			refSegZone = false;
			refSegs.push_back(refseg);
			refseg = "";
			vectorIndex++;
			segBegin = beginIndices.at(vectorIndex);
			segEnd = endingIndice.at(vectorIndex);	
		}

		if (refSegZone && refMaf[mafIndex] != '-') {
			refseg = refseg + refMaf[mafIndex];
		}
		
		mafIndex++;

		if (ulrMaf[mafIndex] != '-') {
			baseIndex++;
		}
	}
}

std::vector< std::string > CorrectedSegments::getRefSegments()
{
	return refSegs;
}

std::vector< std::string > CorrectedSegments::getcSegments()
{
	return cSegs;
}
