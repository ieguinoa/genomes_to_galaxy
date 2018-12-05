import urllib.request
import sys
from urllib.parse import urlparse
import os
import gff_processing
import subprocess
import download_files


def uri_validator(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc, result.path])
    except:
        return False




def _stream_to_file(file_stream, target_filename, sequence_id, close_stream=True):
    with open(target_filename, 'wb+') as file_writer:
            while True:
                data = fasta_stream.read(CHUNK_SIZE)
                if data:
                    file_writer.write(data)
                else:
                    break
            if close_stream:
                file_stream.close()


# just get the file
# TODO: make a nice output, progress bar, etc
def get_file(uri, out_path):
   tmp_dir = tempfile.mkdtemp()   #create tmp file in case the genome needs to be uncompressed
   if(uri_validator(uri)):  # its a URL
        print(uri_validator(uri))
        #urllib.request.urlretrieve(uri, out_path)
        file_stream=get_stream_reader(urlopen(url), tmp_dir)
        _stream_to_file(file_stream,out_path,sequence_id=sequence_id)
    else:
        # it may be a file path
        if (os.path.exists(uri)): 
            ## its a file path
            #assume it is not compressed and just make a ln
            os.symlink(out_path,uri) 
            # i can also make a stream to the new location
            #file_stream=get_stream_reader(open(filename, 'rb'), tmp_dir)
        else:
            return False
    if tmp_dir and os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)  



def sanitize_names(name_raw):
    return name_raw.replace(' ','_').replace('(','_').replace(')','_').replace(',','_')










def main():
    # Parse Command Line
    wparser = argparse.ArgumentParser()
    parser.add_argument( '-i','--genomes_input', dest='genomes_table', action='store', type=str, default=None )
    parser.add_argument( '-b', '--base_dir', dest='base_dir', action='store', type=str, help='base dir to save genomes and processed files' )
    parser.add_argument( '-s', '--use_symlink', dest='use_symlink', action='store', type=str,default=True, help='Boolean, whether to symlink the files to Galaxy dm-dir or make a copy' )
    options = parser.parse_args()

    base_dir = options.base_dir
    genomes_table_path=options.genomes_table 
    #open the table file
    genomes_table_file=open(genomes_table_path)
    
    #create yaml files to print entries 
    #genome entries, creates dbkey, load genome and index based on genome only
    genomes_yaml=open(os.path.join(base_dir,'genomes.yaml'),'w')    #Fields: dbkey, genome_id (fasta entry), fasta_path
    transcripts_yaml=open(os.path.join(base_dir,'transcripts.yaml'),'w') #Fields: dbkey, transcriptome_id, transcriptome_name, transcripts_path
    annotation_yaml=open(os.path.join(base_dir,'annotations.yaml'),'w') # Fields: dbkey, annotation_id, annotation_name, annotation_path
        
    genomes_list=[]
    gff_transcriptome_list=[]
    
    #skip header
    genome_builds_file.readline()
    
    # Columns in the file must be (see README):
    # Genome_build_abbreviation
    # GFF description (optional)
    # Species
    # Strain / Accession / Cultivar	
    #Source	
    #Version	
    #Info URL
    #FASTA URL
    #GFF URL	
    
    
    
    ## builds dictionary
    builds_gff_dict={}
    
    
    for line in genomes_table_file.readlines():
        build_abbv,gff_desc,species,strain,source,version,info_url,fasta_uri,gff_uri=line.split('\t')
	build_name=species+' '+strain+' '+version)
        build_id=sanitize_name(build_name)
        if build_id not in builds_gff_dict:   ## genome not yet included
            builds_gff_dict[build_id]=[]   # add the build_id key
            build_dir=os.path.join(base_dir,build_id)
            os.mkdir(build_dir)
            gid=build_id+ '_genome'  # id of genome sequence
            out_genome_fasta=os.path.join(build_dir,gid+'.fa')
            ## check that the file does not exists (assume that if exists then it is the same )
            if not os.path.isfile(out_genome_fasta):
                if not get_file(fasta_uri,out_genome_fasta):  
                    return 'The genome file could not be found'
                 ## Index the genome fasta: required to get the transcriptome
                 ## ****** samtools faidx $genome_file
                 args = [ 'samtools','faidx',out_genome_fasta]
                 proc = subprocess.Popen( args=args, shell=False)
                 return_code = proc.wait()
                 if return_code:
                     print("Error building genome index", file=sys.stderr)
                     sys.exit( return_code )

            #add the genome entry in the corresponding list to create the .yaml file
            genomes_list.append( { \
                'dbkey': build_id,\
                'genome_id': gid,\
                'name': build_name,\
                'genome_uri': out_genome_fasta,\
                } )
            
        # Retrieve GFF
        if (gff_desc!=''):
            gff_id=build_id+'_'+sanitize_name(gff_desc) 
        else:
            gff_id=build_id+'_main_gff'
        if gff_id not in builds_gff_dict[build_id]:   # new annotation for this build, add it to the list and continue with processing
            builds_gff_dict[build_id].append(gff_id) 
            out_gff_path=os.path.join(build_dir,gff_id+'.gff')    
            if not os.path.isfile(out_gff_path): ## check that the file does not exists (assume that if exists then it is the same )
                if not get_file(gff_uri,out_gff_path):
                    return 'The gff file could not be downloaded/copied' 
                else:
                    print("The GFF was already located in the correct place, no download/linking required")
    
    
    
            ## Start preprocessing
            # Get the transcriptome
            transcriptome_out=os.path.join(build_dir,gff_id+'_transcripts.fa')
            if not os.path.isfile(transcriptome_out): ## check that the file does not exists (assume that if exists then it is the same )
                print("------------------------")
                print("Creating transcriptome fasta file")
                #print("gffread -g %s -w $exome_out %s",out_genome)
                args = [ 'gffread','-g',out_genome_fasta,'-w', transcriptome_out ]
                proc = subprocess.Popen( args=args, shell=False)
                return_code = proc.wait()
                if return_code:
                    print("Error extracting transcript sequences", file=sys.stderr)
                    sys.exit( return_code )
        
        
            # Get tx2gene and representative_tx_gff
            tx2gene_out_path=os.path.join(build_dir,gff_id+'_tx2gene.tab')
            longest_tx_out_path=os.path.join(build_dir,gff_id+'_longest_tx.gff')
            if (not os.path.isfile(transcriptome_out)) or (not os.path.isfile(transcriptome_out)): ## check of any of the file does not exists (assume that if exists then it is the same )
                print("------------------------")
                print("Processing the annotation file: extracting representativve (longest) transcript per gene and transcript to to gene table:")
                #process_gff_function(out_gff_path, tx2gene_out_path, longest_tx_out_path)
        
            
            #add the gff+transcriptome entry in the list to create .yaml files
            gff_transcriptome_list.append( { \
                    'dbkey': build_id,\
                    'genome_id': gid,\
                    'name': build_name,\
                    'genome_uri': out_genome_fasta,\
                    } )

        else:    ## gff id is already stored in the build lists -> duplicated entry in the input table
            print("Duplicated GFF description")
  


    



if __name__ == "__main__":
    main()
    
