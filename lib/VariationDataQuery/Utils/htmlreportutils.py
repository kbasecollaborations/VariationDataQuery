import uuid
from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.KBaseReportClient import KBaseReport

class htmlreportutils:
    def __init__(self):
        pass

    def create_table(self, filename, output_dir):

        id = filename.split(".")[0]

        htmlout = "<table id=\"" + id + "\" class=\"table table-striped table-bordered\" style=\"width:100%\">"

        with open (output_dir + "/" + filename) as file:
            lines = file.readlines()
            htmlout += "<thead><tr>"
            header = lines[0]
            hrow = header.split("\t")
            for k in range(0, len(hrow)):
                htmlout += "<th>" + hrow[k] + "</th>"
            htmlout += "</tr></thead>"

            htmlout += "<tbody>"
            counter = 0
            for line in lines:
                rows = line.split("\t")
                if (counter != 0):
                    htmlout += "<tr>"
                    for i in range(0,len(rows)):
                        htmlout += "<td>" + rows[i] + "</td>"
                    htmlout += "</tr>"
                counter = counter + 1


            htmlout += "</tbody><tfoot><tr>"
            hrows = header.split("\t")
            for j in range(0, len(hrows)):
                htmlout += "<th>" + hrows[j] + "</th>"
        htmlout += "</tr></tfoot></table>"
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
        output += "<script> $(document).ready(function() {$(\'#variants\').DataTable();} ); </script></heade>"
        output += ""

        output += self.create_table(filename, output_dir)
        return output

    def create_html_report(self, callback_url, output_dir, workspace_name):
        '''
         function for creating html report
        '''

        dfu = DataFileUtil(callback_url)
        report_name = 'kb_variant_report_' + str(uuid.uuid4())
        report = KBaseReport(callback_url)
        index_file_path = output_dir + "/variants.tsv"
        htmlstring = self.create_enrichment_report("variants.tsv", output_dir)

        try:
            with open(output_dir +"/index.html" , "w") as html_file:

               html_file.write(htmlstring + "</body></html><br><br><br>" +"\n")
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


