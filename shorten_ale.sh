#!/bin/bash

##
## Shorten ALE IDs so as to not to create long filenames 
##

# mm9
python shorten_event_ids.py --shorten mm9/ALE.mm9.gff3 mm9/ALE.mm9.gff3

# hg18
python shorten_event_ids.py --shorten hg18/ALE.hg18.gff3 hg18/ALE.hg18.gff3

# hg19
python shorten_event_ids.py --shorten hg19/ALE.hg19.gff3 hg19/ALE.hg19.gff3


## Shorten AFEs