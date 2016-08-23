# Long Read Correction Statistics #

## Manual ##
### Dependencies ###
* Python 2.7.2
* g++ 5.1.0 (though this should technically work with any g++ version with c++11 support)

### Installation ###
```bash
cd src/collection
make
```
### Usage ###
1. Create your own configuration file with `python lrcstats.py --blank_config [CONFIG NAME HERE]`. The configuration file will appear under at `config/[CONFIG NAME HERE].config`.
2. Modify the configuration file to contain the paths to the necessary programs on your system and the details of your experiment.
3. Construct the pipelie scripts with the following commands. They will appear under the directory `scripts`.
```bash
python lrcstats.py -i config/[CONFIG NAME HERE].config -n [NAME OF THE EXPERIMENT] --simulate --correct --align --stats
```
4. Run the pipeline by submitting the scripts under `scripts/[NAME OF THE EXPERIMENT]` to your cluster in the order of
..
