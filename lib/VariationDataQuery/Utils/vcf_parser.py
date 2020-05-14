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

   def get_variants(self, chr, start, stop, url_template, tbi_url_template):
       outpath = "/kb/module/deps"
       cmd =  "node " + outpath + "/get_variants.js " + chr + " " + start + " " + stop + " " + url_template + " " + tbi_url_template 
       self.run_cmd(cmd)

   def getjson(self, header_file, variant_file, output_dir):
       
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
                    Variations.append(
                                       {
                                          "Chr" : chrm,
                                          "Pos" : pos,
                                          "Ref" : ref,
                                          "Alt" : alt,
                                          "type": "SNP/Indel" 
                                       }
                  
                   )
       
       outfile = os.path.join(output_dir,"variants.tsv" )
       with open(outfile, "w") as fout:
            fout.write("Sample\tSNP\tCHR\tRef\tAllele\tPOS\n")
            for i in range(0, len(Variations)):
                fout.write(harray[i] +"\t" +Variations[i]["Chr"]+"_"+Variations[i]["Pos"] + "\t" + Variations[i]["Chr"] + "\t" + Variations[i]["Ref"]+ "\t" + Variations[i]["Alt"] + "\t" + Variations[i]["Pos"]+"\n")       

       return outfile
                
                    
#if __name__ == '__main__':
#   vp = vcf_parser()
#   vp.get_variants( "Chr02", "1" , "10000",  "https://appdev.kbase.us/dynserv/b8fedfd6d8a1fc10372bcbad4f152b4b6d85507b.VariationFileServ/shock/a293a557-47b3-4fcc-8bef-d2049ad6368a", "https://appdev.kbase.us/dynserv/b8fedfd6d8a1fc10372bcbad4f152b4b6d85507b.VariationFileServ/shock/f19936ff-6f66-4a44-831f-1bfcdc6e88c4")
#   vp.getjson("sample_names.txt", "data.txt")
