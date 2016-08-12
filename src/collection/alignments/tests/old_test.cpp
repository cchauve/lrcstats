#include <iostream>
#include <string>
#include "alignments.hpp"

int main()
{
	std::string clr = "CAgtacagTTTTTTcttgGCCCCAGTGGGCTAA";
	std::string clrMaf = "-C-A--gtacag--T-TTT-TT-cttgGCCCC-AGTGGGCTAA";
	std::string ulrMaf = "CCAAGGGTACAGTTTTTTTTTTCCTTGG-CCCAA-TGGGCTAA";
	std::string refMaf = "-C-A--G-AC-G--T-TTT-TT-C-T-GCCCC-AGTGGGCTAA";
	
	Alignments alignments(refMaf, ulrMaf, clr);
	std::string refAlignment = alignments.getRefAlignment();
	std::string cAlignment = alignments.get_cAlignment();
	clrMaf = alignments.getClr();
	ulrMaf = alignments.getUlr();
	refMaf = alignments.getRef();

	std::cout << "clrMaf == " << clrMaf << "\n";
	std::cout << "ulrMaf == " << ulrMaf << "\n";
	std::cout << "refMaf == " << refMaf << "\n\n";

	clr = "CTaccctgtatgacaTGCGCGAATTAACCGTGCGtgagACGATTAcggtaacc";
	clrMaf = "-CT-accctgtatgacaTGCGCGAATTAACCGTGCGtgagACGATTAcggtaacc";
	ulrMaf = "GCT-ACCCTGTATGACATGCGCGAA-TA-C-G-GCGTGAGA-GATTACGGTAACC";
	refMaf = "-CTGA-CCTGTATGACA-GCGCGAATTAACCGTG-GTGAGACGA-TACCTGAACC";

	alignments.reset(refMaf, ulrMaf, clr);
	refAlignment = alignments.getRefAlignment();
	cAlignment = alignments.get_cAlignment();
	clrMaf = alignments.getClr();
	ulrMaf = alignments.getUlr();
	refMaf = alignments.getRef();

	std::cout << "clrMaf == " << clrMaf << "\n";
	std::cout << "ulrMaf == " << ulrMaf << "\n";
	std::cout << "refMaf == " << refMaf << "\n\n";

	clr = "ACGGCCccttggcttGGAAAGgcCTAAtgagaattcgccccAATCCCGTtttgCTGTTGGGaaacactgaa";
	clrMaf = "AC---GGCCccttggcttGG-AAAGgcCTAAtgagaattcgcccc-AAT-CCCGT-tttg-CTGTTG-GGaaacactgaa";
	ulrMaf = "ACCCC-GGCCCTTGGCTTGGAAAAGGCCTAATGAGAATTCGCCCCCAATTCCCGTGTTTGG-TGTTGTGGAAACACTGAA";
	refMaf = "AC---GGCC--T-GGCT-GG-AAAG--CTA-TGA-AATTCGCCTC-AAT-CCCGT-TTTG-CTGTTG-GAAAACAGTGAA";

	alignments.reset(refMaf, ulrMaf, clr);
	refAlignment = alignments.getRefAlignment();
	cAlignment = alignments.get_cAlignment();

	clrMaf = alignments.getClr();
	ulrMaf = alignments.getUlr();
	refMaf = alignments.getRef();

	std::cout << "clrMaf == " << clrMaf << "\n";
	std::cout << "ulrMaf == " << ulrMaf << "\n";
	std::cout << "refMaf == " << refMaf << "\n\n";

	clr = "cattattTCAGACTTAGGgtgctggagATGTgctttaCGCCGCCattaacccgGCTATCAGGTACAAGtaagA";
	clrMaf = "cattattTCAGACT-TAGGgtgctggag-AT-G-Tgcttta-CGCCGCCattaacccg-GCTATCAGGTACAAG-taag---A";
	ulrMaf = "CATTATTCCAGACCTTAGCGTGCTGGAGTATG-TTGCTTTAT-GCCGCCATTAACCCGGGCTATCAGGTACAAGTTAAG-CTA";
	refMaf = "C-TTA--TCA-ACT-TA-G-TGGTG--G-AT-G-TGCTTTA-CGCCGCCATTAACCCG-GCTATCAGGTACAAG-TAAGG--A";

	alignments.reset(refMaf, ulrMaf, clr);
	refAlignment = alignments.getRefAlignment();
	cAlignment = alignments.get_cAlignment();

	clrMaf = alignments.getClr();
	ulrMaf = alignments.getUlr();
	refMaf = alignments.getRef();

	std::cout << "clrMaf == " << clrMaf << "\n";
	std::cout << "ulrMaf == " << ulrMaf << "\n";
	std::cout << "refMaf == " << refMaf << "\n\n";

	return 0;

}
