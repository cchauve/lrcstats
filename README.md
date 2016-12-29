# LRCStats: Long Read Correction Statistics #
LRCStats is an open-source pipeline for benchmarking DNA long read correction algorithms for long reads outputted by third generation sequencing technology such as machines produced by Pacific Biosciences. The reads produced by third generation sequencing technology, as the name suggests, are longer in length than reads produced by next generation sequencing technologies, such as those produced by Illumina. However, long reads are plagued by high error rates, which can cause issues in downstream analysis. Long read correction algorithms reduce the error rate of long reads either through self-correcting methods or using accurate, short reads outputted by next generation sequencing technologies to correct long reads.

Of course, some long read correction algorithms are better than others, and developers of long read correction algorithms will wish to compare their algorithm with others currently available. LRCStats benchmarks long read correction algorithms using long reads produced by simulators (such as SimLoRD or PBSim) where the two-alignment between the uncorrected long reads (uLR) and the corresponding sequences in the reference genome (ref) is given in a Multiple Alignment Format (MAF) file, and then aligning the corrected long reads (cLR) to the ref-uLR two-way alignments to create three-way alignments using a dynamic programming algorithm. Statistics on these three-way alignments are then collected, such as the overall error rates of the corrected long reads.

## Dependencies ##
* Python 2.7.2
* Any version of g++ with c++11 support

## Installation ##
Clone this repository with the command 
```
git clone --recursive https://github.com/thefantasticdron/lrcstats.git
```

Compile the aligner with the command:
```
./install.sh
```

The rest of the pipeline is written in Python so you just need to make sure your version of Python run by the command `python` is 2.7.2.

## Quick Start ##
1. Create your own configuration file with `python lrcstats.py --blank_config CONFIG_PATH`. The configuration file will be created at the path specified by `CONFIG_PATH`.
2. Modify the configuration file to contain the paths to the cLR FASTA and ref-uLR MAF files along with the directory on your system at which you would like to store the temporary and result files.
3. Construct the LRCStats script with the command `python lrcstats.py CONFIG_FILE OUTPUT_PATH` where `CONFIG_FILE` is the path to your configuration file and `OUTPUT_PATH` is the path at which the LRCStats script will be created.
4. Execute the LRCStats file by either running it as a bash shell script or submitting it to your TORQUE/MOAB compatible computing cluster.

## General usage ##
