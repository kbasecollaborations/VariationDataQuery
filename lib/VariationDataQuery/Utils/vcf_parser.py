import os
import subprocess 

class vcf_parser:
  
   def init(self):
       pass

   def run_cmd(self, cmd):

       try:
          process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
          stdout, stderr = process.communicate()
          if stdout:
             print ("ret> ", process.returncode)
             print ("OK> output ", stdout)
          if stderr:
             print ("ret> ", process.returncode)
             print ("Error> error ", stderr.strip())

       except OSError as e:
           print ("OSError > ", e.errno)
           print ("OSError > ", e.strerror)
           print ("OSError > ", e.filename) 

   def get_variants(self, chr, start, stop, url_template, tbi_url_template, index):
       outpath = "/kb/module/deps"
       cmd =  "node " + outpath + "/get_variants.js " + chr + " " + start + " " + stop + " " + url_template + " " + tbi_url_template +" " + str(index)
       self.run_cmd(cmd)

   def getjson(self, header_file, variant_file, output_dir, index):
       
       Variations = []
       harray = []
       with open(header_file,"r") as hfile:
            for hline in hfile:
                hline = hline.rstrip()
                harray = hline.split(",")
       #print(harray)

       with open(variant_file,"r") as vfile:
            for vline in vfile:
                vline = vline.rstrip()
                varray = vline.split(",")
                for var in varray:
                    vcfarray = var.split("\t")
                    #print(vcfline)
                    chrm = vcfarray[0]
                    pos = vcfarray[1]
                    ref = vcfarray[3]
                    alt = vcfarray[4]
                    values = vcfarray[9:len(vcfarray)]
                    #print(values)
                    Variations.append( vcfarray)

       outfile = os.path.join(output_dir, "variants.tsv" )
       with open(outfile, "a") as fout:
            if (index == 0):
                fout.write("CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT")
                for hdr in harray:
                    fout.write("\t" + hdr)
                fout.write("\n")

            for i in range(0, len(Variations)):
                for j in range (0, len(Variations[i])):
                    fout.write(Variations[i][j] + "\t")
                fout.write("\n")

       return outfile
                

