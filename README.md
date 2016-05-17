Hybrid Correction Statistics (hcstats)

Ideas
-----
The first idea is to return the ratio d_c/d_u, where is d_u is the edit distance of the uncorrected long read and d_c is the edit distance of the corrected long read. Finding d_c would require mapping the corresponding long read onto the reference genome using BWA-MEM.

The second idea is given the uncorrected and corrected versions of a long read, uLR and cLR respectively, take the set of all uncorrected segments of cLR. Map each segment back onto the uLR, this will give sections of uLR which the corrected segments of cLR will map to. Find the optimal mapping of corrected segments onto uLR using dynamic programming, and then find the ratio of d_c/d_u for only corrected regions as above.
