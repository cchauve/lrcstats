#!/bin/bash

while IFS='' read -r line || [[ -n "$line" ]]; do
	echo "Beginning retrieval of file $line"
	/global/scratch/seanla/sratoolkit.2.6.2-ubuntu64/bin/fastq-dump --outdir /global/scratch/seanla/Data/peru/ --gzip $line
	echo "Finished retrieving file $line"	
done < "$1"
