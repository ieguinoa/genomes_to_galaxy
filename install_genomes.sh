#!/bin/bash
builds_tab=$1
base_path=$2
symLink=$3

source /home/igegu/miniconda3/bin/activate preprocess_genomes

## preprocess(if not done before) and create the installation .yaml files
python3 /ngsprojects/ngsdb/genomeInformation/test_preprocessing_scripts/preprocess_build_and_install.py -i $builds_tab -b $base_path -s $symLink


# 
for conf_file in find -name '*genomes.yaml' $base_path/ephemeris:
        if symLink == True
            cat $genomes_dm_symlink >> conf_file
        else:
            cat $genomes_dm_nolink >> conf_file
	## install genomes
        run-data-managers --config $conf_file -g $GALAXY_URL -a $API_KEY


for conf_file in find -name '*annotation_and_transcripts.yaml' $base_path/ephemeris:
        ## install annotation and transcripts
        run-data-managers --config $conf_file -g $GALAXY_URL -a $API_KEY

