#include <vector>
#include <string>
#include "catch.hpp"
#include "../data.hpp"

TEST_CASE( "split returns a vector whose size is one more than the number of spaces in the input string", "[split]") {
	std::string testString = "aaaa bbbb cccc";
	int numSpaces = 2;
	std::vector< std::string > tokens = split(testString);
	REQUIRE( tokens.size() == numSpaces + 1 );
}

TEST_CASE("gaplessLength returns an integer whose value is equal to the size of the string minus the number of '-'") {
	std::string testString = "aaaa-bbbb-cccc";
	int numGaps = 2;
	int length = gaplessLength(testString);
	REQUIRE( length == testString.length() - numGaps );	
}
