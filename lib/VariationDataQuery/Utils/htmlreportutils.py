import uuid
import pandas as pd
from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.KBaseReportClient import KBaseReport

class htmlreportutils:
    def __init__(self):
        self.organism_dict = {}

        pass

    def create_table(self, filename, output_dir):

        id = filename.split(".")[0]

        '''try:
            data = pd.read_csv(output_dir + "/" + filename, sep='\t')
        except pd.errors.EmptyDataError:
            print(filename + ' was empty')'''

        htmlout = "<div style=\"height: 850px; width: 1800px; border: 1px ridge; black; background: #e9d8f2; " \
                       "padding-top: 20px; padding-right: 0px; padding-bottom: 20px; padding-left: 20px; " \
                       "overflow: auto;\"><table id=\"" + id + "\" class=\"table table-striped table-bordered\" style=\"width:100%\">" \
                                                               "<tbody>"

        with open (output_dir + "/" + filename) as file:
            lines = file.readlines()
            counter = 0
            header = ''
            for line in lines:
                rows = line.split("\t")


                if (counter == 0):
                    header = line
                    htmlout += "<tr><thead>"
                    for k in range(0,len(rows)):
                        htmlout += "<th>" + rows[k] + "</th>"
                    htmlout += "</thead></tr>"
                else:
                    htmlout += "<tbody><tr>"
                    for i in range(0,len(rows)):
                        htmlout += "<td>" + rows[i] + "</td>"
                    htmlout += "</tr></tbody>"
                counter = counter + 1

                htmlout += "</tr><tfoot>"
            hrows = header.split("\t")
            for j in range(0, len(hrows)):
                htmlout += "<th>" + hrows[j] + "</th>"
        htmlout += "</tfoot></table></div>"
        return htmlout

    def create_enrichment_report(self, filename, output_dir):
        '''
                function for adding enrichment score to report
        '''

        output = "<html><head><link rel=\"stylesheet\" type=\"text/css\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap" \
                 "/3.3.7/css/bootstrap.min.css\"><link rel=\"stylesheet\" type=\"text/css " \
                 "\"href=\"https://cdn.datatables.net/1.10.20/css/dataTables.bootstrap.min.css\"><script src=\"https://code.jquery.com/jquery-3.3.1.js\">" \
                 "</script><script src=\"https://cdn.datatables.net/1.10.20/js/jquery.dataTables.min.js\">" \
                 "</script><script src=\"https://cdn.datatables.net/1.10.20/js/dataTables.bootstrap.min.js\"></script>"
        output += "<script> $(document).ready(function() {$(\'#variants\').DataTable();} ); </script>"

        output += self.create_table(filename, output_dir)
        return output

    def create_html_report(self, callback_url, output_dir, workspace_name, index):
        '''
         function for creating html report
        '''

        dfu = DataFileUtil(callback_url)
        report_name = 'kb_variant_report_' + str(uuid.uuid4())
        report = KBaseReport(callback_url)

        index_file_path = output_dir + "/variants" + str(index) + ".tsv"

        htmlstring = self.create_enrichment_report("variants" + str(index) + ".tsv", output_dir)

        #htmlstring = "<a href='" + index_file_path +"'> report link </a>"

        try:
            with open(output_dir +"/index.html" , "a") as html_file:
               html_file.write("<br><br>Html Report<br><br>" +"\n")
               html_file.write(htmlstring + "<br><br><br>" +"\n")
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


