#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <unistd.h>
#include <getopt.h>

#include "data/data.hpp"
#include "alignments/alignments.hpp"
#include "measures/measures.hpp"

int main(int argc, char *argv[])
{
	std::string mafInputName = "";
	std::string clrName = "";
	std::string mafOutputName = "";

	// Command line argument handling
	int opt;

	while ((opt = getopt(argc, argv, "m:c:o:")) != -1) {
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
			default:
				std::cerr << "Usage: " << argv[0] << " [-m MAF input path] [-c cLR input path] "
					<< "[-o MAF output path]\n";
				return 1;
		}
	}

	bool optionsPresent = true;

	// Pass an error if any option is not set

	if (mafInputName == "") {
		std::cerr << "ERROR: MAF input path required\n";
		optionsPresent = false;
	}
	if (clrName == "") {
		std::cerr << "ERROR: cLR input path required\n";
		optionsPresent = false;
	}
	if (mafOutputName == "") {
		std::cerr << "ERROR: MAF output path required\n";
		optionsPresent = false;
	}

	if (!optionsPresent) {
		return 1;
	}
	
	std::ifstream mafInput (mafInputName, std::ios::in);
	std::ifstream clrInput (clrName, std::ios::in);
	MafFile mafOutput (mafOutputName);

	if (!mafInput.is_open() || !clrInput.is_open()) {
		std::cerr << "Unable to open either maf input or corrected long reads file\n";
		return 1;
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

	Alignments alignments(ref, ulr, clr);
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
			
				// Do statistics
				std::cout << "Edit score for ulr == " << editScore(alignments.getRef(), alignments.getUlr()) << "\n";
				std::cout << "Edit score for clr == " << editScore(alignments.getRef(), alignments.getClr()) << "\n";
			}	

		}

		clr = "";
	}

	mafInput.close();
	clrInput.close();
	return 0;
}
