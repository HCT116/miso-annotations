##
## Map events to genes
##
import os
import sys
import time

import rnaseqlib
import rnaseqlib.utils as utils

genomes_to_events = {"mm9":
                     ["SE", "TandemUTR", "A3SS", "A5SS", "ALE", "AFE",
                      "MXE", "RI", "TandemUTR", "SE_shortest_noAceView",
                      "A3SS_shortest_noAceView", "A5SS_shortest_noAceView",
                      "MXE_shortest_noAceView"],
                     "mm10":
                     ["SE", "TandemUTR", "A3SS", "A5SS", "ALE", "AFE",
                      "MXE", "RI", "TandemUTR", "SE_shortest_noAceView",
                      "A3SS_shortest_noAceView", "A5SS_shortest_noAceView",
                      "MXE_shortest_noAceView"],
                     "hg18":
                     ["SE", "TandemUTR", "A3SS", "A5SS", "ALE", "AFE",
                      "MXE", "RI", "SE_shortest_noAceView",
                      "A3SS_shortest_noAceView", "A5SS_shortest_noAceView",
                      "MXE_shortest_noAceView"],
                     "hg19":
                     ["SE", "TandemUTR", "A3SS", "A5SS", "ALE", "AFE",
                      "MXE", "RI"]}

# Gene tables indexed by genome
gene_tables = {"mm9": "/home/yarden/jaen/pipeline_init/mm9/ucsc/",
               "mm10": "/home/yarden/jaen/pipeline_init/mm9/ucsc/",
               "hg18": "/home/yarden/jaen/pipeline_init/hg18/ucsc/",
               "hg19": "/home/yarden/jaen/pipeline_init/hg19/ucsc/"}

intersect_events = "intersect_events.py"
events_dir = "/home/yarden/jaen/gff-events"
events_outdir = os.path.join(events_dir, "annotated_events")
utils.make_dir(events_outdir)


for genome, events in genomes_to_events.iteritems():
    print "Processing genome %s" %(genome)
    curr_outdir = os.path.join(events_outdir, genome)
    print "  - Output dir: %s" %(curr_outdir)
    for event in events:
        if ("AceView" in event) or ("3pseq" in event):
            continue
        print "Intersecting %s.." %(event)
        events_fname = os.path.join(events_dir,
                                    genome,
                                    "%s.%s.gff3" %(event,
                                                   genome))
        if not os.path.isfile(events_fname):
            raise Exception, "%s does not exist." %(events_fname)
        print "  - Events file: %s" %(events_fname)
        cmd = "%s --intersect %s %s --output-dir %s" \
            %(intersect_events,
              events_fname,
              gene_tables[genome],
              curr_outdir)
        print "Executing: %s" %(cmd)
        os.system(cmd)
    # zip the events
    zip_name = os.path.join(curr_outdir, "%s_events_to_genes.zip" %(genome))
    os.chdir(events_outdir)
    print "CDd into %s" %(events_outdir)
    cmd="zip --exclude=%s %s %s/*.txt" %(curr_outdir,
                                         zip_name,
                                         genome)
    print "Executing: %s" %(cmd)
    os.system(cmd)
