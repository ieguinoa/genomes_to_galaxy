## 
import gffutils
import sys
import os
import tempfile
import optparse
import subprocess



tx_features_names=['mRNA','transcript','lincRNA','snoRNA','tRNA','snRNA','SRP_RNA','lnc_RNA','miRNA','rRNA','ncRNA','ncRNA_gene','pre_miRNA','RNase_MRP_RNA']
gene_features_names=['gene','tRNA_gene','ncRNA_gene','lincRNA_gene','miRNA_gene']


def get_longest_transcripts_only():
    #out_gff = open(sys.argv[2], 'w')
    db = gffutils.create_db(sys.argv[1], 'test.db',merge_strategy="create_unique", force=True)
    
    db = gffutils.FeatureDB('test.db', keep_order=True)
    
    # iterate over all features
    for gene in db.features_of_type(gene_features_names):
         gene_id=gene.attributes['ID']
         gene.attributes['gene_id']=gene_id
         #del feature['ID']
         # iterate over childs to add gene_id
         #if len(db.children(gene, featuretype='mRNA', order_by='start')) > 1:
         #    print ('MULTIPLE TRANSCRIPTS')
         longest_RNA='None'
         max_length=0
         #longest_mRNA=0
         for RNA in db.children(gene, featuretype=tx_features_names):
                 rna_length=RNA.end - RNA.start
                 if rna_length > max_length:
                      longest_RNA=RNA
                      max_length=rna_length 
         # now process the longest mRNA     
         # it could happen that gene is used to define structures other than the classic gene-mRNA-exons. For example  gene-tRNAs
         # in this case the previous loop wont catch any longest mRNA (the gene has no mRNA childs)   
         if longest_RNA != 'None':
    	     print(gene)  # print the feature with the modified values
    	     longest_RNA.attributes['gene_id']=gene_id
    	     print(longest_RNA)
    	     for exon in db.children(longest_RNA, featuretype='exon', order_by='start'):  
    			 exon.attributes['gene_id']=gene_id
    			 print(exon)
         #else:
         #    print gene_id[0] + '\tNo RNA found'



def get_tx2gen_table(gff_file,filename):
    out_file = open(filename, 'w')
    db = gffutils.create_db(gff_file, 'test.db', force=True, merge_strategy='create_unique')
    db = gffutils.FeatureDB('test.db', keep_order=True)
    for gene in db.features_of_type(gene_features_names):
        for child in db.children(gene, order_by='start'):
#           if child.featuretype=='mRNA' or child.featuretype=='rRNA' or child.featuretype=='lnc_RNA':
	    if child.featuretype in tx_features_names:
            	out_file.write(child.id + '\t' + gene.id + '\n')



def main():
    parser = optparse.OptionParser()
    #parser.add_option( '-d', '--out_dir', dest='out_dir', action='store', type="string", default=None )
    parser.add_option( '-o', '--out_file', dest='out_file', action='store', type="string", default=None )
    parser.add_option( '-f', '--gff_file', dest='gff_file', action='store', type="string", default=None )
    (options, args) = parser.parse_args()

    #gff_file=options.gff_file
    #samples=options.samples_list

    #create tmp file to save tx-gene table

    #tmp_dir = tempfile.mkdtemp( prefix='tmp-gene-tx-table' )

    #gene_tx_table = os.path.join( options.out_dir, 'tx2gene_table' )

    get_tx2gen_table(options.gff_file, options.out_file)


if __name__ == "__main__":
    main()



