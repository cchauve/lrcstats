#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <string.h>
#include <unistd.h>
#include <cassert>
// For multithreading
#include <thread>
#include <future>

#include "data/data.hpp"
#include "alignments/alignments.hpp"
#include "measures/measures.hpp"

enum CorrectedReadType {Trimmed,Untrimmed};

int64_t g_threads = 1;
std::string g_mafInputName = "";
std::string g_clrName = "";
std::string g_outputPath = "";
CorrectedReadType g_cReadType = Untrimmed;

struct RawRead_t {
	std::string ref;
	std::string ulr;
	std::string clr;
	ReadInfo readInfo;	
};

struct AlignedTrimmedReads_t {
	TrimmedAlignment alignment;
	ReadInfo readInfo;	
};

struct AlignedUntrimmedReads_t {
	UntrimmedAlignment alignment;
	ReadInfo readInfo;
};

std::vector< RawRead_t > getReadsFromMafAndFasta()
{
	std::ifstream mafInput (g_mafInputName, std::ios::in);
	std::ifstream clrInput (g_clrName, std::ios::in);

	if (!mafInput.is_open() || !clrInput.is_open()) {
		std::cerr << "Unable to open either maf input or corrected long reads file\n";
		return; 
	}	

	std::string mafLine;
	std::string clrLine;

	std::vector< RawRead_t > reads;

	// First, collect all the reads from the FASTA and MAF files
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

		std::vector<std::string> mafTokens = split(mafLine);	

		assert( mafTokens.size() == 7 );

		std::string ulr = mafTokens.at(6);
		std::string readName = mafTokens.at(1);
		int64_t readMafNum = atoi( readName.c_str() );
		std::string readOrient = mafTokens.at(4);

		//Skip line 
		std::getline(mafInput, mafLine); 

		ReadInfo readInfo(readName, refOrient, readOrient, start, srcSize);	

		std::getline(clrInput, clrLine);
		std::string clr = clrLine;

		RawRead_t read;
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

std::vector< std::vector<RawRead_t> > partitionReads( std::vector< RawRead_t > reads ) 
{
	std::vector< RawRead_t >::iterator iter = reads.begin();
	
	int64_t partitionSize = reads.size() / g_threads;
	std::vector< RawRead_t > readsPartition;
	std::vector< std::vector<RawRead_t> > partitions;

	do {
		if (reads.end() - iter > partitionSize) {
			readsPartition.assign(iter, iter + partitionSize);
			iter += partitionSize;
		} else {
			readsPartition.assign(iter, reads.end());
		}
		partitions.push_back(readsPartition);	
	} while ( !reads.empty() );

	return partitions;
}

std::vector< AlignedUntrimmedReads_t > alignUntrimmedReads( std::vector<RawRead_t> reads )
{
	std::vector< UntrimmedAlignments > alignments;

	for (int64_t i = 0; i < reads.size(); i++) {
		read = reads.at(i);
		Alignment alignment(read.ref, read.ulr, read.clr);

		AlignedUntrimmedReads_t aligned;
		aligned.alignment = alignment;
		aligned.readInfo = read.readInfo;
		alignments.push_back(alignments);		
	}
	
	return alignments;
}

std::vector< AlignedTrimmedReads_t > alignTrimmedReads( std::vector<RawRead_t> reads )
{
	std::vector< UntrimmedAlignments > alignments;

	for (int64_t i = 0; i < reads.size(); i++) {
		read = reads.at(i);
		Alignment alignment(read.ref, read.ulr, read.clr);

		AlignedTrimmedReads_t aligned;
		aligned.alignment = alignment;
		aligned.readInfo = read.readInfo;
		alignments.push_back(alignments);		
	}
	
	return alignments;
}

void generateMaf()
{
	// Read the MAF and cLR FASTA file
	std::vector< RawRead_t > reads = getReadsFromMafAndFasta(); 

	// Split the reads vector into g_threads equally sized partition(s) contained in a vector of 
	// RawRead_t vectors
	std::vector< std::vector<RawRead_t> > partitions = partitionReads(reads);

	// Process each partition separately in its own thread 
	std::vector< std::future<std::vector<AlignedUntrimmedReads_t>> > partitionThread;
	
	for (int64_t i = 0; i < partitions.size(); i++) {
		partitionThread.push_back() = std::async( &alignUntrimmedReads, partitions.at(i) );
	} 

	// Once the threads have finished doing their thing, get all the aligned partitions of reads
	std::vector< std::vector<AlignedUntrimmedReads_t> > alignedPartitions;

	for (int64_t i = 0; i < partitionThread.size(); i++) {
		alignedPartitions.push_back() = partitionThread.at(i).get();
	}

	// Write the alignments to MAF file
	MafFile mafOutput(outputPath);

	for (int64_t vectorIndex = 0; vectorIndex < alignedPartitions.size(); vectorIndex++) {
		std::vector< AlignedUntrimmedReads_t > partition = alignedPartitions.at(vectorIndex);	
		for (int64_t partitionIndex` = 0; partitionIndex < partition.size(); partitionIndex++) {
			AlignedUntrimmedReads_t read = partition.at(partitionIndex);
			mafOutput.addReads( read.alignment, read.readInfo );
		} 
	}
}

void generateUntrimmedMaf(std::string mafInputName, std::string clrName, std::string outputPath)
/* Generates a 3-way maf file from data contained in input maf file and cLR file */
{
	std::ifstream mafInput (mafInputName, std::ios::in);
	std::ifstream clrInput (clrName, std::ios::in);
	MafFile mafOutput (outputPath);

	if (!mafInput.is_open() || !clrInput.is_open()) {
		std::cerr << "Unable to open either maf input or corrected long reads file\n";
		return; 
	}	

	std::string mafLine;
	std::string clrLine;

	std::vector<std::string> mafTokens;

	std::string ref = "";
	std::string ulr = "";
	std::string clr = "";

	std::string readName = "";
	std::string refOrient = "";
	std::string readOrient = "";
	std::string start = "";
	std::string srcSize = "";

	bool refNonEmpty;
	bool ulrNonEmpty;

	UntrimmedAlignments alignments(ref, ulr, clr);
	ReadInfo readInfo(readName, refOrient, readOrient, start, srcSize);	

	// Skip first line in maf file
	while (std::getline(mafInput, mafLine) && std::getline(clrInput, clrLine)) {
		//std::cout << mafLine << "\n";
		// Read ref line
		std::getline(mafInput, mafLine);
		//std::cout << mafLine << "\n";

		mafTokens = split(mafLine);	

		assert( mafTokens.size() == 7 );

		ref = mafTokens.at(6);			
		refOrient = mafTokens.at(4);
		start = mafTokens.at(2);
		srcSize = mafTokens.at(5);

		// Read ulr line
		std::getline(mafInput, mafLine);
		//std::cout << mafLine << "\n";

		mafTokens = split(mafLine);	

		assert( mafTokens.size() == 7 );

		ulr = mafTokens.at(6);
		readName = mafTokens.at(1);
		int64_t readMafNum = atoi( readName.c_str() );
		readOrient = mafTokens.at(4);

		//Skip line again
		std::getline(mafInput, mafLine); 
		//std::cout << mafLine << "\n\n";

		readInfo.reset(readName, refOrient, readOrient, start, srcSize);

		// Next, read from clr file
		//std::cout << clrLine << "\n";

		/*
		std::string fastaHeader;
		fastaHeader = clrLine.substr(1, clrLine.npos);
		int64_t readFastaNum = atoi( fastaHeader.c_str() );
		*/
		std::cout << "Aligning read " << readMafNum << "...\n";
		/*
		if ( readFastaNum != readMafNum ) {
			std::cout << "Error; FASTA read number does not equal MAF read number.\n";
			std::cout << "FASTA read number is " << readFastaNum << "\n";
			std::cout << "MAF read number is " << readMafNum << "\n";
			assert( readFastaNum == readMafNum );
		}
		*/

		std::getline(clrInput, clrLine);
		clr = clrLine;
		
		alignments.reset(ref, ulr, clr);

		// Write info into maf file

		mafOutput.addReads(alignments, readInfo);
	}

	mafInput.close();
	clrInput.close();
}

void generateTrimmedMaf(std::string mafInputName, std::string clrName, std::string outputPath)
/* Generates a 3-way maf file from data contained in input maf file and cLR file */
{
	std::ifstream mafInput (mafInputName, std::ios::in);
	std::ifstream clrInput (clrName, std::ios::in);
	MafFile mafOutput (outputPath);

	if (!mafInput.is_open() || !clrInput.is_open()) {
		std::cerr << "Unable to open either maf input or corrected long reads file\n";
		return; 
	}	

	std::string mafLine;
	std::string clrLine;

	std::vector<std::string> mafTokens;

	std::string ref = "";
	std::string ulr = "";
	std::string clr = "";

	std::string readName = "";
	std::string refOrient = "";
	std::string readOrient = "";
	std::string start = "";
	std::string srcSize = "";

	bool refNonEmpty;
	bool ulrNonEmpty;

	TrimmedAlignments alignments(ref, ulr, clr);
	ReadInfo readInfo(readName, refOrient, readOrient, start, srcSize);	

	// Skip first line in maf file
	while (std::getline(mafInput, mafLine) && std::getline(clrInput, clrLine)) {
		//std::cout << mafLine << "\n";
		// Read ref line
		std::getline(mafInput, mafLine);
		//std::cout << mafLine << "\n";

		mafTokens = split(mafLine);	

		assert( mafTokens.size() == 7 );

		ref = mafTokens.at(6);			
		refOrient = mafTokens.at(4);
		start = mafTokens.at(2);
		srcSize = mafTokens.at(5);

		// Read ulr line
		std::getline(mafInput, mafLine);
		//std::cout << mafLine << "\n";

		mafTokens = split(mafLine);	

		assert( mafTokens.size() == 7 );

		ulr = mafTokens.at(6);
		readName = mafTokens.at(1);
		int64_t readMafNum = atoi( readName.c_str() );
		readOrient = mafTokens.at(4);

		//Skip line again
		std::getline(mafInput, mafLine); 
		//std::cout << mafLine << "\n\n";

		readInfo.reset(readName, refOrient, readOrient, start, srcSize);

		// Next, read from clr file
		//std::cout << clrLine << "\n";

		std::string fastaHeader;
		fastaHeader = clrLine.substr(1, clrLine.npos);
		int64_t readFastaNum = atoi( fastaHeader.c_str() );

		std::cout << "Aligning read " << readMafNum << "...\n";
		//assert( readFastaNum == readMafNum );

		std::getline(clrInput, clrLine);
		clr = clrLine;
		
		alignments.reset(ref, ulr, clr);

		// Write info into maf file

		mafOutput.addReads(alignments, readInfo);
	}

	mafInput.close();
	clrInput.close();
}

std::vector<int64_t> untrimmedReadStats(std::string ref, std::string cRead, int64_t cSize, std::string uRead, int64_t uSize)
{
	std::vector<int64_t> statistics;

	// Length of the sequences only, sans gaps
	statistics.push_back(cSize);
	statistics.push_back(uSize);

	// Length of the alignments (i.e. sequences including gaps)
	int64_t cAlignmentLength = cRead.length();
	statistics.push_back( cAlignmentLength );

	int64_t uAlignmentLength = uRead.length();
	statistics.push_back( uAlignmentLength );

	statistics.push_back( getDeletions(ref,cRead) );
	statistics.push_back( getInsertions(ref,cRead) );
	statistics.push_back( getSubstitutions(ref,cRead) );

	statistics.push_back( getDeletions(ref,uRead) );
	statistics.push_back( getInsertions(ref,uRead) );
	statistics.push_back( getSubstitutions(ref,uRead) );

	// True and false positive numbers in the corrected long read
	statistics.push_back( correctedTruePositives(ref,cRead) );
	statistics.push_back( correctedFalsePositives(ref,cRead) );

	statistics.push_back( uncorrectedTruePositives(ref,cRead) );
	statistics.push_back( uncorrectedFalsePositives(ref,cRead) );

	return statistics;
}

std::vector<int64_t> trimmedReadStats(CorrespondingSegments segments)
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
	int64_t cAlignmentLength = clr.length();
	statistics.push_back( cAlignmentLength );

	int64_t uAlignmentLength = ulr.length();
	statistics.push_back( uAlignmentLength );

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

void createUntrimmedStat(std::string mafName, std::string outputPath)
/* Given a 3-way MAF file between cLR, uLR and ref sequences, outputs a
 */
{
	std::ifstream mafFile (mafName, std::ios::in);
	std::ofstream output (outputPath, std::ios::out);
	std::string line = "";

	// Indices where each respective information lies in the MAF file line
	int sizeIndex = 3; 
	int seqIndex = 6;
	// Number of statistics we consider
	int numStatistics = 10;

	// Skip first four lines
	
	for (int i = 0; i < 4; i++) {
		assert( !mafFile.eof() );	
		std::getline(mafFile, line); 
	} 

	// The getline in the while loop condition skips the "a" line
	while (std::getline(mafFile, line)) {
		// Read ref line
		std::getline(mafFile, line);

		std::string ref = split(line).at(seqIndex);
		assert(ref != "");

		// Read ulr line
		std::getline(mafFile, line);

		std::string ulr = split(line).at(seqIndex);
		assert(ulr != "");

		int64_t ulrSize = atoi( split(line).at(sizeIndex).c_str() );
		assert( ulrSize > 0 );

		// Read clr line
		std::getline(mafFile, line);

		std::string clr = split(line).at(seqIndex);	
		assert(clr != "");

		int64_t clrSize = atoi( split(line).at(sizeIndex).c_str() );
		assert( clrSize > 0 );

		// Skip last line, which is empty 
		std::getline(mafFile, line);

		// Write whole read statistics
		std::vector<int64_t> statistics = untrimmedReadStats(ref,clr,clrSize,ulr,ulrSize);

		output << "u ";
		for (int index = 0; index < statistics.size(); index++) {
			output << statistics.at(index) << " ";
		} 
		output << "\n";

		// Write corrected segment statistics
		std::vector<CorrespondingSegments> correspondingSegmentsList = getUntrimmedCorrespondingSegmentsList(clr,ulr,ref);

		for (int index = 0; index < correspondingSegmentsList.size(); index++) {
			CorrespondingSegments segments = correspondingSegmentsList.at(index);
			std::vector<int64_t> statistics = trimmedReadStats(segments);

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

void createTrimmedStat(std::string mafName, std::string outputPath)
/* Given a 3-way MAF file between cLR, uLR and ref sequences, outputs a
 */
{
	std::ifstream mafFile (mafName, std::ios::in);
	std::ofstream output (outputPath, std::ios::out);
	std::string line = "";

	// Indices where each respective information lies in the MAF file line
	int readIndex = 1;
	int sizeIndex = 3; 
	int seqIndex = 6;
	// Number of statistics we consider
	int numStatistics = 10;

	// Skip first four lines
	
	for (int i = 0; i < 4; i++) {
		assert( !mafFile.eof() );	
		std::getline(mafFile, line); 
	} 

	// The getline in the while loop condition skips the "a" line
	while (std::getline(mafFile, line)) {
		// Read ref line
		std::getline(mafFile, line);

		std::string ref = split(line).at(seqIndex);
		assert(ref != "");

		// Read ulr line
		std::getline(mafFile, line);

		std::string ulr = split(line).at(seqIndex);
		assert(ulr != "");

		int64_t ulrSize = atoi( split(line).at(sizeIndex).c_str() );
		assert( ulrSize > 0 );

		// Read clr line
		std::getline(mafFile, line);

		std::string clr = split(line).at(seqIndex);	
		assert(clr != "");

		int64_t clrSize = atoi( split(line).at(sizeIndex).c_str() );
		std::string read = split(line).at(readIndex);
		assert( clrSize > 0 );

		// Skip last line
		std::getline(mafFile, line);

		// Write corrected segment statistics
		std::vector<CorrespondingSegments> correspondingSegmentsList = getTrimmedCorrespondingSegmentsList(clr,ulr,ref);

		if (correspondingSegmentsList.size() == 0) {
			std::cout << "Error at read " << read << "\n";
			assert( correspondingSegmentsList.size() > 0 );
		}

		for (int index = 0; index < correspondingSegmentsList.size(); index++) {
			CorrespondingSegments segments = correspondingSegmentsList.at(index);
			std::vector<int64_t> statistics = trimmedReadStats(segments);

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
		      	  << "[-o output path] [-g perform global statistics] [-p number of threads]\n";
		std::cout << "aligner maf to create 3-way MAF file\n";
		std::cout << "aligner stats to perform statistics on MAF file\n";
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
		
		if (mode != "maf" && mode != "stats") {
			std::cerr << "Please select a mode\n";
			displayUsage();
			return 1;
		}
	}

	std::string mode = argv[1];
	optind = 2;

	// Command line argument handling

	CorrectedReadType cReadType = Untrimmed;
	bool trimmed = false;

	while ((opt = getopt(argc, argv, "m:c:o:htp:")) != -1) {
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
			case 't':
				// Whether the corrected long reads are trimmed or not
				g_cReadType = Trimmed;	
				break;
			case 'h':
				// Displays usage
				displayHelp();
				displayUsage();
				return 0;
			case 'p':
				g_threads = int(optarg);
				break;
			default:
				std::cerr << "Error: unrecognized option.\n";
				displayUsage();
				return 1;
		}
	}

	bool optionsPresent = true;

	// Pass an error if essential option is not set
	
	if (mafInputName == "") {
		std::cerr << "ERROR: MAF input path required\n";
		optionsPresent = false;
	}
	if (outputPath == "") {
		std::cerr << "ERROR: Output path required\n";
		optionsPresent = false;
	}
	if (mode == "maf" && clrName == "") {
		std::cerr << "ERROR: cLR input path required\n";
		optionsPresent = false;
	}

	if (!optionsPresent) {
		displayUsage();
		return 1;
	}

	if (mode == "maf") {
		generateMaf();
	} else {
		if (g_cReadType == Trimmed) {
			createTrimmedStat();				
		} else {
			createUntrimmedStat();
		}
	}
	
	return 0;
}
