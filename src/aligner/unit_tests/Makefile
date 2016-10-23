all: build

build:
	g++ -std=c++11 -o unit_tests_aligner catch_config_main.cpp test_alignments.cpp test_measures.cpp test_data.cpp ../alignments.cpp ../data.cpp ../measures.cpp

clean:
	rm *.o unit_tests_aligner
