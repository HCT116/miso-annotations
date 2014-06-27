##
## Index all events
##
import os
import sys
import glob
import time

import rnaseqlib
import rnaseqlib.utils as utils

MERGED_EVENTS_DIR = os.path.expanduser("~/jaen/gff-events/merged-events/")

def index_merged_events():
    event_types = ["SE", "SE_shortest_noAceView", "MXE", "A3SS", "A5SS", "RI"]
    genomes = ["mm9", "hg18", "hg19"]
    for genome in genomes:
        for event_type in event_types:
            gff_fname = \
                os.path.join(MERGED_EVENTS_DIR, genome,
                             "%s.%s.gff3" %(event_type, genome))
            output_dir = \
                os.path.join(MERGED_EVENTS_DIR, "pickled", genome, event_type)
            if not os.path.isdir(output_dir):
                utils.make_dir(output_dir)
            if not os.path.isfile(gff_fname):
                print "Cannot find %s" %(gff_fname)
                continue
            cmd = "index_gff --index %s %s" %(gff_fname, output_dir)
            ret_val = os.system(cmd)
            if ret_val != 0:
                raise Exception, "Failed to index %s" %(gff_fname)

def main():
    index_merged_events()

    
if __name__ == "__main__":
    main()
