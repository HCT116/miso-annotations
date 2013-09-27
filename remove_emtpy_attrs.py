##
## Script to remove empty attributes like 'Parent;'
## from GFF file
##
import os
import sys
import time
import argh
from argcomplete.completers import EnvironCompleter
from argh import arg
import shutil


def reformat_attrs(attrs):
    """
    Remove empty attributes from GFF.
    """
    new_attrs_fields = []
    fields = attrs.split(";")
    for f in fields:
        if "=" not in f:
            continue
        new_attrs_fields.append(f)
    new_attrs = ";".join(new_attrs_fields)
    return new_attrs
    

@arg("gff-fname", help="GFF filename to remove empty attributes from.")
def run(gff_fname):
    """
    Run on GFF filename.
    """
    output_fname = "%s.tmp" %(gff_fname)
    gff_out = open(output_fname, "w")
    with open(gff_fname) as gff_in:
        for line in gff_in:
            if line.startswith("#"):
                gff_out.write(line)
                continue
            line = line.strip()
            fields = line.split("\t")
            attrs = reformat_attrs(fields[-1])
            new_line = "\t".join(fields[0:-1] + [attrs]) + "\n"
            gff_out.write(new_line)
    gff_out.close()
    print "Renaming %s -> %s" %(output_fname, gff_fname)
    shutil.move(output_fname, gff_fname)


def main():
    argh.dispatch_commands([
        run,
    ])

if __name__ == "__main__":
    main()
