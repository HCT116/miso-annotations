##
## Fix ALE events that do not have proper .A/.B suffix in their mRNAs
##
import os
import sys
import time

from itertools import ifilter, islice

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
        raise Exception, "Entries do not start with gene."
    if entries[-1].fields[2] == "gene":
        raise Exception, " Entries set spills over to next gene."


def fix_ale_gff(gff_fname, output_dir):
    utils.make_dir(output_dir)
    fixed_gff_fname = os.path.join(output_dir,
                                   os.path.basename(gff_fname))
    gff_in = pybedtools.BedTool(gff_fname)
    while True:
        entries = list(islice(gff_in, 6))
        if len(entries) == 0:
            raise StopIteration
        fix_ale_entries(entries)
    

def main():
    gff_fname = os.path.expanduser("~/jaen/gff-events/hg18/ALE.hg18.gff3")
    output_dir = os.path.expanduser("~/jaen/gff-events/hg18_ale_fixed/")
    fix_ale_gff(gff_fname, output_dir)


if __name__ == "__main__":
    main()
