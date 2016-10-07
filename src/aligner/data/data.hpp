#ifndef DATA_H
#define DATA_H

#include "../alignments/alignments.hpp"

std::vector<std::string> split(const std::string &str);
/* Splits a string into its constituent tokens similar to the .split() function in python. */

int64_t gaplessLength(std::string read);
/* Returns the length of a sequence without gaps. */

struct ReadInfo
/* Contains the read information for the two-way MAF file for the uncorrected long read and reference sequence 
 */
{
	std::string name;
	std::string refOrient;
	std::string readOrient;
	std::string start;
	std::string srcSize;
};

struct Read_t
/* Carries the reference and uncorrected alignments from the two-way MAF file and the corrected long read sequence
 * from the FASTA file.
 */
{
	std::string ref;
	std::string ulr;
	std::string clr;
	ReadInfo readInfo;
};

class MafFile
/* Object to create a MAF containing 3-way alignments between a reference, uLR and cLR 
 */
{
	public:
		MafFile(std::string fileName);
		void addReads(Read_t reads);
	private:
		std::string filename;
};

#endif /* DATA_H */
