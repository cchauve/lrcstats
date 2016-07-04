#include <iostream>
#include <string>
#include <cassert> // for assert
#include <cctype> // for toupper, tolower, isupper, and islower
#include "measures.hpp"

/* The following three structs are simple containers for the proportion of the respective
 * mutations between a corrected long read segment and its respective uncorrected long
 * read segment */

struct InsertionProportion 
{
	int64_t cReadQuantity;
	int64_t uReadQuanity;
};

struct DeletionProportion 
{
	int64_t cReadQuantity;
	int64_t uReadQuanity;
};

struct SubstitutionProportion 
{
	int64_t cReadQuantity;
	int64_t uReadQuanity;
};

struct CorrespondingSegments 
/* This struct is a simple container for corrected segments of corrected long reads and its
 * respective segments in the uncorrected long read and reference sequences. */
{
	std::string cReadSegment;
	std::string uReadSegment;
	std::string refSegment;
};

std::vector< CorrespondingSegments > getCorrespondingSegmentsList(std::string cRead, std::string uRead, std::string ref) 
/* Returns a vector of all the CorrespondingSegments of the given cLR, uLR and reference sequences. */
{
	assert(cRead.length() == uRead.length());	
	assert(cRead.length() == ref.length());	
	assert(ref.length() == uRead.length());	

	int64_t length = ref.length();
	bool inCorrectedSegment;
	std::string cReadSegment;
	std::string uReadSegment;
	std::string refSegment;
	CorrespondingSegments correspondingSegments;
	std::vector< CorrespondingSegments > segmentList;

	for (int index = 0; index < length; index++) {
		if ( isupper(cRead[index]) ) {
			inCorrectedSegment = true;
		} else if ( islower(cRead[index]) and inCorrectedSegment ) {
			inCorrectedSegment = false;

			correspondingSegments.cReadSegment = cReadSegment;
			correspondingSegments.uReadSegment = uReadSegment;
			correspondingSegments.refSegment = refSegment;
			
			segmentList.push_back(correspondingSegments);	

			cReadSegment = "";
			uReadSegment = "";
			refSegment = "";
		}
		
		if (inCorrectedSegment) {
			cReadSegment = cReadSegment + cRead[index];
			uReadSegment = uReadSegment + uRead[index];
			refSegment = refSegment + ref[index];
		}
	}

	return segmentList;
}

SubstitutionProportion getSubstitutionProportion( CorrespondingSegments correspondingSegments )
/* Returns the proportion of substitutions between the reads in the correspondingSegments */
{
	cRead = correspondingSegments.cReadSegment;
	uRead = correspondingSegments.uReadSegment;
	ref = correspondingSegments.refSegment;

	SubstitutionProportion proportion;
	proportion.cRead = substitutions(ref, cRead);
	proportion.cRead = substitutions(ref, uRead);
		
	return proportion;
}

InsertionProportion getInsertionProportion( CorrespondingSegments correspondingSegments )
/* Returns the proportion of insertions between the reads in the correspondingSegments */
{
	cRead = correspondingSegments.cReadSegment;
	uRead = correspondingSegments.uReadSegment;
	ref = correspondingSegments.refSegment;

	InsertionProportion proportion;
	proportion.cRead = insertions(ref, cRead);
	proportion.cRead = insertions(ref, uRead);
		
	return proportion;
}

DeletionProportion getDeletionProportion( CorrespondingSegments correspondingSegments )
/* Returns the proportion of deletions between the reads in the correspondingSegments */
{
	cRead = correspondingSegments.cReadSegment;
	uRead = correspondingSegments.uReadSegment;
	ref = correspondingSegments.refSegment;

	DeletionProportion proportion;
	proportion.cRead = deletions(ref, cRead);
	proportion.cRead = deletions(ref, uRead);
		
	return proportion;
}

int64_t editScore(std::string ref, std::string lr)
/* Since maf files give the true alignment, we can find the true "edit distance"
 * (or edit score, as we call it) without trying to find an approximation.
 * We can also use this module to find the edit distance between cLRs and the ref
 * using the same metric as when calculating the edit score between the ref and lr
 */
{
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

int64_t uncorrectedBases(std::string read)
// Returns the number of uncorrected bases in the read 
{
	assert( read.length() > 0 );
	
	int64_t uncorrected = 0;

	for (int64_t index = 0; index < read.length(); index++) {
		if ( islower(read[index]) ) { uncorrected++; } 
	}

	return uncorrected;
}

std::vector<MutationProportion> getInsertionProportion(std::string cRead, std::string uRead, std::string ref)
{

}
