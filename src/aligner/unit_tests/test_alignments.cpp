#include <iostream>
#include <algorithm> // for std::count
#include <string>
#include "catch.hpp"
#include "../alignments.hpp"
#include "../data.hpp"

TEST_CASE( "ref, uLR and cLR alignments are the same length", "[alignments]" ) {
	SECTION( "UntrimmedAlignments are the same length" ) {
		std::string ref = "C-GAGTCAATAAAAA";
		std::string ulr = "CTG-GTC--TAAG-A";
		std::string clr = "ctggTCAATaaga"; 
		UntrimmedAlignments alignments;
		Read_t alignedReads = alignments.align(ref,ulr,clr);
		ref = alignedReads.ref;
		ulr = alignedReads.ulr;
		clr = alignedReads.clr;

		std::cout << ref << std::endl;
		std::cout << ulr << std::endl;
		std::cout << clr << std::endl;

		REQUIRE( ref.length() == ulr.length() );
		REQUIRE( ulr.length() == clr.length() );
	}
	SECTION( "TrimmedAlignments are the same length" ) {
		std::string ref = "C-GAGTCAATAAAAA";
		std::string ulr = "CTG-GTC--TAAG-A";
		std::string clr = "TCAAT"; 

		TrimmedAlignments alignments;
		Read_t alignedReads = alignments.align(ref,ulr,clr);
		ref = alignedReads.ref;
		ulr = alignedReads.ulr;
		clr = alignedReads.clr;

		std::cout << ref << std::endl;
		std::cout << ulr << std::endl;
		std::cout << clr << std::endl;

		REQUIRE( ref.length() == ulr.length() );
		REQUIRE( ulr.length() == clr.length() );
	}
}

TEST_CASE( "Alignments output (-,X,X) delimiters to indicate the boundaries of corrected/trimmed segments",
           "[alignments]" ) 
{
	SECTION("An even number of delimiters are outputted when a segment of the cLR aligns outside of the uLR and ref") {
		std::string ref = "AAAAA";
		std::string ulr = "AAAAA";
		std::string clr = "TCCCTaaaaa"; 
		UntrimmedAlignments alignments;
		Read_t alignedReads = alignments.align(ref,ulr,clr);
		ref = alignedReads.ref;
		ulr = alignedReads.ulr;
		clr = alignedReads.clr;
		size_t refCount = std::count(ref.begin(), ref.end(), 'X');
		size_t ulrCount = std::count(ulr.begin(), ulr.end(), 'X');
		size_t clrCount = std::count(clr.begin(), clr.end(), 'X');

		std::cout << ref << std::endl;
		std::cout << ulr << std::endl;
		std::cout << clr << std::endl;


		SECTION( "uLR and cLR alignments contain an even number of X delimiters" ) {
			REQUIRE( ulrCount % 2 == 0 );
			REQUIRE( clrCount % 2 == 0 );
		}	

		SECTION( "uLR and cLR alignments contain the same number of X delimiters" ) {
			REQUIRE( ulrCount == clrCount );
		}

		SECTION( "the number of X delimiters in the ref alignment is 0" ) {
			REQUIRE( refCount == 0 );
		}
	}
	SECTION( "UntrimmedAlignments output (-,X,X) delimiters to indicate the boundaries of corrected segments" ) {
		std::string ref = "CGAGTCAATAAAAA";
		std::string ulr = "CGAGTCAATAAAAA";
		std::string clr = "cgagTCAATaaaaa"; 
		UntrimmedAlignments alignments;
		Read_t alignedReads = alignments.align(ref,ulr,clr);
		ref = alignedReads.ref;
		ulr = alignedReads.ulr;
		clr = alignedReads.clr;

		std::cout << ref << std::endl;
		std::cout << ulr << std::endl;
		std::cout << clr << std::endl;

		size_t refCount = std::count(ref.begin(), ref.end(), 'X');
		size_t ulrCount = std::count(ulr.begin(), ulr.end(), 'X');
		size_t clrCount = std::count(clr.begin(), clr.end(), 'X');
		
		SECTION( "uLR and cLR alignments contain an even number of X delimiters" ) {
			REQUIRE( ulrCount % 2 == 0 );
			REQUIRE( clrCount % 2 == 0 );
		}	

		SECTION( "uLR and cLR alignments contain the same number of X delimiters" ) {
			REQUIRE( ulrCount == clrCount );
		}

		SECTION( "the number of X delimiters in the ref alignment is 0" ) {
			REQUIRE( refCount == 0 );
		}
	}

	SECTION( "TrimmedAlignments output (-,X,X) delimiters to indicate the boundaries of trimmed segments" ) {
		std::string ref = "CGAGTCAATAAAAA";
		std::string ulr = "CGAGTCAATAAAAA";
		std::string clr = "CGAGT CAAT AAAAA";

		TrimmedAlignments alignments;
		Read_t alignedReads = alignments.align(ref,ulr,clr);
		ref = alignedReads.ref;
		ulr = alignedReads.ulr;
		clr = alignedReads.clr;

		size_t refCount = std::count(ref.begin(), ref.end(), 'X');
		size_t ulrCount = std::count(ulr.begin(), ulr.end(), 'X');
		size_t clrCount = std::count(clr.begin(), clr.end(), 'X');

		std::cout << ref << std::endl;
		std::cout << ulr << std::endl;
		std::cout << clr << std::endl;
		
		SECTION( "uLR and cLR alignments contain an even number of X delimiters" ) {
			REQUIRE( ulrCount % 2 == 0 );
			REQUIRE( clrCount % 2 == 0 );
		}	

		SECTION( "uLR and cLR alignments contain the same number of X delimiters" ) {
			REQUIRE( ulrCount == clrCount );
		}

		SECTION( "the number of X delimiters in the ref alignment is 0" ) {
			REQUIRE( refCount == 0 );
		}
	}
}

TEST_CASE( "ExtendedUntrimmedAlignments" )
{
	std::string ref = "C-GAGTCAATAAAAA";
	std::string ulr = "CTG-GTC--TAAG-A";
	std::string clr = "ACTACtggTCAATaagATAC"; 
	ExtendedUntrimmedAlignments alignment;
	Read_t alignedReads = alignment.align(ref,ulr,clr);
	ref = alignedReads.ref;
	ulr = alignedReads.ulr;
	clr = alignedReads.clr;

	size_t refCount = std::count(ref.begin(), ref.end(), 'X');
	size_t ulrCount = std::count(ulr.begin(), ulr.end(), 'X');
	size_t clrCount = std::count(clr.begin(), clr.end(), 'X');

	std::cout << ref << std::endl;
	std::cout << ulr << std::endl;
	std::cout << clr << std::endl;
	SECTION( "uLR and cLR alignments contain an even number of X delimiters" ) {
		REQUIRE( ulrCount % 2 == 0 );
		REQUIRE( clrCount % 2 == 0 );
	}	

	SECTION( "uLR and cLR alignments contain the same number of X delimiters" ) {
		REQUIRE( ulrCount == clrCount );
	}

	SECTION( "the number of X delimiters in the ref alignment is 0" ) {
		REQUIRE( refCount == 0 );
	}

}

TEST_CASE( "ExtendedUntrimmedAlignments on real colormap read" )
{
	std::string ref = "TA-CCAG---TATAT-GCAACAAA--TGCC-CG-TCGGCAGCAGCTTTACAATG--A--C-CATCAATGCCTGC-CAGACCTCTGTGA-ACTATGACGCCAGCAGCGGCGCACGCTGTAAGGATCAGGCC-TCC--GGC-AACTGGTATGTTCGCAACGTCACCCATA-C-GA-AA-G-CAGC-AAATC-T-ACGGTTG-ATA--AA-TACCC-ACTCGC-TG-G--CGGAAGT-AT-TTATCAACAGCGAC-GGAGTACCG-ACTCTGGGCGAAGGGA-ACGCCGACTG-C-CG-GACGCAAACCA-TCGGCAGCCGT-TCA-GGA-TTAAGTTGTAA-GATGG-TTAACT-ATAC-CCT-GCAAACAAACGGACTCAGCAACA-CC-TCA-ATCCATATATTCCCGGCGAT-CGC-CAA-CTCGTCGTTAGCC-T-CGGC-CGTC-GG-G-GCGTAC--GAT-ATGCAG-TTCA-GTCTGAATGGCAGTTCA-T-GGAAACCGGTGAG-CAATACC-GCCTATTACTACACCTTCAACGAGATGA-AG-AGCGCAGACTC--GATCTATGTTTTCTTCTCGAGCAACTTCTTTAA-GC-AG-A-TG--GTGAA--CC--TCGG--GATCAGCGAT--ATCAACACCAA-";
	std::string ulr = "TAGCCAGGAGTATATGGCAACAAACCTG-CACGTTCGGCAGCAGCTTTACAATGAGAATCCC-TCAATGC-TGCTCAGACCTCTGTGAGACTATGACGCCAGCAGCGG-GCACGCTG-AAGGATCAGGCCAGCCATGGCGAACTGGTGTGTTCGCAA-GTCACCCATAAATGATA-AGTCAGCCAAATCTTCACGGTTGCATACTAAC-ACCCCACTCGCGT-CGAACG-AAG-TATTTTATCAACAGCGACCGGAGTACCGAACTCTGGGCGAAGGGAAACGCCGACTGGCGAGGGACGCAAACCAATCGGCAGCCGTGT--TGGAACTAAGTTGTAAAGATGGA-TAACTTATA-CC-TCGCA-ACAAACGGACTCAGCAACAGCCGTCACATCCATA-ATTCC-GGCGATTCGCC-AAACTCGTCGTTAGCCATACGGCGCGTCAGGAGAGCGTACGCGATAATGCAGCT-CACGTCTGAATGGCAGTTCACTTGGAA-CC-GTGAGACAATACCTGCCTAT-ACTACACCTTCAACGAGA-GAAAGTAGC-CAGACTCCGGATCTAT-T-TTCTTCTCGAGCAACTTCTT-AAGGCTAGTAGTGGAGTGAAGACCAATCG-AGTATCAGCGATTGATCAACACCAAG";
	std::string clr = "GATGCACGGCATGTTGTCAGACGCGTTTTACCAGTATATGCAACAAATGCCCGTCGGCAGCAGCTTTACAATGACCATCAATGCCTGCCAGACCTCTGTGAACTATGACGCCAGCAGCGGCGCACGCTGTAAGGATCAGGCCTCCGGCAACTGGTATGTTCGCAACGTCACCCATACGAAAGCAGCAAATCTACGGTTGATAAAAACCCACTCGCTGGCGGAAGTATTTATCAACAGCGACGGAGTACCGACTCTGGGCGAAGGGAACGCCGACTGCCGGACGCAAACCATCGGCAGCCGTTCAGGATTAAGTTGTAAGATGGTTAACTATACCCTGCAAACAAACGGACTCAGCAACACCTCAATCCATATATTCCCGGCGATCGCCAACTCGTCGTTAGCCTCGGCCGTCGGGGCGTACCATATGCAGTTCAGTCTGAATGGCAGTTCATGGAAACCGGTGAGCAATACCGCCTATTACTACACCTTCAACGAGATGAAGAGCGCAGACTCGATCTATGTTTTCTTCTCGAGCAACTTCTTTAAGCAGATGGTGAACCTCGGGATCAGCGATATCAACACCAAAGATCT";

	ExtendedUntrimmedAlignments alignment;
	Read_t alignedReads = alignment.align(ref,ulr,clr);
	ref = alignedReads.ref;
	ulr = alignedReads.ulr;
	clr = alignedReads.clr;

	size_t refCount = std::count(ref.begin(), ref.end(), 'X');
	size_t ulrCount = std::count(ulr.begin(), ulr.end(), 'X');
	size_t clrCount = std::count(clr.begin(), clr.end(), 'X');

	std::cout << ref << std::endl;
	std::cout << ulr << std::endl;
	std::cout << clr << std::endl;
	SECTION( "uLR and cLR alignments contain an even number of X delimiters" ) {
		REQUIRE( ulrCount % 2 == 0 );
		REQUIRE( clrCount % 2 == 0 );
	}	

	SECTION( "uLR and cLR alignments contain the same number of X delimiters" ) {
		REQUIRE( ulrCount == clrCount );
	}

	SECTION( "the number of X delimiters in the ref alignment is 0" ) {
		REQUIRE( refCount == 0 );
	}
}
