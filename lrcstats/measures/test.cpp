#include <vector>
#include <iostream>
#include <string>
#include <cassert>
#include <cstdint>
#include "measures.hpp"

int main()
{
	std::string ref = "AAA-AT-TTTCCCCGGGG";
	std::string ulr = "ATTAATAAATCGGCGCCG";
	std::string clr = "aAA-at-TTtcCCcgGGg";

	std::vector< CorrespondingSegments > segmentList = getCorrespondingSegmentsList(clr, ulr, ref);

	for (int i = 0; i < segmentList.size(); i++) {
		std::cout << segmentList.at(i).cReadSegment << " " << segmentList.at(i).uReadSegment << " " << segmentList.at(i).refSegment << "\n";
	}
	
	return 0;
}
