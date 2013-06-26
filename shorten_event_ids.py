##
## Shorten long event IDs from GFF file to unique identifier
##
import misopy
import misopy.gff_utils as GFF
import time
import os
import sys
import re

# Global counter for new IDs
id_num = 0

def shorten_id(id_value, max_id_len):
    """
    Return shortened version of ID.
    """
    global id_num
    prefix_len = 20
    new_id = id_value
    # Use first N characters of the original ID plus number
    # if ID is too long
    if len(id_value) > max_id_len:
        new_id = "%s%d" %(id_value[0:prefix_len], id_num)
        if "," in id_value:
            original_suffix = id_value.split(",")[-1]
            new_id = "%s.%s" %(new_id, original_suffix)
        id_num += 1
    new_id = new_id.replace(",", "")
    if len(new_id) > max_id_len:
        print len(new_id)
        raise Exception, "%s greater than or equal to 70 chars." \
              %(new_id)
    return new_id


def shorten_rec(gff_rec, old_to_new_ids, max_id_len):
    """
    Shorten GFF record. Return new record.
    """
    rec_id = ",".join(gff_rec.attributes["ID"])
    if "Parent" in gff_rec.attributes:
        rec_parent = ",".join(gff_rec.attributes["Parent"])
    else:
        rec_parent = ""
    
    new_attributes = gff_rec.attributes.copy()

    if rec_id not in old_to_new_ids:
        # Set new attributes for ID field
        old_to_new_ids[rec_id] = shorten_id(rec_id, max_id_len)
    new_attributes['ID'] = [old_to_new_ids[rec_id]]
    new_attributes['Name'] = [old_to_new_ids[rec_id]]
    if rec_parent not in old_to_new_ids:
        # Set new attributes for Parent field
        old_to_new_ids[rec_parent] = shorten_id(rec_parent, max_id_len)
    if old_to_new_ids[rec_parent] != "":
        # Only set parent record if there is a parent 
        new_attributes['Parent'] = [old_to_new_ids[rec_parent]]
    new_gff_rec = GFF.GFF(seqid=gff_rec.seqid,
                          source=gff_rec.source,
                          type=gff_rec.type,
                          start=gff_rec.start,
                          end=gff_rec.end,
                          score=gff_rec.score,
                          strand=gff_rec.strand,
                          phase=gff_rec.phase,
                          attributes=new_attributes)

    return new_gff_rec
    
    
def shorten_gff(input_gff, output_gff, max_id_len=75):
#     # List of search and replace with IDs
#     replace_ids = []

#     # pattern to identify ID= elements
#     pat = 'ID=(.+);'


#     input_file = open(input_gff, 'r')
#     for line in input_file:
#         # find ID= elements
#         match = re.search(pat, line)
#         if match != None:
#             assert(len(match.groups()) > 0)
#             id_to_replace = match.groups()[0]
#             if len(id_to_replace) >= max_id_len:
#                 new_id = shorten_id(id_to_replace)
#                 #replace_ids.append((id_to_replace, new_id))
#                 old_to_new_ids[id_to_replace] = new_id
    """
    Replace the ith ID in old_ids with the ith ID in new_ids.
    Output result to output gff.
    """
    new_recs = []
    # Load input GFF
    t1 = time.time()
    gff_in = GFF.GFFDatabase(from_filename=input_gff,
                             reverse_recs=True)

    # Mapping from old to new IDs
    old_to_new_ids = {}
    
    for rec in gff_in:
        new_record = shorten_rec(rec, old_to_new_ids, max_id_len)
        new_recs.append(new_record)
    t2 = time.time()

    print "Loading of input GFF took %.2f seconds" %(t2 - t1)

    print "Writing revised gff to: %s" %(output_gff)

    output_file = open(output_gff, 'w')
    gff_writer = GFF.Writer(output_file)

    # Write new GFF file
    gff_writer.write_recs(new_recs)

    output_file.close()

def main():
    from optparse import OptionParser
    parser = OptionParser()  
    parser.add_option("--shorten", dest="shorten", nargs=2, default=None,
                      help="Shorten input GFF file (first argument) and output "
                      "to filename (second argument)")
    (options, args) = parser.parse_args()

    if options.shorten != None:
        input_filename = os.path.abspath(os.path.expanduser(options.shorten[0]))
        output_filename = os.path.abspath(os.path.expanduser(options.shorten[1]))

        shorten_gff(input_filename, output_filename)

if __name__ == '__main__':
    main()
