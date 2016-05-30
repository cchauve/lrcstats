std::vector<std::string> &split(const std::string &s, char delim, std::vector<std::string> &elems);

std::vector<std::string> split(const std::string &s, char delim);

struct Reads
{
	std::string readName;
	std::string cAlignment;
	std::string uAlignment;
	std::string refAlignment;
};

class MafFile
{
	public:
		MafFile(std::string fileName);
		void addReads(Reads reads);
	private:
		std::string filename;
};
