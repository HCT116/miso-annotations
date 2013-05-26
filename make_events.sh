#!/bin/bash
events_dir=~/jaen/gff-events

rm $events_dir/mm9_alt_events.zip
rm $events_dir/hg18_alt_events.zip
rm $events_dir/hg19_alt_events.zip
rm $events_dir/modENCODE_alt_events.zip

## Mouse
mm9_outdir=$events_dir/mm9/pickled
rm -rf $mm9_outdir


# Make TandemUTR_3pseq
tandemutr_3pseq_file=${events_dir}/TandemUTR-3pseq-mm9/TandemUTR_3pseq_mm9.gff
for event_type in TandemUTR_3pseq
do
  cmd="index_gff.py --index ${tandemutr_3pseq_file} $mm9_outdir/${event_type} > ${events_dir}/mm9_output"
  echo "Executing: $cmd" 
  $cmd
done

for event_type in SE ALE TandemUTR AFE A3SS A5SS RI MXE 
do
 cmd="index_gff.py --index $events_dir/mm9/${event_type}.mm9.gff3 $mm9_outdir/${event_type} > ${events_dir}/mm9_output"
 echo "Executing: $cmd" 
 $cmd
done

##
## without AceView
##
for event_type in SE_noAceView SE_shortest_noAceView MXE_shortest_noAceView A3SS_shortest_noAceView A5SS_shortest_noAceView
do 
 cmd="index_gff.py --index $events_dir/mm9/$event_type.mm9.gff3 $mm9_outdir/$event_type > ${events_dir}/mm9_output_noAceView"
 echo "Executing: $cmd"
 $cmd
done

mmzipdir="mm9"
echo "Zipping mouse directory $mmzipdir"
zip -r $events_dir/mm9_alt_events.zip $mmzipdir -x "$mmzipdir/pickled/*"

##
## Human
## hg18
##
hg18_outdir=$events_dir/hg18/pickled
rm -rf $hg18_outdir
for event_type in SE ALE TandemUTR AFE A3SS A5SS RI MXE SE_noAceView
do
 cmd="index_gff.py --index $events_dir/hg18/$event_type.hg18.gff3 $hg18_outdir/$event_type > ${events_dir}/hg18_output"
 echo "Executing: $cmd"
 $cmd
done

##
## without AceView
##
hg18_outdir=$events_dir/hg18/pickled
for event_type in SE_noAceView SE_shortest_noAceView MXE_shortest_noAceView A3SS_shortest_noAceView A5SS_shortest_noAceView
do
 cmd="index_gff.py --index $events_dir/hg18/$event_type.hg18.gff3 $hg18_outdir/$event_type > ${events_dir}/hg18_output_noAceView"
 echo "Executing: $cmd"
 $cmd
done


hgzipdir="hg18"
echo "Zipping human directory $hgzipdir"
zip -r $events_dir/hg18_alt_events.zip $hgzipdir -x "$hgzipdir/pickled/*"

# hg19
hg19_outdir=$events_dir/hg19/pickled
rm -rf $hg19_outdir
for event_type in SE.hg19 ALE.hg19 TandemUTR.hg19 AFE.hg19 A3SS.hg19 A5SS.hg19 RI.hg19.revised MXE.hg19
do
  cmd="index_gff.py --index $events_dir/hg19/$event_type.gff3 $hg19_outdir/$event_type > ${events_dir}/hg19_output"
  echo "Executing: $cmd"
  $cmd
done

hg19zipdir="hg19"

echo "Zipping human directory $hg19zipdir"

zip -r $events_dir/hg19_alt_events.zip $hg19zipdir -x "$hg19zipdir/pickled/*"


# # modENCODE
# moddir=./modENCODE/
# # rm -rf $modENCODE_outdir
# # #modENCODE_A3SS_MISO.gff3  modENCODE_MISO_GFF3.tar.gz  modENCODE_RI_MISO.gff3
# # #modENCODE_A5SS_MISO.gff3  modENCODE_MXE_MISO.gff3     modENCODE_SE_MISO.gff3
# # for modtype in A3SS A5SS MXE RI SE
# # do
# #   event_name="modENCODE_$modtype"
# #   cmd="python $miso_dir/index_gff.py --index $events_dir/modENCODE/${event_name}_MISO.gff3 $modENCODE_outdir/$modtype"
# #   echo "Executing: $cmd"
# #   $cmd
# # done

# echo "Zipping modENCODE directory ${modENCODEdir}"
# zip -r $events_dir/modENCODE_alt_events.zip $moddir -x "$moddir/pickled/*"




