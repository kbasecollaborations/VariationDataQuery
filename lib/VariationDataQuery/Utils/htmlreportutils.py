import uuid
from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.KBaseReportClient import KBaseReport

class htmlreportutils:
    def __init__(self):
        self.organism_dict = {}
        pass

    def create_table(self, filename, caption, output_dir):

        id = filename.split(".")[0]

        try:
            data = pd.read_csv(output_dir + "/" + filename, sep='\t')
        except pd.errors.EmptyDataError:
            print(filename + ' was empty')

        sorteddf = data.sort_values('pval', ascending=True)

        htmlout = "<center><b>Gene Set Enrichment using " + caption + "</b></center>"

        if (filename == 'paper_output.txt'):
            htmlout += "<div style=\"height: 850px; width: 590px; border: 1px ridge; black; background: #e9d8f2; " \
                       "padding-top: 20px; padding-right: 0px; padding-bottom: 20px; padding-left: 20px; overflow: auto;\">" \
                       "<table id=\"" + id + "\" class=\"table table-striped table-bordered\" style=\"width:100%\"><thead><tr>" \
                                             "<th>Feature Id</th><th>Term</th><th>Matches</th><th>P-value</th><th>Organism Name</th></tr></thead><tbody>"
        else:
            htmlout += "<div style=\"height: 850px; width: 590px; border: 1px ridge; black; background: #e9d8f2; " \
                       "padding-top: 20px; padding-right: 0px; padding-bottom: 20px; padding-left: 20px; " \
                       "overflow: auto;\"><table id=\"" + id + "\" class=\"table table-striped table-bordered\" style=\"width:100%\">" \
                                                               "<thead><tr><th>Feature Id</th><th>Term</th><th>Matches</th><th>P-value</th></tr></thead><tbody>"

        for index, row in sorteddf.iterrows():
            feature = row['ID']
            term = row['Term']
            matches = row['k']
            pvalue = format(row["pval"], '.3g')

            if (filename == 'paper_output.txt'):
                htmlout += "<tr><td>" + str(feature) + "</td><td>" + str(term) + "</td><td>" + str(
                    matches) + "</td><td>" \
                           + str(pvalue) + "</td><td>" + self.get_organism(feature) + "</td></tr>"
            else:
                htmlout += "<tr><td>" + str(feature) + "</td><td>" + str(term) + "</td><td>" + str(
                    matches) + "</td><td>" \
                           + str(pvalue) + "</td></tr>"

        htmlout += "</tbody><tfoot><tr><th>Feature Id</th><th>Term</th><th>Matches</th><th>P-value</th></tr></tfoot></table></div>"
        return htmlout

    def create_enrichment_report(self, output_dir, dir):
        '''
                function for adding enrichment score to report
        '''

        dirs = next(os.walk(dir))[1]
        for i in range(len(next(os.walk(dir))[1])):
            path = os.path.join(dir, (next(os.walk(dir))[1])[i])

        output = "<html><head><link rel=\"stylesheet\" type=\"text/css\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap" \
                 "/3.3.7/css/bootstrap.min.css\"><link rel=\"stylesheet\" type=\"text/css " \
                 "\"href=\"https://cdn.datatables.net/1.10.20/css/dataTables.bootstrap.min.css\"><script src=\"https://code.jquery.com/jquery-3.3.1.js\">" \
                 "</script><script src=\"https://cdn.datatables.net/1.10.20/js/jquery.dataTables.min.js\">" \
                 "</script><script src=\"https://cdn.datatables.net/1.10.20/js/dataTables.bootstrap.min.js\"></script>"
        output += "<script> $(document).ready(function() {$(\'#go_biological_process_output\').DataTable();} ); </script>"
        output += "<script> $(document).ready(function() {$(\'#go_molecular_function_output\').DataTable();} ); </script>"
        output += "<script> $(document).ready(function() {$(\'#go_cellular_component_output\').DataTable();} ); </script>"
        output += "<script> $(document).ready(function() {$(\'#kegg_enzyme_output\').DataTable();} ); </script>"
        output += "<script> $(document).ready(function() {$(\'#kog_output\').DataTable();} ); </script>"
        output += "<script> $(document).ready(function() {$(\'#panther_output\').DataTable();} ); </script>"
        output += "<script> $(document).ready(function() {$(\'#smart_output\').DataTable();} ); </script>"
        output += "<script> $(document).ready(function() {$(\'#pfam_output\').DataTable();} ); </script>"
        output += "<script> $(document).ready(function() {$(\'#pathway_output\').DataTable();} ); </script>"
        output += "<script> $(document).ready(function() {$(\'#paper_output\').DataTable();} ); </script>"
        output += "<br><b>Gene Set:</b>&nbsp;&nbsp;&nbsp;" + self.get_genelist(path + ".genelist") + "<br>"
        output += "</head><body><table cellpadding = \"100\" cellspacing = \"100\" >"

        output += "<tr><td style=\"padding:10px\">" + self.create_table("go_biological_process_output.txt",
                                                                        "GO (Biological Process)", output_dir) \
                  + "</td><td style=\"padding:10px\">" + self.create_table("go_molecular_function_output.txt",
                                                                           "GO (Molecular Function)", output_dir) \
                  + "</td> <td style=\"padding:10px\">" + self.create_table("go_cellular_component_output.txt",
                                                                            "GO (Cellular Component)", output_dir) \
                  + "</td></tr>"

        output += "<tr><td style=\"padding:10px\">" + self.create_table("kegg_enzyme_output.txt", "KEGG Enzyme",
                                                                        output_dir) \
                  + "</td> <td style=\"padding:10px\">" + self.create_table("kog_output.txt", "KOG", output_dir) \
                  + "</td><td style=\"padding:10px\">" + self.create_table("panther_output.txt", "Panther",
                                                                           output_dir) + "</td></tr>"

        output += "<tr><td style=\"padding:10px\">" + self.create_table("smart_output.txt", "SMART", output_dir) \
                  + "</td> <td style=\"padding:10px\">" + self.create_table("pfam_output.txt", "PFAM", output_dir) \
                  + "</td> <td style=\"padding:10px\">" + self.create_table("pathway_output.txt", "Pathway",
                                                                            output_dir) + "</td></tr>"
        output += "<tr><td colspan=\"3\" style=\"padding:10px\">" + self.create_table("paper_output.txt", "Publication",
                                                                                      output_dir) + "</td></tr>"
        output += "</table></body></html>"

        return output

    def create_html_report(self, callback_url, output_dir, workspace_name):
        '''
         function for creating html report
        '''

        dfu = DataFileUtil(callback_url)
        report_name = 'kb_variant_report_' + str(uuid.uuid4())
        report = KBaseReport(callback_url)


        index_file_path = output_dir + "/variants.tsv"
        htmlstring = "<a href='" + index_file_path +"'> report link </a>"

       
        try:
            with open(output_dir +"/index.html" , "wt") as html_file:
               n = html_file.write(htmlstring)
        except IOError:
            print("Unable to write "+ index_file_path + " file on disk.")

        report_shock_id = dfu.file_to_shock({'file_path': output_dir,
                                            'pack': 'zip'})['shock_id']

        html_file = {
            'shock_id': report_shock_id,
            'name': 'index.html',
            'label': 'index.html',
            'description': 'HTMLL report for GSEA'
            }
        
        report_info = report.create_extended_report({
                        'direct_html_link_index': 0,
                        'html_links': [html_file],
                        'report_object_name': report_name,
                        'workspace_name': workspace_name
                    })
        return {
            'report_name': report_info['name'],
            'report_ref': report_info['ref']
        }


