# LRCStats: Long Read Correction Statistics #

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
1. Create your own configuration file with `python lrcstats.py --blank_config CONFIG_PATH`. The configuration file will be created at the path `CONFIG_PATH`.
2. Modify the configuration file to contain the paths to the cLR FASTA and ref-uLR MAF files along with the directory on your system at which you would like to store the temporary and result files.
3. Construct the LRCStats script with the command `python lrcstats.py CONFIG_FILE OUTPUT_PATH` where `CONFIG_FILE` is the path to your configuration file and `OUTPUT_PATH` is the path at which the LRCStats script will be created.
4. Execute the LRCStats file by either running it as a bash shell script or submitting it to your TORQUE/MOAB compatible computing cluster.
