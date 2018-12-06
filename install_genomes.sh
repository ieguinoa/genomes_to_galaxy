#!/bin/bash


genomes_dm_symlink=genomes_dm_symlink.yaml
genomes_dm_cp=genomes_dm_cp.yaml

annotation_dm_symlink=annotation_dm_symlink.yaml
annotation_dm_copy=annotation_dm_cp.yaml


PARAMS=""
symLink=false

while (( "$#" )); do
  case "$1" in
    -a|--api-key)
      API_KEY=$2
      shift 2
      ;;
    -g|--galaxy-server)
      GALAXY_SERVER=$2
      shift 2
      ;;
    -i|--builds-table)
      PARAMS="$PARAMS -i $2"
      shift 2
      ;;
    -b|--base-path)
      PARAMS="$PARAMS -b $2"
      base_path=$2
      shift 2
      ;;
    -s)
      symLink=true
      shift
      ;;
    --) # end argument parsing
      shift
      break
      ;;
    -*|--*=) # unsupported flags
      echo "Error: Unsupported flag $1" >&2
      exit 1
      ;;
    *) # preserve positional arguments
      PARAMS="$PARAMS $1"
      shift
      ;;
  esac
done



## preprocess(if not done before) and create the installation .yaml files
#python3 /ngsprojects/ngsdb/genomeInformation/test_preprocessing_scripts/preprocess_build_and_install.py -i $builds_tab -b $base_path -s $symLink




### Install the resulting files

conf_files_dir=$base_path/ephemeris
for conf_file in `find $conf_files_dir -name "*genomes.yaml" -type f`; do  
    if [ "$symLink" == true ]
    then
        echo "symblinking...."
        cat $genomes_dm_symlink >> conf_file
    else
        echo "not symlinking"
        cat $genomes_dm_cp >> conf_file
    fi 
    # install genomes
    #run-data-managers --config $conf_file -g $GALAXY_URL -a $API_KEY
done



for conf_file in `find $conf_files_dir -name "*annotation_and_transcripts.yaml" -type f`; do
    if [ "$symLink" == true ]
    then
        echo "symblinking...."
        cat $annotation_dm_symlink >> conf_file
    else
        echo "not symlinking"
        cat $annotation_dm_cp >> conf_file
    fi
    # install genomes
    #run-data-managers --config $conf_file -g $GALAXY_URL -a $API_KEY
done



