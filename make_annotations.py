##
## Driver script for making all annotations v2.0
##
import os
import sys
import glob
import time
import zipfile
from time import strftime, localtime

import rnaseqlib
import rnaseqlib.utils as utils
import rnaseqlib.gff.gffutils_helpers as gffutils_helpers

# Annotations version
VERSION = "v2"

def zip_annotations(events_dir, genomes, 
                    flanking="commonshortest"):
    """
    Create zip archives of annotations.
    """
    log_fname = os.path.join(events_dir, "log.txt")
    timestamp = strftime("%Y-%m-%d %H:%M:%S", localtime())
    log_file = open(log_fname, "w")
    log_file.write("#GFF3 annotations of alternative events for MISO\n" \
                   "#created: %s\n" %(timestamp))
    log_file.write("#version: %s\n" %(VERSION))
    log_file.close()
    for genome in genomes:
        zip_fname = \
            os.path.join(events_dir,
                         "miso_annotations_%s_%s.zip" %(genome, VERSION))
        if os.path.isfile(zip_fname):
            print "Removing old zip file..."
            os.unlink(zip_fname)
        print "Zipping annotations for %s into %s" %(genome,
                                                     zip_fname)
        annotation_fnames = \
            glob.glob(os.path.join(events_dir, genome, flanking,
                                   "*.gff3"))
        files_to_zip = [log_fname] + annotation_fnames
        print "  - Files to zip: ", files_to_zip
        zip_file = zipfile.ZipFile(zip_fname, "w")
        for fname_to_zip in files_to_zip:
            zip_file.write(fname_to_zip,
                           arcname=os.path.join(genome,
                                                os.path.basename(fname_to_zip)))


def upload_annotations(events_dir, genomes):
    """
    Upload annotations to Argonaute.

    Send to:

    http://genes.mit.edu/burgelab/miso/annotations/ver2/
    """
    for genome in genomes:
        zip_fname = \
            os.path.join(events_dir,
                         "miso_annotations_%s_%s.zip" %(genome, VERSION))
        if not os.path.isfile(zip_fname):
            raise Exception, "Cannot find annotation zip %s" %(zip_fname)
        cmd = \
            "scp %s root@argonaute.mit.edu:/home/website/htdocs/burgelab/miso/annotations/ver2/" \
            %(zip_fname)
        print "Uploading %s" %(os.path.basename(zip_fname))
        os.system(cmd)
        

# Mapping from genome to a UCSC table
def genome_to_ucsc_table(genome):
    table_fname = \
        os.path.expanduser("~/jaen/pipeline_init/%s/ucsc/ensGene.kgXref.combined.txt" \
                           %(genome))
    return table_fname


def main():
    genomes = ["mm9", "mm10",
               "hg18", "hg19"]
    event_types = ["SE", "MXE", "A3SS", "A5SS", "RI"]
    # Directory where UCSC tables are
    ucsc_tables_dir = os.path.expanduser("~/jaen/ucsc_tables/")
    events_dir = os.path.expanduser("~/jaen/gff-events/ver2/")
    for genome in genomes:
        print "Making annotations for %s" %(genome)
        output_dir = os.path.join(events_dir, genome)
        curr_tables_dir = os.path.join(ucsc_tables_dir, genome)
        utils.make_dir(output_dir)
        cmd = \
            "gff_make_annotation.py %s %s --genome-label %s --sanitize " \
            %(curr_tables_dir,
              output_dir,
              genome)
        print "Executing: "
        print cmd
        #os.system(cmd)
    #Annotate the GFFs with gene information
    gff_fnames = []
    for genome in genomes:
        commonshortest_dir = \
            os.path.join(events_dir, genome, "commonshortest")
        for event_type in event_types:
            curr_gff = os.path.join(commonshortest_dir,
                                    "%s.%s.gff3" %(event_type, genome))
            gffutils_helpers.annotate_gff(curr_gff, genome)
    # Zip the annotations
    zip_annotations(events_dir, genomes)
    upload_annotations(events_dir, genomes)
        
    

if __name__ == "__main__":
    main()
