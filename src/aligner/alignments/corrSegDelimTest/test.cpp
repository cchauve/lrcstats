#include <string>
#include <iostream>
#include <vector>
#include "alignments.hpp"

int main()
{
	std::cout << "Test Case 1\n";

	std::string realRefMaf = "AAAAA-TTTT-T-AAAAA";
	std::string realUlrMaf = "AAAA--TCT-CT-AA-AA";
	std::string realClrMaf = "aaaa-XTCTT-TXaa-aa";

	std::string ref = "AAAAATTTT-TAAAAA";
	std::string ulr = "AAAA-TCT-CTAA-AA";
	std::string clr = "aaaaTCTTTaaaa";

	UntrimmedAlignments alignments(ref,ulr,clr);

	std::string obsRefMaf = alignments.getRef();
	std::string obsUlrMaf = alignments.getUlr();
	std::string obsClrMaf = alignments.getClr();

	std::cout << "Actual alignment:\n";
	std::cout << realRefMaf << std::endl;
	std::cout << realUlrMaf << std::endl;
	std::cout << realClrMaf << std::endl;
	
	std::cout << "Observed alignment:\n";
	std::cout << obsRefMaf << std::endl;
	std::cout << obsUlrMaf << std::endl;
	std::cout << obsClrMaf << std::endl;

	std::cout << std::endl << "Test Case 2\n";

	realRefMaf = "-AAAAATTTT-T-AAAAA";
	realUlrMaf = "-AAAAATCT-CT-AAAAA";
	realClrMaf = "XAAAAATCTT-TXaaaaa";

	ref = "AAAAATTTT-TAAAAA";
	ulr = "AAAAATCT-CTAAAAA";
	clr = "AAAAATCTTTaaaaa";

	UntrimmedAlignments alignments2(ref,ulr,clr);

	obsRefMaf = alignments2.getRef();
	obsUlrMaf = alignments2.getUlr();
	obsClrMaf = alignments2.getClr();

	std::cout << "Actual alignment:\n";
	std::cout << realRefMaf << std::endl;
	std::cout << realUlrMaf << std::endl;
	std::cout << realClrMaf << std::endl;
	
	std::cout << "Observed alignment:\n";
	std::cout << obsRefMaf << std::endl;
	std::cout << obsUlrMaf << std::endl;
	std::cout << obsClrMaf << std::endl;

	std::cout << std::endl << "Test Case 3\n";

	realRefMaf = "AAAAA-TTTT-TAAAAA-";
	realUlrMaf = "AAAA--TCT-CT-AAAA-";
	realClrMaf = "aaaa-XTCTT-TAAAAAX";

	ref = "AAAAATTTT-TAAAAA";
	ulr = "AAAA-TCT-CT-AAAA";
	clr = "aaaaTCTTTAAAAA";

	UntrimmedAlignments alignments3(ref,ulr,clr);

	obsRefMaf = alignments3.getRef();
	obsUlrMaf = alignments3.getUlr();
	obsClrMaf = alignments3.getClr();

	std::cout << "Actual alignment:\n";
	std::cout << realRefMaf << std::endl;
	std::cout << realUlrMaf << std::endl;
	std::cout << realClrMaf << std::endl;
	
	std::cout << "Observed alignment:\n";
	std::cout << obsRefMaf << std::endl;
	std::cout << obsUlrMaf << std::endl;
	std::cout << obsClrMaf << std::endl;

	std::cout << std::endl << "Test Case 4\n";

	realRefMaf = "-AAAAATTTT-TAAAAA-";
	realUlrMaf = "-AAAA-TCT-CT-AAAA-";
	realClrMaf = "XAAAAATCTT-TAAAAAX";

	ref = "AAAAATTTT-TAAAAA";
	ulr = "AAAA-TCT-CT-AAAA";
	clr = "AAAAATCTTTAAAAA";

	UntrimmedAlignments alignments4(ref,ulr,clr);

	obsRefMaf = alignments4.getRef();
	obsUlrMaf = alignments4.getUlr();
	obsClrMaf = alignments4.getClr();

	std::cout << "Actual alignment:\n";
	std::cout << realRefMaf << std::endl;
	std::cout << realUlrMaf << std::endl;
	std::cout << realClrMaf << std::endl;
	
	std::cout << "Observed alignment:\n";
	std::cout << obsRefMaf << std::endl;
	std::cout << obsUlrMaf << std::endl;
	std::cout << obsClrMaf << std::endl;

	std::cout << std::endl << "Test Case 5\n";

	realRefMaf = "AAAAA-TTTT-T-GGGGG-TTTT-T-AAAAA";
	realUlrMaf = "AAAA--TCT-CT-GGGGG-TCT-CT-AA-AA";
	realClrMaf = "aaaa-XTCTT-TXgggggXTTTT-TXaa-aa"; 

	ref = "AAAAATTTT-TGGGGGTTTT-TAAAAA";
	ulr = "AAAA-TCT-CTGGGGGTCT-CTAA-AA";
	clr = "aaaaTCTTTgggggTTTTTaaaa"; 

	UntrimmedAlignments alignments5(ref,ulr,clr);

	obsRefMaf = alignments5.getRef();
	obsUlrMaf = alignments5.getUlr();
	obsClrMaf = alignments5.getClr();

	std::cout << "Actual alignment:\n";
	std::cout << realRefMaf << std::endl;
	std::cout << realUlrMaf << std::endl;
	std::cout << realClrMaf << std::endl;
	
	std::cout << "Observed alignment:\n";
	std::cout << obsRefMaf << std::endl;
	std::cout << obsUlrMaf << std::endl;
	std::cout << obsClrMaf << std::endl;

	std::cout << std::endl << "Test Case 6\n";

	realRefMaf = "--------------GGGGGG";
	realUlrMaf = "--------------GGGGGG";
	realClrMaf = "aaXAAXaaXAAXaagggggg";

	ref = "GGGGGG";
	ulr = "GGGGGG";
	clr = "aaAAaaAAaagggggg";

	UntrimmedAlignments alignments6(ref,ulr,clr);

	obsRefMaf = alignments6.getRef();
	obsUlrMaf = alignments6.getUlr();
	obsClrMaf = alignments6.getClr();

	std::cout << "Actual alignment:\n";
	std::cout << realRefMaf << std::endl;
	std::cout << realUlrMaf << std::endl;
	std::cout << realClrMaf << std::endl;
	
	std::cout << "Observed alignment:\n";
	std::cout << obsRefMaf << std::endl;
	std::cout << obsUlrMaf << std::endl;
	std::cout << obsClrMaf << std::endl;

	return 0;
}
