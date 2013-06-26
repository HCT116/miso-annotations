##
## Fix ALE events that do not have proper .A/.B suffix in their mRNAs
##
import os
import sys
import time

from itertools import ifilter, islice, tee

import rnaseqlib
import rnaseqlib.utils as utils

import pybedtools


def fix_ale_entries(entries):
    """
    Given all entries belonging to an event, fix it such
    that the first mRNA is A.

    Also remove blank parent ID.
    """
    if entries[0].fields[2] != "gene":
        print str(entries[0]).strip()
        raise Exception, "Entries do not start with gene."
    if entries[-1].fields[2] == "gene":
        raise Exception, " Entries set spills over to next gene at: %s" %(str(entries[0]))


def ale_iterator(gff_in):
    """
    Return ALE iterator. 
    """
    while True:
        # Get next 6 elements
        gff_stream1, gff_stream2 = tee(gff_in, 2)
        stream1_entries = list(islice(gff_stream1, 6))
        # Otherwise, it's a correctly formed entry, so return
        # the entries up until
        stream2_entries = list(islice(gff_stream2, 5))
        if len(stream1_entries) == 0 or len(stream2_entries) == 0:
            raise StopIteration
        # If the last type is an exon, it's a malformed
        # entry with too many exons -- still consider
        # it 
        last_entry_type = stream1_entries[-1].fields[2]
        if last_entry_type == "exon":
            gff_in = gff_stream1
            yield stream1_entries
        else:
            gff_in = gff_stream2
            yield stream2_entries


def fix_ale_gff(gff_fname, output_dir):
    utils.make_dir(output_dir)
    fixed_gff_fname = os.path.join(output_dir,
                                   os.path.basename(gff_fname))
    gff_in = list(pybedtools.BedTool(gff_fname))
    for entries in ale_iterator(gff_in):
        fix_ale_entries(entries)
    # gff_in = pybedtools.BedTool(gff_fname).as_intervalfile()
    # while True:
    #     entries = list(islice(gff_in, 5))
    #     # Check if it's an entry set with three exons or not
    #     if last_entry_type:
    #         # It's a malformed entry with 3 exons
    #         fix_ale_entries
        
    #     if len(entries) == 0:
    #         raise StopIteration
    #     fix_ale_entries(entries)
        
    

def main():
    gff_fname = os.path.expanduser("~/jaen/gff-events/hg18/ALE.hg18.gff3")
    output_dir = os.path.expanduser("~/jaen/gff-events/hg18_ale_fixed/")
    fix_ale_gff(gff_fname, output_dir)


if __name__ == "__main__":
    main()
