#include <iostream>
#include <vector>
#include <string>
#include "alignments.hpp"

int main()
{
	std::string clr1 = "cattattTCAGACTTAGGgtgctggagATGTgctttaCGCCGCCattaacccgGCTATCAGGTACAAGtaagA";

	std::string clrMaf = "cattattTCAGACT-TAGGgtgctggag-AT-G-Tgcttta-CGCCGCCattaacccg-GCTATCAGGTACAAG-taag---A";
	std::string ulrMaf = "CATTATTCCAGACCTTAGCGTGCTGGAGTATG-TTGCTTTAT-GCCGCCATTAACCCGGGCTATCAGGTACAAGTTAAG-CTA";
	std::string refMaf = "C-TTA--TCA-ACT-TA-G-TGGTG--G-AT-G-TGCTTTA-CGCCGCCATTAACCCG-GCTATCAGGTACAAG-TAAGG--A";

	GenericAlignments alignments1(refMaf, ulrMaf, clr1);

	std::cout << clrMaf << "\n";
	std::cout << ulrMaf << "\n";
	std::cout << refMaf << "\n\n";

	std::cout << alignments1.getClr() << "\n";
	std::cout << alignments1.getUlr() << "\n";
	std::cout << alignments1.getRef() << "\n\n";

	std::string clr2 = "TCAGACTTAGG ATGT CGCCGCC GCTATCAGGTACAAG";

	ProovreadAlignments alignments2(refMaf, ulrMaf, clr2);

	std::cout << alignments2.getClr() << "\n";
	std::cout << alignments2.getUlr() << "\n";
	std::cout << alignments2.getRef() << "\n\n";

	return 0;
}
