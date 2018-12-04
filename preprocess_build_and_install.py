import urllib.request
import sys
from urllib.parse import urlparse
import os
import gff_processing
import subprocess

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
    genome_builds_file=open(sys.argv[1])
    base_build_path=sys.argv[2]
    
    
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
    
    
    for line in genome_builds_file.readlines():
        build_abbv,gff_desc,species,strain,source,version,info_url,fasta_uri,gff_uri=line.split('\t')
        build_id=sanitize_name(species+'_'+strain+'_'+version)
        if build_id not in builds_gff_dict:
            builds_gff_dict[]
            build_dir=os.path.join(base_path,build_id)
            os.mkdir(build_dir)
            out_genome_fasta=os.path.join(build_dir,build_id.genome.fa)
            if not get_file(fasta_uri,out_genome_fasta):  
                return 'The genome file could not be found'
            ## ****** samtools faidx $genome_file
            #print the genome entry in the corresponding .yaml file
            
        # Retrieve GFF
        if (gff_desc!=''):
            gff_id=build_id+'_'+sanitize_name(gff_desc) 
        else:
            gff_id=build_id+'_main_gff'
        out_gff_path=os.path.join(build_dir,gff_id+'.gff')    
        if not get_file(gff_uri,out_gff_path):
            return 'The gff file could not be found'  
    
    
    
        ## Start preprocessing
        # Get the transcriptome
        print("------------------------")
        print("Creating transcriptome fasta file")
        #print("gffread -g %s -w $exome_out %s",out_genome)
        args = [ 'gffread','-g',out_genome_fasta,'-w', transcriptome_out ]
        proc = subprocess.Popen( args=args, shell=False)
        return_code = proc.wait()
        if return_code:
            print("Error building transcriptome", file=sys.stderr)
            sys.exit( return_code )
    
    
        # Get tx2gene and representative_tx_gff
        print("------------------------")
        print("Processing the annotation file: extracting representativve (longest) transcript per gene and transcript to to gene table:")
        process_gff_function(out_gff_path, tx2gene_out_path, longest_tx_out_path)
    
        
        #print the gff entry and the transcriptome entry in the corresponding .yaml files
        
   
  


    



if __name__ == "__main__":
    main()
    
