#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <string.h>
#include <unistd.h>

#include "data/data.hpp"
#include "alignments/alignments.hpp"
#include "measures/measures.hpp"

void generateMaf(std::string mafInputName, std::string clrName, std::string mafOutputName, bool isProovread)
/* Generates a 3-way maf file from data contained in input maf file and cLR file */
{
	std::ifstream mafInput (mafInputName, std::ios::in);
	std::ifstream clrInput (clrName, std::ios::in);
	MafFile mafOutput (mafOutputName);

	if (!mafInput.is_open() || !clrInput.is_open()) {
		std::cerr << "Unable to open either maf input or corrected long reads file\n";
		return; 
	}	

	std::string mafLine;
	std::string clrLine;

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

	if (isProovread) {
		ProovreadAlignments alignments(ref, ulr, clr);
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
				getline(clrInput, clrLine);
			
				if (clrLine[0] != '>') {
					clr = clr + clrLine;
					//std::cout << clrLine << "\n";
				}

				// Start reading the first line of clr

				while ( getline(clrInput, clrLine) && clrLine[0] != '>') {
					clr = clr + clrLine;
					//std::cout << clrLine << "\n";
				}

			/*	
			std::cout << ref << "\n";
			std::cout << ulr << "\n";	
			std::cout << clr << "\n";
			*/
			
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
	} else {
		GenericAlignments alignments(ref, ulr, clr);
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
				getline(clrInput, clrLine);
			
				if (clrLine[0] != '>') {
					clr = clr + clrLine;
					//std::cout << clrLine << "\n";
				}

				// Start reading the first line of clr

				while ( getline(clrInput, clrLine) && clrLine[0] != '>') {
					clr = clr + clrLine;
					//std::cout << clrLine << "\n";
				}

			/*	
			std::cout << ref << "\n";
			std::cout << ulr << "\n";	
			std::cout << clr << "\n";
			*/
			
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

}

void performStatistics(std::string mafName)
/* Given a 3-way MAF file between cLR, uLR and ref sequences, perform
 * statistics. */
{
	std::ifstream mafFile (mafName, std::ios::in);
	std::string line = "";

	std::string ref;
	std::string ulr;
	std::string clr;

	// Skip first four lines
	
	for (int i = 0; i < 4; i++) {
		std::getline(mafFile, line); 
	} 


	while (!mafFile.eof()) {
		// Skip first line
		std::getline(mafFile, line);
		
		// Read ref line
		std::getline(mafFile, line);

		if (line != "") {
			ref = split(line).at(6);	
		}

		// Read ulr line
		std::getline(mafFile, line);

		if (line != "") {
			ulr = split(line).at(6);
		}

		// Read clr line
		std::getline(mafFile, line);

		if (line != "") {
			clr = split(line).at(6);	
		}

		// Skip last line
		std::getline(mafFile, line);

		// Do statistics
		// ...
	}
}

int main(int argc, char *argv[])
{
	int opt;

	if (argc == 1) {
		std::cerr << "Please select a mode\n";
		std::cerr << "Usage: " << argv[0] << " [mode] [-m MAF input path] [-c cLR input path] "
		      	  << "[-o MAF output path]\n";
		std::cerr << argv[0] << " maf to create 3-way MAF file\n";
		std::cerr << argv[0] << " stats to perform statistics on MAF file\n";
		return 1;
	} else {

		std::string mode = argv[1];
		
		if (mode != "maf" && mode != "stats") {
			std::cerr << "Please select a mode\n";
			std::cerr << "Usage: " << argv[0] << " [mode] [-m MAF input path] [-c cLR input path] "
		      		  << "[-o MAF output path]\n";
			std::cerr << argv[0] << " maf to create 3-way MAF file\n";
			std::cerr << argv[0] << " stats to perform statistics on MAF file\n";
			return 1;
		}
	}

	std::string mode = argv[1];
	optind = 2;

	// Command line argument handling

	std::string mafInputName = "";
	std::string clrName = "";
	std::string mafOutputName = "output.maf";
	bool isProovread = false;

	while ((opt = getopt(argc, argv, "m:c:o:ph")) != -1) {
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
				mafOutputName = optarg;
				break;
			case 'p':
				isProovread = true;
			case 'h':
				// Displays usage
				std::cout << "Usage: " << argv[0] << " [mode] [-m MAF input path] [-c cLR input path] "
					<< "[-o MAF output path]\n";
				std::cout << argv[0] << " maf to create 3-way MAF file\n";
				std::cout << argv[0] << " stats to perform statistics on MAF file\n";
				return 0;
			default:
				std::cerr << "Usage: " << argv[0] << " [mode] [-m MAF input path] [-c cLR input path] "
					<< "[-o MAF output path]\n";
				return 1;
		}
	}

	bool optionsPresent = true;

	// Pass an error if essential option is not set
	
	if (mafInputName == "") {
		std::cerr << "ERROR: MAF input path required\n";
		optionsPresent = false;
	}
	if (mode == "maf" && clrName == "") {
		std::cerr << "ERROR: cLR input path required\n";
		optionsPresent = false;
	}
	if (!optionsPresent) {
		std::cerr << "Usage: " << argv[0] << " [mode] [-m MAF input path] [-c cLR input path] "
		      	  << "[-o MAF output path]\n";
		return 1;
	}

	if (mode == "maf") {
		generateMaf(mafInputName, clrName, mafOutputName, isProovread);
	} else {
		performStatistics(mafInputName);				
	}
	
	return 0;
}
