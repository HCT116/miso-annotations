##
## Merge SpliceGraph events with new annotation
##
import os
import sys
import time
import glob

import gffutils
import gffutils.helpers as helpers
import gffutils.gffwriter as gffwriter

import rnaseqlib
import rnaseqlib.utils as utils
import rnaseqlib.gff.gffutils_helpers as gffutils_helpers

import misopy
import misopy.gff_utils as gff_utils
import misopy.Gene as gene_utils

import pandas
import pybedtools

from collections import defaultdict


def generic_merge(splicegraph_gff_fname, gff_fname, output_gff_fname,
                  genome, exon_id_suffix,
                  coords_diff_cutoff=10,
                  SE_merge=False):
    # Load SpliceGraph skipped exons
    splicegraph_in = pybedtools.BedTool(splicegraph_gff_fname)
    splicegraph_exons = \
        splicegraph_in.filter(lambda x: x.attrs["ID"].endswith(exon_id_suffix))
    # New annotation's skipped exons
    new_in = pybedtools.BedTool(gff_fname)
    new_exons = new_in.filter(lambda x: x.attrs["ID"].endswith(exon_id_suffix))
    # Intersect splicegraph exons with new exons
    intersected_gff = splicegraph_exons.intersect(new_exons,
                                                  wao=True,
                                                  s=True)
    # Compile the overlaps for each exon and the exon it
    # overlaps with
    exons_to_overlaps = defaultdict(list)
    for exon in intersected_gff:
        curr_overlap = int(exon.fields[-1])
        exons_to_overlaps[exon.attrs["ID"]].append((curr_overlap, exon))
    # If the maximum overlap between the SpliceGraph exon and
    # all exons in the new GFF annotation is LESS than 'coords_diff_cutoff'
    # then keep the SpliceGraph exon in the annotation
    # Name of SpliceGraph event trios to include in merged annotation
    splicegraph_trios_to_add = []
    # Mapping from SpliceGraph potentially redundant trios
    # to the new trios that they overlap with
    sg_redundant_trios = defaultdict(list)
    for exon_id in exons_to_overlaps:        
        trio_id = exon_id.rsplit(".", 2)[0]
        # Get maximum overlap
        overlaps = \
            [overlap_exon[0] \
             for overlap_exon in exons_to_overlaps[exon_id]]
        overlapping_trios = \
            [overlap_exon[1].attrs["ID"].rsplit(".", 2)[0] \
             for overlap_exon in exons_to_overlaps[exon_id]]
        max_ind, max_overlap = utils.max_item(overlaps)
        if max_overlap < coords_diff_cutoff:
            splicegraph_trios_to_add.append(trio_id)
        else:
            # Look at all new trios it overlaps with
            for new_overlapping_trio_id in overlapping_trios:
                if new_overlapping_trio_id != trio_id:
                    sg_redundant_trios[trio_id].append(new_overlapping_trio_id)
                else:
                    # Skip identical trios
                    continue
            # Collect potentially redundant trios
            sg_redundant_trios[trio_id].append(new_overlapping_trio_id)
    # If we're dealing with SEs, then do an SE specific
    # merge for the potentially redundant trios
    num_sg_trios = len(splicegraph_trios_to_add)
    print "Added %d trios from SpliceGraph" %(num_sg_trios)
    output_combined_gff_events(splicegraph_gff_fname,
                               splicegraph_trios_to_add,
                               gff_fname,
                               output_gff_fname,
                               genome)


def merge_se(splicegraph_gff_fname, gff_fname, output_gff_fname,
             genome):
    """
    Merge skipped exons. 
    """
    generic_merge(splicegraph_gff_fname, gff_fname, output_gff_fname,
                  genome,
                  ".se",
                  coords_diff_cutoff=10)
    

def merge_mxe(splicegraph_gff_fname, gff_fname, output_gff_fname,
              genome):
    generic_merge(splicegraph_gff_fname, gff_fname, output_gff_fname,
                  genome,
                  ".mxe1",
                  coords_diff_cutoff=10)


def merge_a3ss(splicegraph_gff_fname, gff_fname, output_gff_fname,
               genome):
    generic_merge(splicegraph_gff_fname, gff_fname, output_gff_fname,
                  genome,
                  ".coreAndExt",
                  coords_diff_cutoff=10)


def merge_a5ss(splicegraph_gff_fname, gff_fname, output_gff_fname,
               genome):
    generic_merge(splicegraph_gff_fname, gff_fname, output_gff_fname,
                  genome,
                  ".coreAndExt",
                  coords_diff_cutoff=10)


def merge_ri(splicegraph_gff_fname, gff_fname, output_gff_fname,
             genome):
    generic_merge(splicegraph_gff_fname, gff_fname, output_gff_fname,
                  genome,
                  ".withRI",
                  coords_diff_cutoff=10)


def merge_afe():
    pass


def merge_ale():
    pass


def merge_tandemUTR():
    """
    Use older SpliceGraph annotation for now.
    """
    pass


def merge_events(genome,
                 event_type,
                 splicegraph_events_dir,
                 new_events_dir,
                 output_dir):
    """
    Merge events.
    """
    sg_gff_fname = os.path.join(splicegraph_events_dir,
                                genome,
                                "%s.%s.gff3" %(event_type, genome))
    if not os.path.isfile(sg_gff_fname):
        print "Cannot find %s" %(sg_gff_fname)
        return
    if "_" in event_type:
        new_event_type = event_type.split("_")[0]
    else:
        new_event_type = event_type
    new_gff_fname = os.path.join(new_events_dir,
                                 genome,
                                 "commonshortest",
                                 "%s.%s.gff3" %(new_event_type, genome))
    if not os.path.isfile(new_gff_fname):
        print "Cannot find %s" %(new_gff_fname)
        return
    output_dir = os.path.join(output_dir, genome)
    utils.make_dir(output_dir)
    output_gff_fname = \
        os.path.join(output_dir, "%s.%s.gff3" %(event_type, genome))
    print "Merging %s.." %(event_type)
    print "  - Old: %s" %(sg_gff_fname)
    print "  - New: %s" %(new_gff_fname)
    merge_func = None
    if event_type.startswith("SE"):
        merge_func = merge_se
    elif event_type.startswith("MXE"):
        merge_func = merge_mxe
    elif event_type.startswith("A5SS"):
        merge_func = merge_a5ss
    elif event_type.startswith("A3SS"):
        merge_func = merge_a3ss
    elif event_type.startswith("RI"):
        merge_func = merge_ri
    if merge_func is None:
        raise Exception, "Unrecognized event type %s" %(event_type)
    # Make merge operation
    merge_func(sg_gff_fname, new_gff_fname, output_gff_fname,
               genome)


def get_se_from_gene_recs(gene_recs):
    for rec in gene_recs:
        if rec.id.endswith(".se"):
            return rec
    return None


def overlap_se(sg_gff_fname, new_gff_fname):
    """
    Compute overlap between old and new GFFs for SE events.
    """
    print "Overlapping old and new SE..."
    sg_db = gffutils.create_db(sg_gff_fname, ":memory:")
    new_db = gffutils.create_db(new_gff_fname, ":memory:")
    # Coordinates of new SEs
    new_se_coords = {}
    # Record all the new alternative exons
    for new_recs in new_db.iter_by_parent_childs():
        new_se_rec = get_se_from_gene_recs(new_recs)
        new_se_entry = \
            (new_se_rec.chrom, new_se_rec.start,
             new_se_rec.stop, new_se_rec.strand)
        new_se_coords[new_se_entry] = True
    # Check how many of the old ones are in the new
    in_both = 0
    for old_recs in sg_db.iter_by_parent_childs():
        old_se_rec = get_se_from_gene_recs(old_recs)
        old_se_entry = \
            (old_se_rec.chrom, old_se_rec.start,
             old_se_rec.stop, old_se_rec.strand)
        if old_se_entry in new_se_coords:
            print "%s" %(str(old_se_entry)), " is in new!"
            in_both += 1
    print "Total of %d SE exons in both." %(in_both)


def get_event_gff_recs(event_id, gff_db):
    """
    Get event's GFF records from a gff database.
    """
    event_rec = gff_db[event_id]
    event_child_recs = list(gff_db.children(event_id))
    all_recs = [event_rec] + event_child_recs
    return all_recs


def output_combined_gff_events(sg_gff_fname, sg_events,
                               new_gff_fname,
                               output_gff_fname,
                               genome,
                               sg_label="sg2008",
                               source_attr="source"):
    """
    Output the given events from sg_gff_fname and all of
    the entries from new_gff_fname into a single file.

    Mark SG events with sg_label.
    """
    gff_out_file = open(output_gff_fname, "w")
    gff_out = gffwriter.GFFWriter(gff_out_file)
    # SG records to output
    sg_records = []
    # New records to output
    new_records = []
    # Load up gffutils databases for SG and new events
    new_db = gffutils.create_db(new_gff_fname, ":memory:",
                                verbose=False)
    sg_db = gffutils.create_db(sg_gff_fname, ":memory:",
                               verbose=False)
    #sg_gff_genes = sg_db.features_of_type("gene")
    new_gff_genes = new_db.features_of_type("gene")
    # Output new events first
    new_ids = {}
    for gene_rec in new_gff_genes:
        gene_id = gene_rec.id
        gff_out.write_gene_recs(new_db, gene_id)
        new_ids[gene_id] = True
    # Output SG events
    for sg_gene_id in sg_events:
        if sg_gene_id in new_ids:
            print "Skipping %s" %(sg_gene_id)
            # If this has an identical ID to one of the new annotation
            # events, skip it
            continue
        # Get all SG event records
        sg_recs = get_event_gff_recs(sg_gene_id, sg_db)
        # Add source attribute to each record
        for rec in sg_recs:
            rec.attributes[source_attr] = [sg_label]
            gff_out.write_rec(rec)
    gff_out.close()
    # Sanitize the file
    sanitize_cmd = \
        "gffutils-cli sanitize %s --in-memory --in-place" %(output_gff_fname)
    print "Sanitizing merged GFF..."
    ret_val = os.system(sanitize_cmd)
    if ret_val != 0:
        raise Exception, "Sanitization failed on %s" %(output_gff_fname)
    # Annotate the file
    print "Annotating merged GFF..."
    gffutils_helpers.annotate_gff(output_gff_fname, genome)


def sanitize_splicegraph_events(genome, event_type,
                                splicegraph_dir, output_dir):
    """
    Sanitize and annotate old SpliceGraph events before
    merging with new events.
    """
    gff_fname = os.path.join(splicegraph_dir, genome, "%s.%s.gff3" %(event_type,
                                                                     genome))
    if not os.path.isfile(gff_fname):
        print "Cannot find %s" %(gff_fname)
        return
    # Make output directory for sanitized files
    output_dir = os.path.join(output_dir, genome)    
    utils.make_dir(output_dir)
    print "Sanitizing: %s" %(gff_fname)
    gff_label = os.path.basename(gff_fname)
    output_fname = os.path.join(output_dir, gff_label)
    if os.path.isfile(output_fname):
        print "%s already exists, skipping" %(output_fname)
        return
    sanitize_cmd = \
        "gffutils-cli sanitize %s > %s" %(gff_fname, output_fname)
    ret_val = os.system(sanitize_cmd)
    if ret_val != 0:
        raise Exception, "Sanitize command failed."
    # Now that it is sanitized, annotate it
    print "Annotating GFF..."
    gffutils_helpers.annotate_gff(output_fname, genome)


def main():
    splicegraph_events_dir = os.path.expanduser("~/jaen/gff-events")
    new_events_dir = os.path.expanduser("~/jaen/gff-events/ver2/")
    output_dir = os.path.expanduser("~/jaen/gff-events/merged-events/")
    splicegraph_sanitized_dir = os.path.expanduser("~/jaen/gff-events/splicegraph_sanitized/")
    # TODO: add AFE/ALE
    event_types = ["SE_shortest_noAceView"]#, "SE", "MXE", "A3SS", "A5SS", "RI"]
    print "Merging events..."
    print "  - Output dir: %s" %(output_dir)
    for genome in ["mm9"]:#["hg19"]:
        print "Genome: %s" %(genome)
        for event_type in event_types:
            print "Event type: %s" %(event_type)
            print "Sanitizing old SpliceGraph annotation..."
            sanitize_splicegraph_events(genome,
                                        event_type,
                                        splicegraph_events_dir,
                                        splicegraph_sanitized_dir)
            merge_events(genome,
                         event_type,
                         splicegraph_sanitized_dir,
                         new_events_dir,
                         output_dir)


if __name__ == "__main__":
    main()
    
    
    
    
