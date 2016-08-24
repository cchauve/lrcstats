# LRCStats: Long Read Correction Statistics #

## Dependencies ##
* Python 2.7.2
* g++ 5.1.0 (though this should technically work with any g++ version with c++11 support)

## Installation ##
The only component of the pipeline that needs to be compiled is the aligner, which can be done with the following commands:
```
cd src/aligner
make
```
Otherwise, the rest of the pipeline is written in Python so you just need to make sure your version of Python run by the command `python` is Python 2.7.2.

## Usage ##
1. Create your own configuration file with `python lrcstats.py --blank_config [CONFIG NAME]`. The configuration file will appear under `config/[CONFIG NAME].config`.
2. Modify the configuration file to contain the paths to the necessary programs on your system and the details of your experiment.
3. Construct the pipeline scripts with the following command
`
python lrcstats.py --input_config config/[CONFIG NAME].config --experiment_name [EXPERIMENT NAME] --simulate --correct --align --stats
`
4. If you're running LRCStats on a computing cluster with TORQUE and Moab software (which you really should), you can submit all your batch jobs at once using the `quick-qsub` shell scripts under the `scripts/[EXPERIMENT NAME]` directory. Otherwise, you'll have to execute each script as a `bash` script. Run them in the order of:
  1. simulate
  2. correct
  3. align
  4. stats
