#include <iostream>
#include <string>
#include <algorithm>

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

