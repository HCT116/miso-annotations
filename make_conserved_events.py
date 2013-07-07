##
## Generate conserved events by Ensembl synteny mapping
##
import os
import sys
import time

import yklib

import rnaseqlib
import rnaseqlib.utils as utils

YKLIB = os.path.expanduser("~/jaen/yklib/")
# Conservation script filename
CONS_SCRIPT_FNAME = os.path.join(YKLIB, "gff_conservation.py")
# Input GFF events (use merged events to be most inclusive)
GFF_EVENTS_DIR = os.path.expanduser("~/jaen/gff-events/merged_events/")
# Conserved events output directory
CONS_EVENTS_DIR = os.path.join(GFF_EVENTS_DIR, "conserved_events")

# Get mouse-human conserved events (hg19 coordinates)
#for event_type in SE SE_shortest_noAceView #RI SE_shortest_noAceView SE_noAceView   #ALE TandemUTR AFE A3SS A5SS RI MXE SE_noAceView
#do
#  echo "Running through ${event_type}"
#  gff=~/jaen/gff-events/mm9/$event_type.mm9.gff3
#  outdir=~/jaen/gff-events/conserved_events/mouse_human/
#  cmd="bsub time python $yklib/gff_conservation.py --get-orthologs $gff "mouse" "human" --output-dir $outdir --liftover hg19 hg18"
#  echo $cmd
#  $cmd
#done

def conserved_events_mouse_to_human(event_types=["SE",
                                                 "SE_shortest_noAceView"]):
    """
    Generate conserved events for the given event types, outputting
    result to output_dir.

    Generate conserved events by mapping from mouse events to human.
    """
    output_dir = os.path.join(CONS_EVENTS_DIR, "mouse_to_human")
    utils.make_dir(output_dir)
    print "Generating conserved events from mouse to human..."
    print "  - Output dir: %s" %(output_dir)
    for event_type in event_types:
        print "Generating conserved events of type %s" %(event_type)
        mouse_gff_fname = \
            os.path.join(GFF_EVENTS_DIR, "%s.mm9.gff3" %(event_type))
        print "Mapping %s to human" %(mouse_gff_fname)
        if not os.path.isfile(mouse_gff_fname):
            raise Exception, "Cannot find mouse gff %s" %(mouse_gff_fname)
        cmd = \
            "bsub time python %s --get-orthologs %s \"mouse\" \"human\" --output-dir %s" \
            %(CONS_SCRIPT_FNAME,
              mouse_gff_fname,
              output_dir)
        print "Executing: %s" %(cmd)
        #ret_val = os.system(cmd)
        #if ret_val != 0:
        #    raise Exception, "Call to %s failed." %(CONS_SCRIPT_FNAME)


def main():
    conserved_events_mouse_to_human()

    

        
        
