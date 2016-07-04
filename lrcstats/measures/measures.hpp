#ifndef MEASURES_H
#define MEASURES_H

// The following three structs are simple containers for the proportion of the respective
// mutations between a corrected long read segment and its respective uncorrected long
// read segment
struct InsertionProportion
{
        int64_t cRead;
        int64_t uRead;
};

struct DeletionProportion
{
        int64_t cRead;
        int64_t uRead;
};

struct SubstitutionProportion
{
        int64_t cRead;
        int64_t uRead;
};

struct CorrespondingSegments
/* This struct is a simple container for corrected segments of corrected long reads and its
 *  * respective segments in the uncorrected long read and reference sequences. */
{
        std::string cReadSegment;
        std::string uReadSegment;
        std::string refSegment;
};

std::vector< CorrespondingSegments > getCorrespondingSegmentsList(std::string cRead, std::string uRead, std::string ref);
/* Returns a vector of all the CorrespondingSegments of the given cLR, uLR and reference sequences. */

SubstitutionProportion getSubstitutionProportion( CorrespondingSegments correspondingSegments);
/* Returns the proportion of substitutions between the reads in the correspondingSegments */

InsertionProportion getInsertionProportion( CorrespondingSegments correspondingSegments);
/* Returns the proportion of insertions between the reads in the correspondingSegments */

DeletionProportion getDeletionProportion( CorrespondingSegments correspondingSegments);
/* Returns the proportion of deletions between the reads in the correspondingSegments */

int64_t editScore(std::string ref, std::string lr);
/* Returns the "edit score" of two alignments. 
 * Uses a similar scoring schema as the Levenshtein edit distance equations. */

int64_t substitutions(std::string ref, std::string read);
// Returns the number of substitutions between the reference and read string

int64_t insertions(std::string ref, std::string read);
// Returns the number of insertions between the reference and read string

int64_t deletions(std::string ref, std::string read);
// Returns the number of insertions between the reference and read string

int64_t correctedTruePositives(std::string ref, std::string read);
// Returns the number of pairs of bases such that the read base is corrected and
// the read base is equivalent to the reference base.

int64_t correctedFalsePositives(std::string ref, std::string read);
// Returns the number of pairs of bases such that the read base is corrected and
// the read base is not equivalent to the reference base.

int64_t uncorrectedTruePositives(std::string ref, std::string read);
// Returns the number of pairs of bases where the read base is uncorrected and
// the read base is equivalent to the reference base.

int64_t uncorrectedFalsePositives(std::string ref, std::string read);
// Returns the number of pairs of bases where the read base is uncorrected and
// the read base is not equivalent to the reference base.

int64_t correctedBases(std::string read);
// Returns the number of corrected bases in the read

int64_t uncorrectedBases(std::string read);
// Returns the number of uncorrected bases in the read 

#endif // MEASURES_H
