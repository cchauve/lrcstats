#include <vector>
#include <iostream>
#include <string>
#include <cassert>
#include <cstdint>
#include "measures.hpp"

int main()
{
	std::string clr = "----XTTTTX----XTTTTX-XAAAAX";
	std::string ulr = "AAAA-TTTT-CCCC-GGGG---AAAA-";
	std::string ref = "AAAA-TTTT-CCCC-GGGG---AAAA-";

	std::vector< CorrespondingSegments > segmentList = getTrimmedCorrespondingSegmentsList(clr, ulr, ref);

	for (int i = 0; i < segmentList.size(); i++) {
		std::cout << segmentList.at(i).cReadSegment << " " << segmentList.at(i).uReadSegment << " " << segmentList.at(i).refSegment << "\n";
	}
	
	return 0;
}
