#!/bin/bash
##
## Script to generate all conserved events via Ensembl mapping
##
yklib=~/jaen/yklib/

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

# Match events to exons 
exons_to_match=~/jaen/Musashi/tcga/compiled_data/TCGA_v1_exons.txt
num_base_diff="20"
for event_type in SE_shortest_noAceView
do
  gff=~/jaen/gff-events/conserved_events/mouse_human/$event_type.mm9.mouse_to_human.gff
  outdir=~/jaen/gff-events/conserved_events/mouse_human/exon_matched/
  #gff=~/jaen/gff-events/conserved_events/mouse_human/test.mm9.mouse_to_human.gff
  cmd="python $yklib/gff_conservation.py --match-exons $gff $exons_to_match $num_base_diff --output-dir $outdir"
  echo $cmd
done

##
## Match events
##
# Mouse to human, lifted over from hg19 to hg18
#for event_type in SE SE_shortest_noAceView #SE_noAceView ALE TandemUTR AFE A3SS A5SS RI MXE SE_noAceView
#do
#  echo "Running through ${event_type}"
#  sourcegff=~/jaen/gff-events/hg18/$event_type.hg18.gff3
#  targetgff=~/jaen/gff-events/conserved_events/mouse_human_new/$event_type.mm9.mouse_to_human.hg19_liftOver_hg18.gff
#  outdir=~/jaen/gff-events/conserved_events/mouse_human_new/final_matched_events/
#  bsub time python $yklib/gff_conservation.py --match-events $sourcegff $targetgff --output-dir $outdir
#done


# Get reciprocal events (from human to mouse)
#for event_type in RI  #SE RI    #ALE TandemUTR AFE A3SS A5SS RI MXE SE_noAceView
#do
#  gff=~/jaen/gff-events/hg19/$event_type.hg19.gff3
#  outdir=~/jaen/gff-events/conserved_events/human_mouse/
#  bsub time python $yklib/gff_conservation.py --get-orthologs $gff "human" "mouse" --output-dir $outdir/hg19_to_mouse/
#done

