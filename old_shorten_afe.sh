#!/bin/bash

##
## Shorten AFE IDs so as to not to create long filenames 
##

# mm9
#python shorten_event_ids.py --shorten mm9/AFE.mm9.gff3 mm9/AFE.mm9.gff3

# hg18
#python shorten_event_ids.py --shorten hg18/AFE.hg18.gff3 hg18/AFE.hg18.gff3

# hg19
python shorten_event_ids.py --shorten hg19/AFE.hg19.gff3 hg19/AFE.hg19.gff3

