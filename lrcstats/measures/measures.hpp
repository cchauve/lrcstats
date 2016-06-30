#ifndef MEASURES_H
#define MEASURES_H

#include <cstdint>

int64_t editScore(std::string ref, std::string lr);
/* Returns the "edit score" of two alignments. 
 * Uses a similar scoring schema as the Levenshtein edit distance equations. */

int64_t substitutions(std::string ref, std::string read);
// Returns the number of substitutions between the reference and read string

int64_t insertions(std::string ref, std::string read);
// Returns the number of insertions between the reference and read string

int64_t deletions(std::string ref, std::string read);
// Returns the number of insertions between the reference and read string

int64_t correctTruePositives(std::string ref, std::string read);
// Returns the number of pairs of bases such that the read base is corrected and
// the read base is equivalent to the reference base.

int64_t correctFalsePositives(std::string ref, std::string read);
// Returns the number of pairs of bases such that the read base is corrected and
// the read base is not equivalent to the reference base.

int64_t uncorrectedTruePositive(std::string ref, std::string read);
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
