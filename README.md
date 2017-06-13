# LRCstats: Long Read Correction Statistics #

## Description ##
LRCstats is an open-source pipeline for benchmarking DNA long read correction algorithms for long reads outputted by third generation sequencing technology such as machines produced by Pacific Biosciences. The reads produced by third generation sequencing technology, as the name suggests, are longer in length than reads produced by next generation sequencing technologies, such as those produced by Illumina. However, long reads are plagued by high error rates, which can cause issues in downstream analysis. Long read correction algorithms reduce the error rate of long reads either through self-correcting methods or using accurate, short reads outputted by next generation sequencing technologies to correct long reads.

Of course, some long read correction algorithms are better than others, and developers of long read correction algorithms will wish to compare their algorithm with others currently available. LRCstats benchmarks long read correction algorithms using long reads produced by simulators (such as SimLoRD or PBSim) where the two-way alignments between the uncorrected long reads (uLR) and the corresponding sequences in the reference genome (Ref) are given in some sort of alignment file and then aligning the corrected long reads (cLR) to the Ref-uLR two-way alignments to create three-way alignments using a dynamic programming algorithm. Statistics on these three-way alignments are then collected, such as the overall error rates of the corrected long reads.

## Dependencies ##
* Python 2.7.2
* Any version of g++ with c++11 support

## Installation ##
Clone this repository with the command 
```
git clone --recursive https://github.com/cchauve/lrcstats.git
```

Compile the aligner with the command:
```
./install.sh
```

The rest of the pipeline is written in Python so you just need to make sure your version of Python run by the command `python` is 2.7.2.

## Usage ##
1. Create your own configuration file with `python lrcstats.py --blank_config CONFIG_PATH`. The configuration file will be created at the path specified by `CONFIG_PATH`.
2. Modify the configuration file to contain the paths to the cLR FASTA and Ref-uLR SAM files along with the directory on your system at which you would like to store the temporary and result files.
3. Construct the LRCstats script with the command `python lrcstats.py -i CONFIG_FILE -o OUTPUT_PATH` where `CONFIG_FILE` is the path to your configuration file and `OUTPUT_PATH` is the path at which the LRCstats script will be created.
4. Execute the LRCstats benchmarking pipeline by either running it as a bash shell script or submitting it as a job to your TORQUE/MOAB compatible computing cluster.

## Input ##
The three main files that LRCstats takes as input are:

1. a corrected simulated long reads file in FASTA format
2. a Ref-uLR two-way alignment file in SAM format
3. the reference genome from which the simulated long reads were generated from

The paths to these files can be provided in either a configuration file or as command line arguments.

If the corrected long reads file is given as a FASTQ file instead, the LRCstats repo includes a python script `src/preprocessing/fastq2fasta/fastq2fasta.py` to convert FASTQ files into FASTA format. 

The LRCstats pipeline internally identifies individual simulated long reads by the first contiguous sequence of integers in the header line of the FASTA file using a regular expression. For example, given the long read in FASTA format:
```
>Read_0001_simulated
ATCG
```
LRCstats will identify this long read by the sequence of characters `0001`. SimLoRD outputs the headers of the long reads in this style, although other simulators may not (in particular, PBSim does not).

If the correction algorithm outputs reads in "trimmed" format (i.e. outputs only the corrected segments of the long read) in such a way that each corrected segment has its own entry in the FASTA/Q file, LRCstats assumes three things:

1. The corrected long reads are in sorted order in the FASTA/Q file.
2. If multiple corrected reads originate from the same uncorrected read (i.e. they are corrected segments of the uncorrected read), then the first contiguous sequence of integers in the header line are identical over all these reads
3. Suppose reads 1, ..., k are corrected segments originating from the same uncorrected read and are given in this order in the FASTA/Q file. Then read 1 is to the left of read 2, read 2 to the left of read 3, etc.

To give an explicit example, consider the uncorrected read sequence `AAAACTTTTCGGGG` and it's corresponding FASTA file containing three corrected segments originating from the same uncorrected read:

```
>Read_0001.1_simulated
AAAA
>Read_0001.2_simulated
TTTT
>Read_0001.3_simulated
GGGG
```

Notice that the first contiguous segment of integers in the header are identical over the three reads (i.e. `0001`). Furthermore, the corrected segments appear in the same order in the FASTA file as it appears in the uncorrected read. Jabba and proovread output their corrected reads in this format.

SimLoRD outputs the alignment between the uncorrected long reads and the reference sequence in SAM format. Simply plug the path of this file into your LRCstats configuration file. If your simulator doesn't output the alignments between the uLRs and the reference genome in SAM format, you'll have to do your own preprocessing.

The directory `scripts` contains example scripts for simulating short and long reads using SimLoRD and correcting simulated long reads using simulated short reads with proovread, LoRDEC, Jabba and CoLoRMap.

## Configuration File ##
LRCstats takes as input a configuration file specifying

1. Experiment Details - the details of the experiment
2. Paths - paths to files and directories on the user's machine
3. Initalization Commands - commands to be initialized prior to the start of the pipeline (optional)
4. PBS Parameters - parameters to include in the header of the script outputted by LRCstats (optional)

Details of the experiment (1) and paths on the user's machine (2) can also be provided as command line arguments. However, initialization commands (3) and PBS parameters (4) must be provided in a configuration file if the user wishes to include them in the output script.

### Experiment Details ###

* `experiment_name` name of experiment
* `threads` number of threads to be provided to the dynamic programming alignment program
* `trimmed` whether the corrected long reads are trimmed
* `extended` whether the corrected long reads are extended
* `id_pos` the position in the Read ID that corresponds to the unique Read ID.

To clarify what the `id_pos` of a read is, consider the read name 'SRR1284073.32'. This indicates that the read is the 32nd read of SRR1284073. Then the unique read ID position is 1, because we can sort the reads based on the the second set of contiguous numbers in the read ID. For SimLoRD-simulated reads, the `id_pos` is 0. 

### Paths ###

* `data` the directory where the user wishes to store the files created by the LRCstats pipeline, such as temporary files and the result file
* `clr` the path to the corrected long read FASTA file
* `sam` the path to the Ref-uLR two-way alignment SAM file
* `ref` the path to the reference genome FASTA file

### Initialization Commands (Optional) ###

Commands specified here could be those that load the dependencies onto the user's environment, such as
* `module load python2.7`
* `module load g++/5.1.0`

### PBS Parameters (Optional) ###

The user may specify the PBS parameters that will appear in the header of the script if the user wishes to run the pipeline as a PBS job. Parameters may include the walltime limit, memory limit and the number of processors allocated to the job. Note that the number of cores specified in the PBS parameter list should be identical to the number of threads specified under the "Experiment Details" section.

## Output ##

`lrcstats.py` outputs a script that can be run as either a bash script or submitted to a Moab/TORQUE compatible computing cluster. This script performs the following steps:

1. Converts the SAM alignment file into a Ref-uLR two-way alignment file.
2. Sorts the cLR FASTA file and removes Ref-uLR alignments in the MAF file that do not appear in the cLR FASTA file
3. Constructs the three-way alignments between the corrected long reads, uncorrected long reads and the reference sequences
4. Produces statistics on the three-way alignments

If `data` is the user-specified output directory and `experiment-name` is the name of the experiment, the correction statistics can be found at `data/experiment-name_results.tsv`.

## Directory Structure ##

* `scripts` contains example scripts for the simulation of short and long reads and the correction of long reads.
* `src` contains source code and Python scripts for LRCstats pipeline. Users may find scripts in here useful.
* `tests` contains scripts for unit tests for LRCstats.

## Other Remarks ##

### Failed Alignments ###
In some cases, LRCstats may fail to align untrimmed corrected long reads back to the Ref-uLR alignment. This occurs when there exists an uncorrected segment in the corrected long read which is not completely identical to the corresponding segment in the uncorrected long read. Occurrences of these non-identical uncorrected segments in corrected long reads are the fault of the correction algorithm, so we do not include these faulty reads into the statistics calculations.

### X delimiters in the MAF alignments ###
We modified the multiple alignment format to include `X` delimiters that indicate the boundaries of corrected segments in both trimmed and untrimmed corrected long read alignments. Hence, our version of the multiple alignment format may not be compatible with programs which accept MAF files as input.

## Contact ##
If you have any questions or comments, please submit a GitHub issue or send an email to Sean La at laseanl[at]sfu[dot]ca
