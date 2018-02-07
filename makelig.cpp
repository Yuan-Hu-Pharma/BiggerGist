#include <iostream>
#include <fstream>
#include <stdlib.h>
#include <stdio.h>
#include <string>
#include <string.h>
#include <vector>
#include <sstream>

/*
void dx::printPdb(string outfile) {
double vals[3];
int pos = 0;
FILE * pFile;
pFile = fopen(outfile.c_str(), "w");
//Define the pdb file stuff
string name = "ATOM"; string atom = "H"; string resname = "T3P"; string chainid = "C"; int resseq = 1; double occupancy = 0.0; double T = 0.0;
for (int i = 0; i < count[0]; i++) {
for (int j = 0; j < count[1]; j++) {
for (int k = 0; k < count[2]; k++) {
vals[0] = i*delta[0] + origin[0];
vals[1] = j*delta[1] + origin[1];
vals[2] = k*delta[2] + origin[2];
fprintf (pFile, "%-6s%5i %-4s %3s %1s%4i    %8.3f%8.3f%8.3f%6.2f%6.2f\n", name.c_str(), pos, atom.c_str(), resname.c_str(), chainid.c_str(), resseq, vals[0], vals[1], vals[2], data[pos], T);
//pos++;
}
}
}

}



*/

/*
	Simple code intended to take the gridcen values either from a gist.in input file
		or directly via command line arguments

		Will then output a ligand.pdb structure file (name specified by command line) with an atom of those coordinates

	This will allow the BiggerGist framework to be used by SSTMap, without use of the SSTMap api

*/


std::vector<std::string> splitString(const std::string& s, char delimiter) {
	/*
		General line splitting function stolen from: https://www.fluentcpp.com/2017/04/21/how-to-split-a-string-in-c/
		Will take a string and a delimiter and return a vector of the splits
	*/
	std::vector<std::string> command;
	std::string commandString;
	std::istringstream commandStream(s);
	while (std::getline(commandStream, commandString, delimiter)) {
		command.push_back(commandString);
	}
	return command;
}

void printPdb(double x, double y, double z, std::string out) {
	//Simple printPdb function that will print a pdb structure file for a carbon atom at position
	 // x y z into file out
	//std::cout << "Start print method\n";
	FILE * pFile;
	pFile = fopen(out.c_str(), "w");
	std::string name = "ATOM";
	int pos = 1;
	std::string atom = "C";
	std::string resname = "PLA";
	std::string chainid = "A";
	int resseq = 1;
	double empty = 0.0;
	//Next line seg faults... wasn't able to figure it out, recopied and works with predefined values.
	//fprintf(pFile, "%-6s%5i %-4s %3s %1s%4i    %8.3f%8.3f%8.3f%6.2f%6.2f\n", "ATOM", '1', "C", "PLA", 'A', 1, x, y, z, 0.0, 0.0);
	fprintf(pFile, "%-6s%5i %-4s %3s %1s%4i    %8.3f%8.3f%8.3f%6.2f%6.2f\n", name.c_str(), pos, atom.c_str(), resname.c_str(), chainid.c_str(), resseq, x, y, z, empty, empty);
	fclose(pFile);
	//std::cout << "End print method\n";
	return;
}

int main(int argc, char** argv) {

	std::string infile = "gist.in"; //default infile name
	std::string ligandoutfile = "ligand.pdb";
	double gridcenx = -100.0; //arbitrary negative number for later checks
	double gridceny = -100.0;
	double gridcenz = -100.0;
	bool xprov = false; bool yprov = false; bool zprov = false; //did not provide coordinates in commands
	bool inprov = false;
	int k = 0; //count of arguments
	if (argc <= 1) {
		std::cout << "No options specified, defaults will be used\n";
			
	}
	else {
		//std::cout << "Start processing arguments\n";
		while (k < argc) { //loop through arguments
			if (!strcmp(argv[k], "-i")) {
				infile = argv[++k];
				inprov = true;
			}
			else if (!strcmp(argv[k], "-x")) {
				gridcenx = atof(argv[++k]);
				xprov = true;
			}
			else if (!strcmp(argv[k], "-y")) {
				gridceny = atof(argv[++k]);
				yprov = true;
			}
			else if (!strcmp(argv[k], "-z")) {
				gridcenz = atof(argv[++k]);
				zprov = true;
			}
			else if (!strcmp(argv[k], "-o")) {
				ligandoutfile = argv[++k];
			}
			k++;
		}
		//std::cout << "Done processing arguments\n";
	}

	//Check commands given 
	if (!inprov) {
		if (!xprov && yprov && zprov) {
			std::cout << "Must provide all three coordinates of desired carbon atom with -x -y -z\n";
			exit(0);
		}
	}

	std::cout << "Gist input: " << infile << std::endl
		<< "Ligand output: " << ligandoutfile << std::endl;

	std::ifstream input(infile.c_str());
	std::string temp;
	while (!input.eof()) {
		//std::cout << "Start looping through infile\n";
		getline(input, temp);
		if (!temp.empty()) {
			if (!strcmp(temp.substr(0, 4).c_str(), "gist")) { //only need to process gist command
				std::vector<std::string> splitCommand = splitString(temp, ' ');
				//std::cout << "Split string with gist command\n";
				int commandLength = splitCommand.size();
				for (int i = 0; i < commandLength; i++) {
					if (!strcmp(splitCommand[i].c_str(), "gridcntr")) {
						gridcenx = atof(splitCommand[i + 1].c_str());
						gridceny = atof(splitCommand[i + 2].c_str());
						gridcenz = atof(splitCommand[i + 3].c_str());
					}
				}
				//std::cout << "Set new coordinates\n";
			}
		}
		else {
			continue;
		}
	}

	printPdb(gridcenx, gridceny, gridcenz, ligandoutfile);
	std::cout << "Carbon atom written at desired coordinates\n" <<
		gridcenx << " " << gridceny << " " << gridcenz << std::endl
		<< "Into file: " << ligandoutfile << std::endl << std::endl;

	return 0;
}