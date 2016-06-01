#include <iostream>
#include <string>
#include "alignments.hpp"

int main()
{
	
	
	std::string clr = "";
	std::string clrMaf = "";
	std::string ulrMaf = "";
	std::string refMaf = "";
	
	Alignments alignments(refMaf, ulrMaf, clr);
	std::string refAlignment = alignments.getRefAlignment();
	std::string cAlignment = alignments.get_cAlignment();
	clrMaf = alignments.getClr();
	ulrMaf = alignments.getUlr();
	refMaf = alignments.getRef();

	std::cout << "clrMaf == " << clrMaf << "\n";
	std::cout << "ulrMaf == " << ulrMaf << "\n";
	std::cout << "refMaf == " << refMaf << "\n";

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
	std::cout << "refMaf == " << refMaf << "\n";

	clr = "";
	clrMaf = "";
	ulrMaf = "";
	refMaf = "";

	alignments.reset(refMaf, ulrMaf, clr);
	refAlignment = alignments.getRefAlignment();
	cAlignment = alignments.get_cAlignment();

	clrMaf = alignments.getClr();
	ulrMaf = alignments.getUlr();
	refMaf = alignments.getRef();

	std::cout << "clrMaf == " << clrMaf << "\n";
	std::cout << "ulrMaf == " << ulrMaf << "\n";
	std::cout << "refMaf == " << refMaf << "\n";

	return 0;

}
