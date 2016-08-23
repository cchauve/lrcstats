# LRCStats: Long Read Correction Statistics #

### Dependencies ###
* Python 2.7.2
* g++ 5.1.0 (though this should technically work with any g++ version with c++11 support)
### Installation ###
```
cd src/collection
make
```
### Usage ###
1. Create your own configuration file with `python lrcstats.py --blank_config [CONFIG NAME HERE]`. The configuration file will appear under `config/[CONFIG NAME HERE].config`.
2. Modify the configuration file to contain the paths to the necessary programs on your system and the details of your experiment.
3. Construct the pipelie scripts with the following command. They will appear under the directory `scripts`.
```
python lrcstats.py -i config/[CONFIG NAME HERE].config -n [NAME OF THE EXPERIMENT] --simulate --correct --align --stats
```
4. Run the pipeline by running the scripts in the directory `scripts/[NAME OF THE EXPERIMENT]` in the following order: 
  1. simulate
  2. correct
  3. align
  4. stats
