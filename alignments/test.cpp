#include <iostream>
#include <string>
#include "alignments.hpp"

int main()
{
	
	
	std::string clr = "gTAACTccCTGGC";
	std::string clrMaf = "gTAA-CTccCTGGC";
	std::string ulrMaf = "G----CTCCCT-GC";
	std::string refMaf = "GTAAAAT--CTGGC";
	
	OptimalAlignment alignments(refMaf, ulrMaf, clr);
	std::string refAlignment = alignments.getRefAlignment();
	std::string cAlignment = alignments.get_cAlignment();
	clrMaf = alignments.getClrMaf();
	ulrMaf = alignments.getUlrMaf();
	refMaf = alignments.getRefMaf();

	std::cout << "clrMaf == " << clrMaf << "\n";
	std::cout << "ulrMaf == " << ulrMaf << "\n";
	std::cout << "refMaf == " << refMaf << "\n";

	clr = "CTaccctgtatgacaTGCGCGAATTAACCGTGCGtgagACGATTAcggtaacc";
	clrMaf = "-CT-accctgtatgacaTGCGCGAATTAACCGTGCGtgagACGATTAcggtaacc";
	ulrMaf = "GCT-ACCCTGTATGACATGCGCGAA-TA-C-G-GCGTGAGA-GATTACGGTAACC";
	refMaf = "-CTGA-CCTGTATGACA-GCGCGAATTAACCGTG-GTGAGACGA-TACCTGAACC";

	OptimalAlignment alignments1(refMaf, ulrMaf, clr);
	refAlignment = alignments1.getRefAlignment();
	cAlignment = alignments1.get_cAlignment();
	clrMaf = alignments1.getClrMaf();
	ulrMaf = alignments1.getUlrMaf();
	refMaf = alignments1.getRefMaf();

	std::cout << "clrMaf == " << clrMaf << "\n";
	std::cout << "ulrMaf == " << ulrMaf << "\n";
	std::cout << "refMaf == " << refMaf << "\n";

	clr = "GAgtccgGGTAGTcggccGTGCTGTCGagaaagaaaaac";
	clrMaf = "-G----Agtccg-G-G-TAGTcggccGT-GC--T-G--T---C-G-agaaagaaaaac";
	ulrMaf = "TGATGGAGTCCGTGCGTTA-TCGGCCGTTG-CGTG-GGTCTTCCGCAGAAAGAAAAAC";
	refMaf = "-G------C--G-G-G-TAGTCGGCGGT-GC--T-G--T---C-G-AGA---AA---C";

	OptimalAlignment alignments2(refMaf, ulrMaf, clr);
	refAlignment = alignments2.getRefAlignment();
	cAlignment = alignments2.get_cAlignment();
	clrMaf = alignments2.getClrMaf();
	ulrMaf = alignments2.getUlrMaf();
	refMaf = alignments2.getRefMaf();

	std::cout << "clrMaf == " << clrMaf << "\n";
	std::cout << "ulrMaf == " << ulrMaf << "\n";
	std::cout << "refMaf == " << refMaf << "\n";

	return 0;

}
