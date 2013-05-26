#!/bin/bash

events_dir=~/jaen/gff-events/
seqs_dir=${events_dir}/sequences/
mm9_outdir=$events_dir/sequences/mm9/
yklib=~/jaen/yklib
mm9_genome=~/jaen/genomes/mm9_nonewlines/

for event_type in RI #SE
do
  eventfile=${events_dir}/mm9/${event_type}.mm9.gff3
  cmd="python $yklib/fetch_gff_seq.py --fetch $eventfile ${mm9_genome} --output-dir ${seqs_dir}/mm9/$event_type/"
  echo "executing $cmd"
done