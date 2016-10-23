#include <vector>
#include <string>
#include "catch.hpp"
#include "../measures.hpp"

TEST_CASE( "getCorrespondingSegmentsList returns a vector of the corresponding segments of an alignment",
           "[correspondingSegments]" ) {
	std::string ref = "AAAAAAAA-T-TTTTTTTT-GGGGGGGG-CCCCCCCC-";
	std::string ulr = "AAAAAAAAX-TTTTTTTTTXGGGGGGGGXCCCCCCCCX";
	std::string clr = "AAAAAAAAXTTTTTTTTTTXGGGGGGGGXCCCCCCCCX";
	
	CorrespondingSegments trueSegment1;
	trueSegment1.refSegment   = "T-TTTTTTTT";
	trueSegment1.uReadSegment = "-TTTTTTTTT";
	trueSegment1.cReadSegment = "TTTTTTTTTT";

	CorrespondingSegments trueSegment2;
	trueSegment2.refSegment   = "CCCCCCCC";
	trueSegment2.uReadSegment = "CCCCCCCC";
	trueSegment2.cReadSegment = "CCCCCCCC";

	std::vector< CorrespondingSegments > trueSegments;
	trueSegments.push_back(trueSegment1);
	trueSegments.push_back(trueSegment2);

	std::vector< CorrespondingSegments > segments = getCorrespondingSegmentsList(clr,ulr,ref);

	SECTION( "returns the correct number of segments" ) {
		REQUIRE( segments.size() == trueSegments.size() );
	}	
	SECTION( "each string in each correponding segment has the same length" ) {
		for (int i = 0; i < segments.size(); i++) {
			int refLength = segments.at(i).refSegment.length();
			int ulrLength = segments.at(i).uReadSegment.length();
			int clrLength = segments.at(i).cReadSegment.length();
			REQUIRE( refLength == ulrLength );
			REQUIRE( ulrLength == clrLength );
		}
	} 
	SECTION( "the corresponding segments are correct" ) {
		for (int i = 0; i < segments.size(); i++) {
			REQUIRE( segments.at(i).cReadSegment == trueSegments.at(i).cReadSegment );
			REQUIRE( segments.at(i).uReadSegment == trueSegments.at(i).uReadSegment );
			REQUIRE( segments.at(i).refSegment == trueSegments.at(i).refSegment );
		}
	}
}

TEST_CASE( "get[Insertions/Deletion/Substitutions] returns the correct number of [Insertions/Deletions/Substitutions]" ){
	SECTION( "getInsertions returns the correct number of insertions" ) {
		SECTION( "getInsertions ignores pairs of (-,X)" ) {
			std::string ref = "-";
			std::string read = "X";
			REQUIRE( getInsertions(ref,read) == 0 );
		}
		std::string ref  = "-AAAAAAA-AAAAAA-AAAAAAAAAA-";
		std::string read = "TAAAAAAATAAAAAATAAAAAAAAAAT";
		int insertions = 4;
		REQUIRE( getInsertions(ref,read) == insertions ); 
	}
	SECTION( "getDeletions returns the correct number of deletions" ) {
		std::string ref  = "AAAAAAAAAAAAAAAAAAAAAAAAAAA";
		std::string read = "-AAAAAAA-AAAAAA-AAAAAAAAAA-";
		int deletions = 4;
		REQUIRE( getDeletions(ref,read) == deletions );
	}
	SECTION( "getSubstitutions returns the correct number of substitutions" ) {
		SECTION( "getSubstitutions ignores case of bases" ) {
			std::string ref = "A";
			std::string read = "a";
			REQUIRE( getSubstitutions(ref,read) == 0 );
		}
		std::string ref  = "AAAAAAAAAAAAAAAAAAAAAA";
		std::string read = "TAAAAaAAAATAAaAAATAAAT";
		int substitutions = 4;
		REQUIRE( getSubstitutions(ref,read) == substitutions );
	}
}

TEST_CASE( "get[Insertion/Deletion/Substitution]Proportion returns the correct [insertion/deletion/substitution] proportion") {
	SECTION( "getInsertionProportion returns the correct insertion proportion" ) {
		std::string ref = "-A-A-AA";
		std::string ulr = "TATA-AA";
		std::string clr = "-ATAGAA";

		InsertionProportion trueProp;
		trueProp.cRead = 2;
		trueProp.uRead = 2;

		CorrespondingSegments segments;
		segments.refSegment = ref;
		segments.uReadSegment = ulr;
		segments.cReadSegment = clr;

		InsertionProportion prop = getInsertionProportion(segments);	

		REQUIRE( prop.cRead == trueProp.cRead );
		REQUIRE( prop.uRead == trueProp.uRead );
	}
	SECTION( "getDeletionProportion returns the correct deletion proportion" ) {
		std::string ref = "AAAAAAA";
		std::string ulr = "A-AA-AA";
		std::string clr = "AA--AAA";

		DeletionProportion trueProp;
		trueProp.cRead = 2;
		trueProp.uRead = 2;

		CorrespondingSegments segments;
		segments.refSegment = ref;
		segments.uReadSegment = ulr;
		segments.cReadSegment = clr;

		DeletionProportion prop = getDeletionProportion(segments);	

		REQUIRE( prop.cRead == trueProp.cRead );
		REQUIRE( prop.uRead == trueProp.uRead );
	}
	SECTION( "getSubstitutionProportion returns the correct substitution proportion" ) {
		std::string ref = "AAAAAAA";
		std::string ulr = "ATAATAA";
		std::string clr = "AATTAAA";

		SubstitutionProportion trueProp;
		trueProp.cRead = 2;
		trueProp.uRead = 2;

		CorrespondingSegments segments;
		segments.refSegment = ref;
		segments.uReadSegment = ulr;
		segments.cReadSegment = clr;

		SubstitutionProportion prop = getSubstitutionProportion(segments);	

		REQUIRE( prop.cRead == trueProp.cRead );
		REQUIRE( prop.uRead == trueProp.uRead );
	}
}
