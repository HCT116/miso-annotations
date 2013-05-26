#!/bin/bash

# Replace commas with "-" signs for events
events_dir="/srv/sugarman/scratch/yarden/gff-events";
substitute="-";

# # mouse
# for event_type in SE ALE TandemUTR AFE A3SS A5SS RI MXE
# do
#   sed "s/,/$substitute/g" $events_dir/mm9/$event_type.mm9.gff3 > $events_dir/mm9/commaless/$event_type.mm9.gff3
# done

# # human hg18
# for event_type in SE ALE TandemUTR AFE A3SS A5SS RI MXE
# do
#   sed "s/,/$substitute/g" $events_dir/hg18/$event_type.hg18.gff3 > $events_dir/hg18/commaless/$event_type.hg18.gff3
# done

# # human hg19
# for event_type in SE.hg19 ALE.hg19 TandemUTR.hg19 AFE.hg19 A3SS.hg19 A5SS.hg19 RI.hg19.revised MXE.hg19
# do
#   sed "s/,/$substitute/g" $events_dir/hg19/$event_type.gff3 > $events_dir/hg19/commaless/$event_type.gff3
# done
