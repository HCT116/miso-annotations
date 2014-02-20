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
        shutil.rmtree(output_dir)
    # Make new output directory
    misc_utils.make_dir(output_dir)

class MISOFunctionalTests(unittest.TestCase):
    """
    Test MISO functionality on large scale data.
    """
    def setUp(self):
        self.data_dir = "./data"
        self.gff_fname = "./gff/SE.head_5000.mm9.gff3"
        self.bam_fname = os.path.join(self.data_dir, "mm9_reads_1.bam")
        self.sample1_bam = self.bam_fname
        self.sample2_bam = os.path.join(self.data_dir, "mm9_reads_2.bam")
        self.ensGene_gff = "./gff/ensGene.head_10000.gff3"
        self.output_dir = OUTPUT_DIR
        self.settings_fname = "./miso_settings.txt"
        self.sample1_output = os.path.join(self.output_dir,
                                         "sample1_output")
        self.sample2_output = os.path.join(self.output_dir,
                                           "sample2_output")
        

    def run_cmd(self, cmd):
        print "Executing: %s" %(cmd)
        ret_val = os.system(cmd)
        if ret_val != 0:
            raise Exception, "Command failed."


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


    def test_b_run_miso_two_samples(self):
        print "Run MISO on sample1 and sample2"
        # Run on sample1
        output_dir = os.path.join(self.output_dir,
                                  self.sample1_output)
        index_dir = os.path.join(self.output_dir, "index")        
        cmd = "miso --run %s %s --read-len 40 --output-dir %s" \
              %(index_dir,
                self.sample1_bam,
                output_dir)
        self.run_cmd(cmd)
        # Run on sample2
        output_dir = os.path.join(self.output_dir,
                                  self.sample2_output)
        cmd = "miso --run %s %s --read-len 40 --output-dir %s" \
              %(index_dir,
                self.sample2_bam,
                output_dir)
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

        
def main():
    clear_output_dir()
    unittest.main()
        
        
if __name__ == '__main__':
    main()
