#include <iostream>
#include <algorithm> // for std::count
#include <string>
#include "catch.hpp"
#include "../alignments.hpp"

TEST_CASE( "ref, uLR and cLR alignments are the same length", "[alignments]" ) {
	SECTION( "UntrimmedAlignments are the same length" ) {
		std::string ref = "C-GAGTCAATAAAAA";
		std::string ulr = "CTG-GTC--TAAG-A";
		std::string clr = "ctg-gTCAATaag-a"; 
		UntrimmedAlignments alignments(ref, ulr, clr);

		ref = alignments.getRef();
		ulr = alignments.getUlr(); 
		clr = alignments.getClr();

		REQUIRE( ref.length() == ulr.length() );
		REQUIRE( ulr.length() == clr.length() );
	}
	SECTION( "TrimmedAlignments are the same length" ) {
		std::string ref = "C-GAGTCAATAAAAA";
		std::string ulr = "CTG-GTC--TAAG-A";
		std::string clr = "TCAAT"; 
		UntrimmedAlignments alignments(ref, ulr, clr);

		ref = alignments.getRef();
		ulr = alignments.getUlr(); 
		clr = alignments.getClr();

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
		UntrimmedAlignments alignments(ref, ulr, clr);
		ref = alignments.getRef();
		ulr = alignments.getUlr(); 
		clr = alignments.getClr();
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
	SECTION( "UntrimmedAlignments output (-,X,X) delimiters to indicate the boundaries of corrected segments" ) {
		std::string ref = "CGAGTCAATAAAAA";
		std::string ulr = "CGAGTCAATAAAAA";
		std::string clr = "cgagTCAATaaaaa"; 
		UntrimmedAlignments alignments(ref, ulr, clr);

		ref = alignments.getRef();
		ulr = alignments.getUlr(); 
		clr = alignments.getClr();

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

		TrimmedAlignments alignments(ref,ulr,clr);

		ref = alignments.getRef();
		ulr = alignments.getUlr(); 
		clr = alignments.getClr();

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
}
