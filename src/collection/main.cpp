#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <string.h>
#include <unistd.h>
#include <cassert>

#include "data/data.hpp"
#include "alignments/alignments.hpp"
#include "measures/measures.hpp"

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

	std::vector<std::string> mafTokens;
	std::vector<std::string> clrTokens;

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

	while (!mafInput.eof() && !clrInput.eof()) {
		// Read from maf file first
	
		// //Skip line
		std::getline(mafInput, mafLine); 
		//std::cout << mafLine << "\n";

		// Read ref line
		std::getline(mafInput, mafLine);
		//std::cout << mafLine << "\n";

		if (mafLine != "") {
			mafTokens = split(mafLine);	

			assert( mafTokens.size() > 5 );

			ref = mafTokens.at(6);			
			refOrient = mafTokens.at(4);
			start = mafTokens.at(2);
			srcSize = mafTokens.at(5);
			refNonEmpty = true;
		} else {
			refNonEmpty = false;
		}

		// Read ulr line
		std::getline(mafInput, mafLine);
		//std::cout << mafLine << "\n";

		if (mafLine != "") {
			mafTokens = split(mafLine);	

			assert( mafTokens.size() > 5 );

			ulr = mafTokens.at(6);
			readName = mafTokens.at(1);
			readOrient = mafTokens.at(4);
			ulrNonEmpty = true;
		} else {
			ulrNonEmpty = false;
		}

		//Skip line again
		std::getline(mafInput, mafLine); 
		//std::cout << mafLine << "\n\n";

		if (refNonEmpty && ulrNonEmpty) {
			readInfo.reset(readName, refOrient, readOrient, start, srcSize);
			// Next, read from clr file
		
			// Skip first line
			getline(clrInput, clr);
			
			// Read clr line
			getline(clrInput, clr);
		
			if (clr != "") {
				alignments.reset(ref, ulr, clr);

				// Write info into maf file
				mafOutput.addReads(alignments, readInfo);
			}	
		}
		clr = "";
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

	std::vector<std::string> mafTokens;
	std::vector<std::string> clrTokens;

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

	while (!mafInput.eof() && !clrInput.eof()) {
		// Read from maf file first
	
		// //Skip line
		std::getline(mafInput, mafLine); 
		//std::cout << mafLine << "\n";

		// Read ref line
		std::getline(mafInput, mafLine);
		//std::cout << mafLine << "\n";

		if (mafLine != "") {
			mafTokens = split(mafLine);	

			assert( mafTokens.size() > 5 );

			ref = mafTokens.at(6);			
			refOrient = mafTokens.at(4);
			start = mafTokens.at(2);
			srcSize = mafTokens.at(5);
			
			refNonEmpty = true;
		} else {
			refNonEmpty = false;
		}

		// Read ulr line
		std::getline(mafInput, mafLine);
		//std::cout << mafLine << "\n";

		if (mafLine != "") {
			mafTokens = split(mafLine);	

			assert( mafTokens.size() > 5 );

			ulr = mafTokens.at(6);
			readName = mafTokens.at(1);
			readOrient = mafTokens.at(4);
			ulrNonEmpty = true;
		} else {
			ulrNonEmpty = false;
		}

		//Skip line again
		std::getline(mafInput, mafLine); 
		//std::cout << mafLine << "\n\n";

		if (refNonEmpty && ulrNonEmpty) {
			// Reset readInfo object
			readInfo.reset(readName, refOrient, readOrient, start, srcSize);
			// Next, read from clr file
		
			// Skip first line
			getline(clrInput, clr);

			// Read clr line
			getline(clrInput, clr);
		
				if (clr != "") {
				alignments.reset(ref, ulr, clr);

				// Write info into maf file
				mafOutput.addReads(alignments, readInfo);
			}	
		}
		clr = "";
	}

	mafInput.close();
	clrInput.close();
}

std::vector<int64_t> untrimmedReadStats(std::string ref, std::string cRead, int64_t cSize, std::string uRead, int64_t uSize)
{
	std::vector<int64_t> statistics;

	statistics.push_back(cSize);
	statistics.push_back(uSize);

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

	int64_t cLength = gaplessLength(clr);
	statistics.push_back(cLength);

	int64_t uLength = gaplessLength(ulr);
	statistics.push_back(uLength);

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

		// Skip last line
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
			for (int i = 0; i < 7; i++) {
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
	int sizeIndex = 3; 
	int seqIndex = 6;
	// Number of statistics we consider
	int numStatistics = 10;

	// Skip first four lines
	
	for (int i = 0; i < 4; i++) {
		assert( !mafFile.eof() );	
		std::getline(mafFile, line); 
	} 

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

		// Skip last line
		std::getline(mafFile, line);

		// Write corrected segment statistics
		std::vector<CorrespondingSegments> correspondingSegmentsList = getTrimmedCorrespondingSegmentsList(clr,ulr,ref);

		for (int index = 0; index < correspondingSegmentsList.size(); index++) {
			CorrespondingSegments segments = correspondingSegmentsList.at(index);
			std::vector<int64_t> statistics = trimmedReadStats(segments);

			assert( statistics.size() == 7 );

			output << "t ";
			for (int i = 0; i < 7; i++) {
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
		std::cerr << "Usage: lrcstats [mode] [-m MAF input path] [-c cLR input path] [-t cLR are trimmed] "
		      	  << "[-o MAF output path]\n";
		std::cerr << "lrcstats maf to create 3-way MAF file\n";
		std::cerr << "lrcstats stats to perform statistics on MAF file\n";
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

	std::string mafInputName = "";
	std::string clrName = "";
	std::string outputPath = "output.maf";
	bool trimmed = false;

	while ((opt = getopt(argc, argv, "m:c:o:ht")) != -1) {
		switch (opt) {
			case 'm':
				// Source maf file name
				mafInputName = optarg;
				break;
			case 'c':
				// cLR file name
				clrName = optarg;
				break;
			case 'o':
				// maf output file name
				outputPath = optarg;
				break;
			case 't':
				// Whether the corrected long reads are trimmed or not
				trimmed = true;
				break;
			case 'h':
				// Displays usage
				displayHelp();
				displayUsage();
				return 0;
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
		if (trimmed) {
			generateTrimmedMaf(mafInputName, clrName, outputPath);
		} else {
			generateUntrimmedMaf(mafInputName, clrName, outputPath);
		}
	} else {
		if (trimmed) {
			createTrimmedStat(mafInputName,outputPath);				
		} else {
			createUntrimmedStat(mafInputName,outputPath);
		}
	}
	
	return 0;
}
