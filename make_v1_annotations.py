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
VERSION = "v1"
LIFTOVER_HG18_TO_HG19 = \
    os.path.expanduser("~/jaen/genomes/liftOver/hg18ToHg19.over.chain")

LIFTOVER_MM9_TO_MM10 = \
    os.path.expanduser("~/jaen/genomes/liftOver/mm9ToMm10.over.chain")


ANNOTATED_DIR = os.path.expanduser("~/jaen/gff-events/annotated_events/")
GENOME_TO_ANNOTATION_DIR = \
    {"mm9": os.path.join(ANNOTATED_DIR, "mm9", "mm9_events_to_genes.zip"),
     "mm10": os.path.join(ANNOTATED_DIR, "mm10", "mm10_events_to_genes.zip"),
     "hg18": os.path.join(ANNOTATED_DIR, "hg18", "hg18_events_to_genes.zip"),
     "hg19": os.path.join(ANNOTATED_DIR, "hg19", "hg19_events_to_genes.zip")}


def zip_annotations(events_dir, genomes):
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
            glob.glob(os.path.join(events_dir, genome, 
                                   "*.gff3"))
        files_to_zip = [log_fname] + annotation_fnames
        # Exclude AceView
        files_to_zip = [f for f in files_to_zip \
                        if "AceView" not in f]
        # Add events to genes mapping
        files_to_zip.append(GENOME_TO_ANNOTATION_DIR[genome])
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

    http://genes.mit.edu/burgelab/miso/annotations/
    """
    for genome in genomes:
        zip_fname = \
            os.path.join(events_dir,
                         "miso_annotations_%s_%s.zip" %(genome, VERSION))
        if not os.path.isfile(zip_fname):
            raise Exception, "Cannot find annotation zip %s" %(zip_fname)
        cmd = \
            "scp %s root@argonaute.mit.edu:/home/website/htdocs/burgelab/miso/annotations/" \
            %(zip_fname)
        print "Uploading %s" %(os.path.basename(zip_fname))
        print cmd
        os.system(cmd)


def liftOver_hg18_events(events_dir, event_types):
    for event_type in event_types:
        print "Converting %s from hg18 -> hg19 by liftOver" %(event_type)
        hg18_fname = \
            os.path.join(events_dir, "hg18", "%s.hg18.gff3" %(event_type))
        hg19_fname = \
            os.path.join(events_dir, "hg19", "%s.hg19.gff3" %(event_type))
        liftOver_cmd = "liftOver -gff %s %s %s %s" %(hg18_fname,
                                                     LIFTOVER_HG18_TO_HG19,
                                                     hg19_fname,
                                                     "./hg18_to_hg19.unmapped")
        print "Executing: %s" %(liftOver_cmd)
        ret_val = os.system(liftOver_cmd)
        if ret_val != 0:
            raise Exception, "liftOver from hg18 to hg19 failed."


def liftOver_mm9_events(events_dir, event_types):
    for event_type in event_types:
        print "Converting %s from mm9 -> mm10 by liftOver" %(event_type)
        mm9_fname = \
            os.path.join(events_dir, "mm9", "%s.mm9.gff3" %(event_type))
        mm10_fname = \
            os.path.join(events_dir, "mm10", "%s.mm10.gff3" %(event_type))
        liftOver_cmd = "liftOver -gff %s %s %s %s" %(mm9_fname,
                                                     LIFTOVER_MM9_TO_MM10,
                                                     mm10_fname,
                                                     "./mm9_to_mm10.unmapped")
        print "Executing: %s" %(liftOver_cmd)
        ret_val = os.system(liftOver_cmd)
        if ret_val != 0:
            raise Exception, "liftOver from mm9 to mm10 failed."
        

def main():
    # Ignore Drosophila annotations for now
    #genomes = ["mm9", "hg18", "hg19"]
    genomes = ["hg18", "mm9"]
    event_types = ["SE", "MXE", "A3SS", "A5SS", "RI", "AFE", "ALE", "TandemUTR"]
    # Directory where GFFs are
    events_dir = os.path.expanduser("~/jaen/gff-events/")
    for genome in genomes:
        print "Making sanitized annotations for %s" %(genome)
        for event_type in event_types:
            print "Processing %s" %(event_type)
            gff_fname = \
                os.path.join(events_dir, genome, "%s.%s.gff3" %(event_type,
                                                                genome))
            if not os.path.isfile(gff_fname):
                raise Exception, "Cannot find %s" %(gff_fname)
            sanitize_cmd = \
                "gffutils-cli sanitize %s --in-place" %(gff_fname)
            print "Executing: "
            print sanitize_cmd
            #os.system(sanitize_cmd)
    # Make hg19 annotations from hg18
    liftOver_hg18_events(events_dir, event_types)
    # Make mm10 annotations from mm9
    liftOver_mm9_events(events_dir, event_types)
    # Zip the annotations
    zip_annotations(events_dir, genomes)
    upload_annotations(events_dir, genomes)
    # Sanitize liftedOver annotations mm10, hg19
    liftedOver_genomes = ["mm10", "hg19"]
    for genome in liftedOver_genomes:
        for event_type in event_types:
            print "Sanitizing %s for %s" %(event_type, genome)
            gff_fname = \
                os.path.join(events_dir, genome, "%s.%s.gff3" %(event_type,
                                                                genome))
            if not os.path.isfile(gff_fname):
                raise Exception, "Cannot find %s" %(gff_fname)
            sanitize_cmd = \
                "gffutils-cli sanitize %s --in-place" %(gff_fname)
            print "Executing: "
            print sanitize_cmd
            #os.system(sanitize_cmd)
    zip_annotations(events_dir, liftedOver_genomes)
    upload_annotations(events_dir, liftedOver_genomes)

if __name__ == "__main__":
    main()
        
