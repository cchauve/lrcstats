#include <iostream>
#include <string>
#include <cassert> // for assert
#include <cctype> // for toupper, tolower, isupper, and islower
#include <vector>
#include "measures.hpp"

std::vector< CorrespondingSegments > getCorrespondingSegmentsList(std::string cRead, std::string uRead, std::string ref) 
/* Returns a vector of all the CorrespondingSegments of the given cLR, uLR and reference sequences. */
{
	assert(cRead.length() == uRead.length());	
	assert(cRead.length() == ref.length());	
	assert(ref.length() == uRead.length());	

	int64_t length = ref.length();
	bool inCorrectedSegment = false;
	std::string cReadSegment;
	std::string uReadSegment;
	std::string refSegment;
	CorrespondingSegments correspondingSegments;
	std::vector< CorrespondingSegments > segmentList;

	assert( length > 0 );

	for (int64_t index = 0; index < length; index++) {
		// Check if we've just entered a corrected segment
		if ( not inCorrectedSegment and cRead[index] == 'X') {
			inCorrectedSegment = true;
		} else if (inCorrectedSegment and cRead[index] != 'X') {
			// Add the next base to the corrected segment
			cReadSegment = cReadSegment + cRead[index];
			uReadSegment = uReadSegment + uRead[index];
			refSegment = refSegment + ref[index];
		// Check if we've just left an uncorrected segment
		// If so, add the previous corresponding segment to the vector
		} else if (inCorrectedSegment and cRead[index] == 'X') {
			inCorrectedSegment = false;

			correspondingSegments.cReadSegment = cReadSegment;
			correspondingSegments.uReadSegment = uReadSegment;
			correspondingSegments.refSegment = refSegment;
			segmentList.push_back(correspondingSegments);	

			cReadSegment = "";
			uReadSegment = "";
			refSegment = "";
		}
	}

	return segmentList;
}
SubstitutionProportion getSubstitutionProportion( CorrespondingSegments correspondingSegments )
/* Returns the proportion of getSubstitutions between the reads in the correspondingSegments */
{
	std::string cRead = correspondingSegments.cReadSegment;
	std::string uRead = correspondingSegments.uReadSegment;
	std::string ref = correspondingSegments.refSegment;

	SubstitutionProportion proportion;
	proportion.cRead = getSubstitutions(ref, cRead);
	proportion.uRead = getSubstitutions(ref, uRead);
		
	return proportion;
}

InsertionProportion getInsertionProportion( CorrespondingSegments correspondingSegments )
/* Returns the proportion of getInsertions between the reads in the correspondingSegments */
{
	std::string cRead = correspondingSegments.cReadSegment;
	std::string uRead = correspondingSegments.uReadSegment;
	std::string ref = correspondingSegments.refSegment;

	InsertionProportion proportion;
	proportion.cRead = getInsertions(ref, cRead);
	proportion.uRead = getInsertions(ref, uRead);
		
	return proportion;
}

DeletionProportion getDeletionProportion( CorrespondingSegments correspondingSegments )
/* Returns the proportion of getDeletions between the reads in the correspondingSegments */
{
	std::string cRead = correspondingSegments.cReadSegment;
	std::string uRead = correspondingSegments.uReadSegment;
	std::string ref = correspondingSegments.refSegment;

	DeletionProportion proportion;
	proportion.cRead = getDeletions(ref, cRead);
	proportion.uRead = getDeletions(ref, uRead);
		
	return proportion;
}

int64_t getSubstitutions(std::string ref, std::string read)
// Returns the number of substitutions between the reference and read string
{
	assert( ref.length() == read.length() );

	int64_t subs = 0;

	for (int64_t index = 0; index < ref.length(); index++) {
		char refBase = ref[index];
		char readBase = read[index];
		if ( readBase != 'X' and refBase != '-' and readBase != '-' 
		     and toupper(refBase) != toupper(readBase) ) {
			subs++;
		}			
	}

	return subs;
}

int64_t getInsertions(std::string ref, std::string read)
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

int64_t getDeletions(std::string ref, std::string read)
// Returns the number of deletions between the reference and read string
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

/* DO NOT USE THESE STATISTICS - THEY ARE ERRONEOUS */

int64_t correctedTruePositives(std::string ref, std::string read)
// Returns the number of pairs of bases such that the read base is corrected and
// the read base is equivalent to the reference base.
{
	assert( ref.length() == read.length() );

	int64_t truePositives = 0;

	for (int64_t index = 0; index < ref.length(); index++) {
		char refBase = ref[index];
		char readBase = read[index];
		if ( (isupper(readBase) or readBase == '-') and readBase != 'X' and refBase != 'X' 
		      and toupper(readBase) == toupper(refBase) ) {
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
		char readBase = read[index];
		char refBase = ref[index];
		if ( (isupper(readBase) or readBase == '-') and readBase != 'X' and refBase != 'X' 
		      and toupper(readBase) != toupper(refBase) ) {
			falsePositives++;		
		}	
	}

	return falsePositives;
}

int64_t uncorrectedTruePositives(std::string ref, std::string read)
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
