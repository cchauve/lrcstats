#include <iostream>
#include <string>
#include "data.hpp"

int main()
{
	std::string prefix = "/global/scratch/seanla/Data/ecoli";
	std::string maf = prefix + "/long-d5/ecoli-long-d5_0001-1read.maf";
	std::string ref = prefix + "/escherichia-coli_reference.fasta";
	std::string ulr = prefix + "/long-d5/ecoli-long-d5_0001-1read.fastq";
	std::string clr = prefix + "/results/may19-2/jabba10x100reads_k41/Jabba-ecoli-long-d5_0001-1read.fastq";	

	Data data(ref, maf, ulr, clr);

	int length = data.length();
	LongReadData reads[length] = data.lrData();
	
	for (int index = 0; index < length; index++) {
		std::cout << reads[index].ref() << "\n";
		std::cout << reads[index].refMaf() << "\n";
		std::cout << reads[index].ulr() << "\n";
		std::cout << reads[index].ulr_maf() << "\n";
		std::cout << reads[index].clr() << "\n";
		
		int segLength = reads[index].cSegs.length();
		CorrectedSegs segs[segLength] = reads[index].cSegs.array();
		
		for (int segIndex = 0; segIndex < segLength; segIndex++) {
			std::cout << segs[segIndex].cSeg() << "\n";
			std::cout << segs[segIndex].refSeg() << "\n";	
		}
	}
}
