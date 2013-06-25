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
    log_file.close()
    for genome in genomes:
        zip_fname = \
            os.path.join(events_dir,
                         "%s_alt_events.zip" %(genome, VERSION))
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

    http://genes.mit.edu/burgelab/miso/annotations/
    """
    for genome in genomes:
        zip_fname = \
            os.path.join(events_dir,
                         "%s_alt_events.zip" %(genome, VERSION))
        if not os.path.isfile(zip_fname):
            raise Exception, "Cannot find annotation zip %s" %(zip_fname)
        cmd = \
            "scp %s root@argonaute.mit.edu:/home/website/htdocs/burgelab/miso/annotations/" \
            %(zip_fname)
        print "Uploading %s" %(os.path.basename(zip_fname))
        print cmd
        print "DRY RUN"
        #os.system(cmd)


def main():
    # Ignore Drosophila annotations for now
    genomes = ["mm9", "mm10",
               "hg18", "hg19"]
    event_types = ["SE", "MXE", "A3SS", "A5SS", "RI", "AFE", "ALE"]
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
            os.system(sanitize_cmd)
    # Zip the annotations
    zip_annotations(events_dir, genomes)
    upload_annotations(events_dir, genomes)
        
