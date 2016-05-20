#include <string>

class OptimalAlignment
{
	public:
                OptimalAlignment(std::string uLR, std::string cLR);
                ~OptimalAlignment();
                std::string getAlignment();
                int getDistance();
		void printMatrix();
        private:
                std::string uLR;
                std::string cLR;
		int rows;
		int columns;
                int**  memo;
                std::string alignment;
                int distance;
                int findDistance(int cIndex, int uIndex);
};
