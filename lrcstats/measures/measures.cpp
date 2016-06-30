#include <iostream>
#include <string>
#include <cassert> // for assert
#include <cctype> // for toupper, tolower, isupper, and islower
#include "measures.hpp"

int editScore(std::string ref, std::string lr)
{
/* Since maf files give the true alignment, we can find the true "edit distance"
 * (or edit score, as we call it) without trying to find an approximation.
 * We can also use this module to find the edit distance between cLRs and the ref
 * using the same metric as when calculating the edit score between the ref and lr
 */
	int score = 0;
	int del = 1;
	int ins = 1;
	int sub = 1;
	int length = ref.length();
	char refBase;
	char base;

	for (int seqIndex = 0; seqIndex < length; seqIndex++) {
		refBase = ref[seqIndex];
		base = lr[seqIndex];

		if (refBase != base) {
			if (refBase == '-') {
				score = score + ins;
			} else if (base == '-') {
				score = score + del;
			} else {
				score = score + sub;
			}
		}
	}		
	return score;
}

int64_t substitutions(std::string ref, std::string read)
// Returns the number of substitutions between the reference and read string
{
	assert( ref.length() == read.length() );

	int64_t subs = 0;

	for (int64_t index = 0; index < ref.length(); index++) {
		if ( ref[index] != '-' and read[index] != '-' and toupper(ref[index]) != toupper(read[index]) ) {
			subs++;
		}			
	}

	return subs;
}

int64_t insertions(std::string ref, std::string read)
// Returns the number of insertions between the reference and read string
{
	assert( ref.length() == read.length() );

	int64_t ins = 0;

	for (int64_t index = 0; index < ref.length(); index++) {
		if (ref[index] == '-' and read[index] != '-') {
			ins++;
		}
	}

	return ins;
}

int64_t deletions(std::string ref, std::string read)
// Returns the number of insertions between the reference and read string
{
	assert( ref.length() == read.length() );

	int64_t del = 0;

	for (int64_t index = 0; index < ref.length(); index++) {
		if (ref[index] != '-' and read[index] == '-') {
			del++;
		}
	}

	return del;
}

int64_t correctedTruePositives(std::string ref, std::string read)
// Returns the number of pairs of bases such that the read base is corrected and
// the read base is equivalent to the reference base.
{
	assert( ref.length() == read.length() );

	int64_t truePositives = 0;

	for (int64_t index = 0; index < ref.length(); index++) {
		if ( (isupper(read[index]) or read[index] == '-') and toupper(read[index]) == toupper(ref[index]) ) {
			truePositives++;		
		}	
	}

	return truePositives;
}

int64_t correctedFalsePositives(std::string ref, std::string read)
// Returns the number of pairs of bases such that the read base is corrected and
// the read base is not equivalent to the reference base.
{
	assert( ref.length() == read.length() );

	int64_t falsePositives = 0;

	for (int64_t index = 0; index < ref.length(); index++) {
		if ( (isupper(read[index]) or read[index] == '-') and toupper(read[index]) != toupper(ref[index]) ) {
			falsePositives++;		
		}	
	}

	return falsePositives;
}

int64_t uncorrectedTruePositive(std::string ref, std::string read)
// Returns the number of pairs of bases where the read base is uncorrected and
// the read base is equivalent to the reference base.
{
	assert( ref.length() == read.length() );

	int64_t truePositives = 0;

	for (int64_t index = 0; index < ref.length(); index++) {
		if ( islower(read[index]) and tolower(read[index]) == tolower(ref[index]) ) {
			truePositives++;		
		}	
	}

	return truePositives;
}

int64_t uncorrectedFalsePositives(std::string ref, std::string read)
// Returns the number of pairs of bases where the read base is uncorrected and
// the read base is not equivalent to the reference base.
{
	assert( ref.length() == read.length() );

	int64_t falsePositives = 0;

	for (int64_t index = 0; index < ref.length(); index++) {
		if ( islower(read[index]) and tolower(read[index]) != tolower(ref[index]) ) {
			falsePositives++;		
		}	
	}

	return falsePositives;
}

int64_t correctedBases(std::string read)
// Returns the number of corrected bases in the read
{
	assert( read.length() > 0 );

	int64_t corrected = 0;

	for (int64_t index = 0; index < read.length(); index++) { 
		if ( isupper(read[index]) or read[index] == '-' ) { 
			corrected++; 
		}	
	}

	return corrected;
}

int64_t uncorrectedBases(std::string read);
// Returns the number of uncorrected bases in the read 
{
	assert( read.length() > 0 );
	
	int64_t uncorrected = 0;

	for (int64_t index = 0; index < read.length(); index++) {
		if ( islower(read[index]) ) { uncorrected++; } 
	}

	return uncorrected;
}
