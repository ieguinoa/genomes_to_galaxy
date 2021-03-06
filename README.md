# genomes_to_galaxy
Scripts to preprocess genomes+annotation, automatically load them to a Galaxy instance and build the corresponding indexes. This repo also contains yaml files to directly install plants genomes used at PSB-VIB, complementing the genome collection available from PLAZA (https://github.com/ieguinoa/galaxy_data_management)


install_genomes.sh is the wrapper script for all the steps.
The parameters are:

-i Path to genomes table: This is the information about the genomes that need to be installed. It's important to follow the formatting of this table. The columns are:

Species
Strain 
Genome Version        
Annotation version/drescription (can be left blank and it will be labelled as 'reference')
Genome Fasta URL
Annotation (GFF/GTF) URL 

A sample table with some genomes can be found in genomes_sample.tab

-b base_path: This is the path in the local directory where the preprocessing should be done: 

IMPORTANT: the base path must be accessible from the Galaxy server so that all data managers can read the input files created during the preprocessing.

NOT IMPLEMENTED YET
-s Use this parameter (with no value) to run the data managers in link mode. Since the base_path must be accessible from the Galaxy server then it could be better to benefit from it and ask the data managers to only create a symbolic link to the input data. 

NOT IMPLEMENTED YET
-r remote_path (OPTIONAL): This is the remote equivalent in the Galaxy server of the base_path, in case it is mounted in a different base path. Default value is = base_path


-g GALAXY_URL: URL to connect to the Galaxy server. If not set by parameter, it can be set in a global var $GALAXY_URL
-a API_KEY to run data managers. If not set by parameter, it can be set in a global var $API_KEY

## General information about the preprocessing
A genome build is defined by a triad composed of Species+Strain+Version. 
By default, the full GFF and a representative_tx (longest tx only) are installed for each GFF entry/
Several GFF files can be listed in the input file for the same  (e.g subset of genes, extra "low confidence" genes, etc)
As long as the genome build id triad is the same, then the different GFFs will be taken as extra annotations from the same build


For the moment the genomes, annotations and preprocessed files used as input for the data managers are all downloaded to (created in) directories that should be accessible by the Galaxy server. The user can choose to copy or symlinking these input files when running the data managers (parameter -s). 
In the future there will be an extra option that first uploads the files to a history and runs the data managers from these so there will be no need to have the preprocessing files in a Galaxy accessible directory.
