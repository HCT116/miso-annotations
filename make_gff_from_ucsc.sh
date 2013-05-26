#!/bin/bash
##
## Make GFF annotations from UCSC ensGene tables for common genomes
##


##
## Download the ensGene tables from UCSC
##
echo "Downloading tables from UCSC"
echo "Clearing previous files"
rm ./ucsc_tables/*/ensGene*

# mm9
wget http://hgdownload.cse.ucsc.edu/goldenPath/mm9/database/ensGene.txt.gz -O ./ucsc_tables/mm9/ensGene.txt.gz
gunzip ./ucsc_tables/mm9/ensGene.txt.gz
# mm10
wget http://hgdownload.cse.ucsc.edu/goldenPath/mm10/database/ensGene.txt.gz -O ./ucsc_tables/mm10/ensGene.txt.gz
gunzip ./ucsc_tables/mm10/ensGene.txt.gz
# hg18
wget http://hgdownload.cse.ucsc.edu/goldenPath/hg18/database/ensGene.txt.gz -O ./ucsc_tables/hg18/ensGene.txt.gz
gunzip ./ucsc_tables/hg18/ensGene.txt.gz
# hg19
wget http://hgdownload.cse.ucsc.edu/goldenPath/hg19/database/ensGene.txt.gz -O ./ucsc_tables/hg19/ensGene.txt.gz
gunzip ./ucsc_tables/hg19/ensGene.txt.gz


##
## Convert the tables to GFF3 files using ucsc_table2gff3.pl
##
ucsc_table2gff3.pl --table ./ucsc_tables/mm9/ensGene.txt
ucsc_table2gff3.pl --table ./ucsc_tables/mm10/ensGene.txt
ucsc_table2gff3.pl --table ./ucsc_tables/hg18/ensGene.txt
ucsc_table2gff3.pl --table ./ucsc_tables/hg19/ensGene.txt

