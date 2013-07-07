#!/bin/bash

##
## Shorten ALE IDs so as to not to create long filenames 
##

outdir=~/jaen/gff-events/
olddir=~/jaen/miso-annotations/old_annotations/

# hg18
python shorten_event_ids.py --shorten $olddir/hg18/ALE.hg18.gff3 $outdir/hg18/ALE.hg18.gff3

## Shorten AFEs

# hg18
python shorten_event_ids.py --shorten $olddir/hg18/AFE.hg18.gff3 $outdir/hg18/AFE.hg18.gff3

