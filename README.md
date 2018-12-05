# genomes_to_galaxy
Scripts to preprocess genomes+annotation, automatically load them to a Galaxy instance and build the corresponding indexes. This repo also contains yaml files to directly install plants genomes used at PSB-VIB, complementing the genome collection available from PLAZA (https://github.com/ieguinoa/galaxy_data_management)



Genome_build_abbreviation
GFF description
Species
Strain / Accession / Cultivar 
Source 
Version        
Info URL
FASTA URL
GFF URL  



A genome build is defined by a triad composed of Species+Strain+Version  
By default, the full GFF and a representative_tx (longest tx only) are installed for each GFF entry/
Several GFF files can be listed in the input file for the same  (e.g subset of genes, extra "low confidence" genes, etc)
As long as the genome build id triad is the same, then the different GFFs will be taken as extra annotations from the same build


For the moment the genomes, annotations and preprocessed files used as input for the data managers are all downloaded to (created in) directories that should be accessible by the Galaxy server. The user can choose to copy or symlinking these input files when running the data managers (parameter -s). 
In the future there will be an extra option that first uploads the files to a history and runs the data managers from these so there will be no need to have the preprocessing files in a Galaxy accessible directory.
