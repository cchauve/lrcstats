#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <string.h>
#include <unistd.h>
#include <cassert>
// For multithreading
#include <future>
#include <thread>
// For std::exit
#include <cstdlib>

#include "data.hpp"
#include "alignments.hpp"
#include "measures.hpp"

enum CorrectedReadType {Trimmed,Untrimmed};
enum ExtensionType {Extended,Unextended};

// Max number of threads
int64_t g_threads = std::thread::hardware_concurrency();
// Input and output file names
std::string g_mafInputName = "";
std::string g_clrName = "";
std::string g_outputPath = "";
// Corrected read type
CorrectedReadType g_trimType = Untrimmed;
ExtensionType g_extensionType = Unextended;

std::vector< Read_t > getReadsFromMafAndFasta()
/* Get reference sequence, corrected and uncorrected reads from MAF and FASTA files.
 * Assumes reads are in the same order in MAF and FASTA files. 
 * Outputs
 * - reads: vector of Read_t objects
 */
{
	// Open the MAF and FASTA files
	std::ifstream mafInput (g_mafInputName, std::ios::in);
	std::ifstream clrInput (g_clrName, std::ios::in);

	if (!mafInput.is_open() || !clrInput.is_open()) {
		std::cerr << "Unable to open either maf input or corrected long reads file\n";
		std::exit(1);
	}	

	std::string mafLine;
	std::string clrLine;

	std::vector< Read_t > reads;

	// First, collect all the reads from the FASTA and MAF files
	// The get line in the while loop conditional skips the empty "a" line in the MAF line
	// and the header line in the FASTA file.
	while (std::getline(mafInput, mafLine) && std::getline(clrInput, clrLine)) {
		// Read ref line
		std::getline(mafInput, mafLine);

		std::vector<std::string> mafTokens = split(mafLine);	

		assert( mafTokens.size() == 7 );

		std::string ref = mafTokens.at(6);			
		std::string refOrient = mafTokens.at(4);
		std::string start = mafTokens.at(2);
		std::string srcSize = mafTokens.at(5);

		// Read ulr line
		std::getline(mafInput, mafLine);

		mafTokens = split(mafLine);	

		assert( mafTokens.size() == 7 );

		std::string ulr = mafTokens.at(6);
		std::string readName = mafTokens.at(1);
		// read number of the current read
		int64_t readMafNum = atoi( readName.c_str() );
		std::string readOrient = mafTokens.at(4);

		//Skip line 
		std::getline(mafInput, mafLine); 

		ReadInfo readInfo;

		readInfo.name = readName;
		readInfo.refOrient = refOrient;
		readInfo.readOrient = readOrient;
		readInfo.start = start;
		readInfo.srcSize = srcSize;

		std::getline(clrInput, clrLine);
		std::string clr = clrLine;

		Read_t read;
		read.ref = ref;	
		read.ulr = ulr;
		read.clr = clr;
		read.readInfo = readInfo;

		reads.push_back(read);
	}

	mafInput.close();
	clrInput.close();

	return reads;
}

std::vector< std::vector<Read_t> > partitionReads( std::vector< Read_t > &reads ) 
/* Partitions the reads into g_threads number of partitions
 */
{
	// Holds individual partitions of reads
	std::vector< Read_t > readsPartition;
	// Holds all partitions of reads
	std::vector< std::vector<Read_t> > partitions;
	std::vector< Read_t >::iterator iter = reads.begin();

	// Size of partition
	int64_t partitionSize = reads.size() / g_threads;
	// Number of partitions that will have partitionSize + 1 number of reads
	int64_t extra = reads.size() % g_threads;

	// Partition the reads
	for (int64_t i = 0; i < g_threads; i++) {
		int64_t offset = partitionSize + (i < extra ? 1 : 0);
		readsPartition.assign(iter, iter + offset);
		partitions.push_back(readsPartition);	
		iter += offset;
	}

	return partitions;
}

Read_t findAlignment( Read_t &unalignedReads ) 
/* Align the reference, uncorrected and corrected read.
 */
{
	Read_t alignedReads;
	// Use a different alignment object depending on the trim and extension type
	if (g_trimType == Trimmed) {
		if (g_extensionType == Extended) {
			ExtendedTrimmedAlignments alignment;
			alignedReads = alignment.align(unalignedReads.ref, unalignedReads.ulr, unalignedReads.clr);
		} else {
			TrimmedAlignments alignment;
			alignedReads = alignment.align(unalignedReads.ref, unalignedReads.ulr, unalignedReads.clr);
		} 
	} else {
		if (g_extensionType == Extended) {
			ExtendedUntrimmedAlignments alignment;
			alignedReads = alignment.align(unalignedReads.ref, unalignedReads.ulr, unalignedReads.clr);
		} else {
			UntrimmedAlignments alignment;
			alignedReads = alignment.align(unalignedReads.ref, unalignedReads.ulr, unalignedReads.clr);
		}
	}
	alignedReads.readInfo = unalignedReads.readInfo;
	return alignedReads;
}

std::vector<Read_t> alignReads( std::vector<Read_t> reads )
/* Align partitions of reads
 */
{
	std::vector<Read_t> alignments;
	// Align one read after the other
	for (int64_t i = 0; i < reads.size(); i++) {
		Read_t unalignedReads = reads.at(i);
		Read_t alignedReads = findAlignment(unalignedReads);
		alignments.push_back(alignedReads);
	}
	return alignments;
}

void generateMaf()
/* Generates a three-way MAF file between the reference, uncorrected and corrected reads
 */
{
	// Read the MAF and cLR FASTA file
	std::cout << "Reading MAF and FASTA files...\n";
	std::vector< Read_t > reads = getReadsFromMafAndFasta(); 

	// Split the reads vector into g_threads equally sized partition(s) contained in a vector of 
	// Read_t vectors
	std::cout << "Partitioning reads...\n";
	std::vector< std::vector<Read_t> > partitions = partitionReads(reads);

	// Process each partition separately in its own thread 
	std::cout << "Aligning " << ::g_threads << " partitions of reads concurrently...\n";
	std::vector< std::future< std::vector<Read_t> > > partitionThread;
	
	// Only create g_threads - 1 new threads; work will also be done on the main thread
	for (int64_t i = 1; i < partitions.size(); i++) {
		partitionThread.push_back( std::async(std::launch::async, alignReads, 
			partitions.at(i)) );
	} 

	// Once the threads have finished doing their thing, get all the aligned partitions of reads
	std::vector< std::vector<Read_t> > alignedPartitions;

	// Perform work in this thread, too
	alignedPartitions.push_back( alignReads( partitions.at(0) ) );

	for (int64_t i = 0; i < partitionThread.size(); i++) {
		alignedPartitions.push_back( partitionThread.at(i).get() );
	}
	
	// Write the alignments to MAF file
	std::cout << "Writing alignments to MAF file...\n";
	MafFile mafOutput(g_outputPath);

	for (int64_t vectorIndex = 0; vectorIndex < alignedPartitions.size(); vectorIndex++) {
		std::vector< Read_t > partition = alignedPartitions.at(vectorIndex);	
		for (int64_t partitionIndex = 0; partitionIndex < partition.size(); partitionIndex++) {
			Read_t reads = partition.at(partitionIndex);
			mafOutput.addReads( reads );
		} 
	}
	std::cout << "Three-way MAF file construction complete.\n";
}

std::vector<int64_t> untrimmedReadStats(std::string ref, std::string cRead, int64_t cSize, std::string uRead, int64_t uSize)
/* Collects untrimmed read statistics 
 */
{
	std::vector<int64_t> statistics;

	// Length of the sequences only, sans gaps
	statistics.push_back(cSize);
	statistics.push_back(uSize);

	// Length of the alignment
	int64_t alignmentLength = boundarylessLength(cRead);
	statistics.push_back( alignmentLength );

	// Find the number of mutations for the corrected and uncorrected reads
	statistics.push_back( getDeletions(ref,cRead) );
	statistics.push_back( getInsertions(ref,cRead) );
	statistics.push_back( getSubstitutions(ref,cRead) );

	statistics.push_back( getDeletions(ref,uRead) );
	statistics.push_back( getInsertions(ref,uRead) );
	statistics.push_back( getSubstitutions(ref,uRead) );

	return statistics;
}

std::vector<int64_t> trimmedReadStats(CorrespondingSegments segments)
/* Collects trimmed read statistics 
 */
{
	std::vector<int64_t> statistics;

	std::string clr = segments.cReadSegment;
	std::string ulr = segments.uReadSegment;

	// Length of the sequences only, sans gaps
	int64_t cLength = gaplessLength(clr);
	statistics.push_back(cLength);

	int64_t uLength = gaplessLength(ulr);
	statistics.push_back(uLength);

	// Length of the alignments (i.e. sequences including gaps)
	int64_t alignmentLength = clr.length();
	statistics.push_back( alignmentLength );

	// Push the number of mutations in the corrected segments and its
	// corresponding segment in the uncorrected long read

	DeletionProportion delProp = getDeletionProportion( segments );
	InsertionProportion insProp = getInsertionProportion( segments ); 
	SubstitutionProportion subProp = getSubstitutionProportion( segments );

	statistics.push_back(delProp.cRead);
	statistics.push_back(insProp.cRead);
	statistics.push_back(subProp.cRead);

	statistics.push_back(delProp.uRead);
	statistics.push_back(insProp.uRead);
	statistics.push_back(subProp.uRead);

	return statistics;
}

std::string stripReadIdSuffix(std::string readId)
/* Removes the suffix of the read ID token
 */
{
	std::string strippedReadId = "";	
	int index = 0;
	while (index < readId.length() and readId[index] != '.') {
		strippedReadId += readId[index];
		index++;
	}
	return strippedReadId;
}

void createStats()
/* Given a 3-way MAF file between cLR, uLR and ref sequences, outputs a text file containing stats
 */
{
	std::ifstream mafFile (g_mafInputName, std::ios::in);
	std::ofstream output (g_outputPath, std::ios::out);
	std::string line = "";

	// Indices where each respective information lies in the MAF file line
	int readIdIndex = 1;
	int sizeIndex = 3; 
	int seqIndex = 6;
	// Number of statistics we consider
	int numStatistics = 10;

	// Skip first four lines
	for (int i = 0; i < 4; i++) {
		assert( !mafFile.eof() );	
		std::getline(mafFile, line); 
	} 

	//write the legend
	std::string legend = "# [Read ID]: The ID of the read. Takes on any string value.\n"
		"# [Type]: If 't', indicates that the statistics are for only corrected segments of the read.\n"
                "#         If 'u', indicates that the statistics are for the entire segment of the read.\n"
		"# [cLR Length]: Length of the corrected long read segment without '-'. Takes on values > 0.\n"
		"# [uLR Length]: Length of the uncorrected long read segment without '-'. Takes on values > 0.\n"
		"# [Alignment Length]: Length of the segment of the alignment. Takes on values > 0.\n"
                "# [cLR Del]: Number of deletions in the cLR alignment segment. Positive integer values.\n"
                "# [cLR Ins]: Number of insertions in the cLR alignment segment. Positive integer values.\n"
                "# [cLR Sub]: Number of substitutions in the cLR alignment segment. Positive integer values.\n"
                "# [uLR Del]: Number of deletions in the uLR alignment segment. Positive integer values.\n"
                "# [uLR Ins]: Number of insertions in the uLR alignment segment. Positive integer values.\n"
                "# [uLR Sub]: Number of substitutions in the uLR alignment segment. Positive integer values.\n";
	output << legend;

	// write the header line
	std::string header = "# [Read ID] [Type] [cLR Length] [uLR Length] [Alignment Length] [cLR Del] [cLR Ins] [cLR Sub] [uLR Del] [uLR Ins] [uLR Sub]";
	output << header << std::endl;

	// The getline in the while loop condition skips the "a" line
	while (std::getline(mafFile, line)) {
		// Read ref line
		std::getline(mafFile, line);

		std::string ref = split(line).at(seqIndex);

		// Read ulr line
		std::getline(mafFile, line);

		std::vector< std::string > tokens = split(line);

		std::string readId = tokens.at(readIdIndex);
		readId = stripReadIdSuffix(readId); 

		std::string ulr = tokens.at(seqIndex);

		int64_t ulrSize = atoi( split(line).at(sizeIndex).c_str() );

		// Read clr line
		std::getline(mafFile, line);

		std::string clr = split(line).at(seqIndex);	

		int64_t clrSize = atoi( split(line).at(sizeIndex).c_str() );

		// Skip last line, which is empty 
		std::getline(mafFile, line);

		// If the read type if untrimmed, then do untrimmed statistics 
		if (g_trimType == Untrimmed) {
			std::vector<int64_t> statistics = untrimmedReadStats(ref,clr,clrSize,ulr,ulrSize);
			output << readId << " ";
			output << "u ";
			for (int index = 0; index < statistics.size(); index++) {
				output << statistics.at(index) << " ";
			} 
			output << "\n";
		}

		// Write trimmed read statistics
		std::vector<CorrespondingSegments> correspondingSegmentsList = getCorrespondingSegmentsList(clr,ulr,ref);

		for (int index = 0; index < correspondingSegmentsList.size(); index++) {
			CorrespondingSegments segments = correspondingSegmentsList.at(index);
			std::vector<int64_t> statistics = trimmedReadStats(segments);
			output << readId << " ";
			output << "t ";
			for (int i = 0; i < statistics.size(); i++) {
				output << statistics.at(i) << " ";
			}
			output << "\n";
		}
	}

	mafFile.close();
	output.close();
}

void displayHelp()
{
	std::cout << "This program has two functions: outputting three way MAF alignments between corrected long reads,\n";
	std::cout << "uncorrected long reads, and reference sequences, and computing simple statistics about the\n";
	std::cout << "corrected. This program accepts either trimmed or untrimmed corrected long reads. If the\n";
	std::cout << "long reads are trimmed and MAF file creation mode is chosen, the three way alignments will contain\n";
	std::cout << "triples of the form (X,-,-) (where the bases correspond to the cLR, uLR and ref, respectively)\n";
	std::cout << "that indicates the boundaries of the original individual trimmed long read segments.\n";
}

void displayUsage()
{
		std::cout << "Usage: aligner [mode] [-m MAF input path] [-c cLR input path] [-t cLR are trimmed] "
		      	  << "[-e cLR are extended] [-o output path] [-p number of threads]\n";
		std::cout << "aligner maf to create 3-way MAF file\n";
		std::cout << "aligner stats to perform statistics on MAF file\n";
		std::cout << "Note: stats mode only uses 1 thread and ignores the -p option\n";
}

int main(int argc, char *argv[])
{
	int opt;

	if (argc == 1) {
		std::cerr << "Please select a mode\n";
		displayUsage();
		return 1;
	} else {

		std::string mode = argv[1];
		
		if (mode != "maf" and mode != "stats") {
			std::cerr << "Please select a mode\n";
			displayUsage();
			return 1;
		}
	}

	std::string mode = argv[1];
	optind = 2;

	// Command line argument handling

	bool trimmed = false;

	while ((opt = getopt(argc, argv, "m:c:o:hetp:")) != -1) {
		switch (opt) {
			case 'm':
				// Source maf file name
				g_mafInputName = optarg;
				break;
			case 'c':
				// cLR file name
				g_clrName = optarg;
				break;
			case 'o':
				// output file path
				g_outputPath = optarg;
				break;
			case 'e':
				g_extensionType = Extended;
				break;
			case 't':
				// Whether the corrected long reads are trimmed or not
				g_trimType = Trimmed;	
				break;
			case 'h':
				// Displays usage
				displayHelp();
				displayUsage();
				return 0;
			case 'p':
				// Number of threads to perform alignment
				::g_threads = atoi(optarg);
				break;
			default:
				std::cerr << "Error: unrecognized option.\n";
				displayUsage();
				return 1;
		}
	}

	bool optionsPresent = true;

	// Pass an error if essential option is not set
	
	if (g_mafInputName == "") {
		std::cerr << "ERROR: MAF input path required\n";
		optionsPresent = false;
	}
	if (g_outputPath == "") {
		std::cerr << "ERROR: Output path required\n";
		optionsPresent = false;
	}
	if (mode == "maf" and g_clrName == "") {
		std::cerr << "ERROR: cLR input path required\n";
		optionsPresent = false;
	}

	if (!optionsPresent) {
		displayUsage();
		return 1;
	}

	// Create either a MAF file or find statistics from a three-way  MAF file
	if (mode == "maf") {
		generateMaf();
	} else {
		createStats();				
	}
	
	return 0;
}
