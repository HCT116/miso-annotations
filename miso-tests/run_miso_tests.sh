#!/bin/bash
SE=~/jaen/miso-annotations/miso-tests/indexed_events/
rl="40"
settings=~/jaen/Musashi/rna-seq/settings/miso_settings.txt

# Run first sample on cluster
#echo "Testing KH2_NoDox on cluster"
#miso --run $SE ./bams/KH2_NoDox.combined.sorted.bam --output-dir ./miso_output/KH2_NoDox --read-len $rl --use-cluster --chunk-jobs 200 --settings-filename $settings

# Run second sample multi-threaded
echo "Testing KH2_DOX locally"
miso --run $SE ./bams/KH2_DOX.combined.sorted.bam --output-dir ./miso_output/KH2_DOX --read-len $rl -p 5 --settings-filename $settings