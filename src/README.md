# `src` #

This directory contains the meat of the LRCstats pipeline. Except for the `preprocessing` subdirectory, in general it would be wise of you to not modify the contents of `src` (unless you really want to tweak the LRCstats pipeline).

## Directory Information ##

* `aligner` contains the C++ source code for the dynamic programming algorithm for aligning corrected long reads onto Ref-uLR two-way alignments.
* `preprocessing` contains scripts for the preprocessing stage of the LRCstats pipeline. Users may find scripts in this directory useful for their own purposes.
* `sanity_checks` contains Python scripts for detailing and comparing the characteristics of both empirical and simulated short and long reads. The files in this directory are not used in the main LRCstats pipeline and are left here for users who may find them useful.
* `statistics` contains Python scripts for generating statistics for the three-way alignments constructed by the dynamic programming algorithm contained in `aligner`.
