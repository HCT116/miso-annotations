#!/bin/bash
## 
## Send annotation zip files to website
##
events_dir=~/jaen/gff-events/

##
## Update annotated events
##
scp -r ${events_dir}/annotated_events/*/*.zip root@argonaute.mit.edu:/home/website/htdocs/burgelab/miso/annotations/

# Upload gene models
# Mouse
#scp $events_dir/gene-models/gff/Mus_musculus.NCBIM37.65.gff.zip root@argonaute:/home/website/htdocs/burgelab/miso/annotations/gene-models/

# Human
#scp $events_dir/gene-models/gff/Homo_sapiens.GRCh37.65.gff.zip root@argonaute:/home/website/htdocs/burgelab/miso/annotations/gene-models/

##
## MISO alternative events
##
# hg19
#scp $events_dir/hg19_alt_events.zip root@argonaute:/home/website/htdocs/burgelab/miso/annotations

# hg18
#scp $events_dir/hg18_alt_events.zip root@argonaute:/home/website/htdocs/burgelab/miso/annotations

# mm9
#scp $events_dir/mm9_alt_events.zip root@argonaute:/home/website/htdocs/burgelab/miso/annotations

# modENCODE
#scp $events_dir/modENCODE_alt_events.zip root@argonaute:/home/website/htdocs/burgelab/miso/annotations

