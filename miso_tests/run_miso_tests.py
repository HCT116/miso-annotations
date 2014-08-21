##
## Run extensive MISO testing
##
import os
import sys
import unittest
import shutil
import pysam
import misopy
import misopy.misc_utils as misc_utils

OUTPUT_DIR = "./miso_tests_output/"

def clear_output_dir():
    output_dir = OUTPUT_DIR
    # Clear out the previous test output directory
    print "Clearing previous output directory..."
    if os.path.isdir(output_dir):
        shutil.rmtree(output_dir, ignore_errors=True)
    # Make new output directory
    misc_utils.make_dir(output_dir)


class MISOFunctionalTests(unittest.TestCase):
    """
    Test MISO functionality on large scale data.
    """
    def setUp(self):
        self.data_dir = "./data"
        self.gff_dir = "./gff"
        self.gff_fname = \
          os.path.join(self.gff_dir, "SE.head_5000.mm9.gff3")
        self.bam_fname = os.path.join(self.data_dir, "mm9_sample1.bam")
        self.sample1_bam = self.bam_fname
        self.sample2_bam = os.path.join(self.data_dir, "mm9_sample2.bam")
        # BAM with mixed read lengths
        self.mixed_bam_fname = \
          os.path.join(self.data_dir, "mm9_mixed_se_reads.bam")
        self.ensGene_gff = "./gff/ensGene.head_10000.gff3"
        self.output_dir = OUTPUT_DIR
        self.settings_fname = "./miso_settings.txt"
        self.sample1_output = os.path.join(self.output_dir,
                                         "sample1_output")
        self.sample2_output = os.path.join(self.output_dir,
                                           "sample2_output")
        self.sample1_output_compressed = \
          os.path.join(self.output_dir,
                       "sample1_output_compressed")
        # Sample1 output with compressed index
        self.sample1_output_comp = \
          os.path.join(self.output_dir,
                       "sample1_output_comp_index")
        self.compressed_ids_fname = \
          os.path.join(self.output_dir,
                       "index_compressed",
                       "compressed_ids_to_genes.shelve")
        

    def run_cmd(self, cmd):
        print "Executing: %s" %(cmd)
        ret_val = os.system(cmd)
        if ret_val != 0:
            raise Exception, "Command failed."


    def index_gff_fname(self, gff_fname):
        """
        Index a GFF filename and return a link to
        its indexed directory.
        """
        output_dir = os.path.join(self.output_dir, "tmp",
                                  os.path.basename(gff_fname))
        print "Indexing %s to %s" %(gff_fname, output_dir)
        cmd = "index_gff --index %s %s" \
              %(self.gff_fname, output_dir)
        self.run_cmd(cmd)
        return output_dir


    def get_gff_fname(self, test_name):
        """
        Given a filename like 'SE.se_event1'
        return an absolute path to the GFF example, which is
        typically: '/some/path/to/SE.se_event1.gff3' (note
        the .gff3 extension)
        """
        gff_fname = os.path.join(self.gff_dir, "%s.gff3" %(test_name))
        if not os.path.isfile(gff_fname):
            raise Exception, "No GFF file %s found" %(gff_fname)
        return gff_fname
    

    def index_gff_example(self, gff_example_name):
        """
        Given a GFF example name like 'SE.event1.mm9',
        index its GFF and return the path to the GFF directory.
        """
        # First get the GFF filename
        gff_fname = self.get_gff_fname(gff_example_name)
        # Then index it
        index_dir = self.index_gff_fname(gff_fname)
        return index_dir

        
    def test_a_module_availability(self):
        cmd = "module_availability"
        self.run_cmd(cmd)


    def test_a_miso_version(self):
        cmd = "MISO version"
        self.run_cmd("miso --version")
        
        
    def test_a_index(self):
        """
        Test index.
        """
        print "Test index"
        cmd = "index_gff --index %s %s" \
              %(self.gff_fname,
                os.path.join(self.output_dir, "index"))
        self.run_cmd(cmd)
        

    def test_a_index_compressed(self):
        print "Test compressed index"
        cmd = "index_gff --index %s %s --compress-id" \
              %(self.gff_fname,
                os.path.join(self.output_dir, "index_compressed"))
        self.run_cmd(cmd)


    def test_a_exon_utils(self):
        print "Test exon utils"
        output_dir = os.path.join(self.output_dir, "test_exon_utils")
        cmd = "exon_utils --get-const-exons %s --min-exon-size 1000 " \
              "--output-dir %s" %(self.ensGene_gff,
                                  output_dir)
        self.run_cmd(cmd)


    def test_b_pe_utils(self):
        print "Test PE utils"
        cmd = "pe_utils --compute-insert-len "
        # TODO: complete me!


    def test_b_run_miso_two_samples(self):
        print "Run MISO on sample1 and sample2"
        # Run on sample1
        index_dir = os.path.join(self.output_dir, "index")        
        cmd = "miso --run %s %s --read-len 40 --output-dir %s" \
              %(index_dir,
                self.sample1_bam,
                self.sample1_output)
        self.run_cmd(cmd)
        # Run sample1 with compressed index too
        comp_index_dir = os.path.join(self.output_dir, "index_compressed")        
        cmd = "miso --run %s %s --read-len 40 --output-dir %s" \
              %(comp_index_dir,
                self.sample1_bam,
                self.sample1_output_compressed)
        self.run_cmd(cmd)
        # Run on sample2
        output_dir = os.path.join(self.output_dir,
                                  self.sample2_output)
        cmd = "miso --run %s %s --read-len 40 --output-dir %s" \
              %(index_dir,
                self.sample2_bam,
                self.sample2_output)
        self.run_cmd(cmd)
        

    def test_b_run_miso_single_end(self):
        print "Test run MISO single-end"
        output_dir = os.path.join(self.output_dir, "miso_output_single_end")
        index_dir = os.path.join(self.output_dir, "index")
        cmd = "miso --run %s %s --read-len 40 --output-dir %s" \
              %(index_dir,
                self.bam_fname,
                output_dir)
        self.run_cmd(cmd)

        
    def test_b_run_miso_single_end_compressed(self):
        print "Test run MISO single-end with compressed index"
        output_dir = os.path.join(self.output_dir,
                                  "miso_output_single_end_compressed")
        index_dir = os.path.join(self.output_dir, "index_compressed")
        cmd = "miso --run %s %s --read-len 40 --output-dir %s" \
              %(index_dir,
                self.bam_fname,
                output_dir)
        self.run_cmd(cmd)

        
    def test_b_run_miso_single_end_cluster(self):
        print "Test run MISO single-end on cluster"
        output_dir = os.path.join(self.output_dir, "miso_output_single_end_cluster")
        index_dir = os.path.join(self.output_dir, "index")
        # Call cluster but don't wait for jobs
        cmd = "miso --run %s %s --read-len 40 --output-dir %s --use-cluster --no-wait " \
              "--settings-filename %s" \
              %(index_dir,
                self.bam_fname,
                output_dir,
                self.settings_fname)
        self.run_cmd(cmd)


    def test_b_run_miso_mixed_single_end_reads(self):
        """
        Run MISO mixed read lengths file. Uses the example
        SE event "SE.event1.mm9" 
        """
        print "Test run MISO single-end on mixed read lengths"
        output_dir = os.path.join(self.output_dir,
                                  "miso_output_mixed_readlen_single_end")
        index_dir = self.index_gff_example("SE.event1.mm9")
        # Call cluster but don't wait for jobs
        cmd = "miso --run %s %s --read-len 40 --output-dir %s " \
              "--settings-filename %s" \
              %(index_dir,
                self.mixed_bam_fname,
                output_dir,
                self.settings_fname)
        self.run_cmd(cmd)
        print "QUITTING..."
        sys.exit(1)
        

    def test_b_run_miso_paired_end(self):
        print "Test run MISO paired-end"
        output_dir = os.path.join(self.output_dir, "miso_output_paired_end")
        index_dir = os.path.join(self.output_dir, "index")
        cmd = "miso --run %s %s --read-len 40 --output-dir %s --paired-end 200 20" \
              %(index_dir,
                self.bam_fname,
                output_dir)
        self.run_cmd(cmd)


    def test_c_miso_pack(self):
        print "Testing MISO packing"
        # Pack regular output (after copying it)
        source_dir = os.path.join(self.output_dir, "miso_output_single_end")
        sink_dir = os.path.join(self.output_dir, "miso_output_single_end_packed")
        self.run_cmd("cp -r %s %s" %(source_dir, sink_dir))
        miso_output = os.path.join(self.output_dir, "miso_output_single_end_packed")
        cmd = "miso_pack --pack %s" %(miso_output)
        print "Packing an unpacked MISO directory"
        self.run_cmd(cmd)
        # Try it again on packed directory
        print "Trying to pack already packed MISO directory"
        self.run_cmd(cmd)


    def test_d_summarize_samples(self):
        print "Test MISO sample summaries"
        # Summarize regular output
        miso_output = os.path.join(self.output_dir,
                                   "miso_output_single_end")
        output_dir = os.path.join(self.output_dir,
                                  "summary_single_end")
        cmd = "summarize_miso --summarize-samples %s %s" %(miso_output,
                                                           output_dir)
        self.run_cmd(cmd)
        # Summarize packed output
        miso_output = os.path.join(self.output_dir,
                                   "miso_output_single_end_packed")
        output_dir = os.path.join(self.output_dir,
                                  "summary_single_end_packed")
        cmd = "summarize_miso --summarize-samples %s %s" %(miso_output,
                                                           output_dir)
        self.run_cmd(cmd)
        # Summarize output for a sample with a compressed GFF index
        miso_output = os.path.join(self.output_dir,
                                   "miso_output_single_end_compressed")
        output_dir = os.path.join(self.output_dir,
                                  "summary_single_end_compressed")
        cmd = \
          "summarize_miso --summarize-samples %s %s --use-compressed %s" \
          %(miso_output,
            output_dir,
            self.compressed_ids_fname)
        
        
    def test_d_compare_samples(self):
        print "Test MISO sample comparison"
        # Compare regular miso outputs
        output_dir = os.path.join(self.output_dir, "test_comparison")
        comp_cmd = "compare_miso --compare-samples %s %s %s" \
                   %(self.sample1_output,
                     self.sample2_output,
                     output_dir)
        self.run_cmd(comp_cmd)
        # Pack one of the samples's outputs (sample1)
        cmd = "miso_pack --pack %s" %(self.sample1_output)
        self.run_cmd(cmd)
        # Run comparison: packed output versus unpacked output
        comp_cmd = "compare_miso --compare-samples %s %s %s" \
                   %(self.sample1_output,
                     self.sample2_output,
                     output_dir)
        self.run_cmd(comp_cmd)
        # Pack the second sample's output (sample2)
        cmd = "miso_pack --pack %s" %(self.sample2_output)
        self.run_cmd(cmd)
        # Run comparison: this time packed versus packed outputs
        comp_cmd = "compare_miso --compare-samples %s %s %s" \
                   %(self.sample1_output,
                     self.sample2_output,
                     output_dir)
        self.run_cmd(comp_cmd)
        # Compare samples with sample1 made from a compressed
        # index
        comp_cmd = "compare_miso --compare-samples %s %s %s " \
                   "--use-compressed %s" \
                   %(self.sample1_output,
                     self.sample2_output,
                     output_dir,
                     self.compressed_ids_fname)
        self.run_cmd(comp_cmd)


        
def main():
    clear_output_dir()
    unittest.main()
        
        
if __name__ == '__main__':
    main()
