# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os
import uuid
from VariationDataQuery.Utils.vcf_parser import vcf_parser
from VariationDataQuery.Utils.htmlreportutils import htmlreportutils
from installed_clients.KBaseReportClient import KBaseReport

#END_HEADER


class VariationDataQuery:
    '''
    Module Name:
    VariationDataQuery

    Module Description:
    A KBase module: VariationDataQuery
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = ""
    GIT_COMMIT_HASH = ""

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.shared_folder = config['scratch']
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        self.vp = vcf_parser() 
        self.hr = htmlreportutils()
        #END_CONSTRUCTOR
        pass


    def run_VariationDataQuery(self, ctx, params):
        """
        This example function accepts any number of parameters and returns results in a KBaseReport
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "ReportResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN run_VariationDataQuery

        outputdir = self.shared_folder + '/' + str(uuid.uuid1())
        os.mkdir(outputdir)
        workspace = params['workspace_name']
        coordinates = params['coordinates']

        id = 0

        coord_array = coordinates.split(",")
        for coord in coord_array:
            contig_id,start,stop = coord.split("-")
            id = id + 1
            print(contig_id + "\t" + str(start) + "\t" + str(stop))
            sample_info_file = os.path.join(self.shared_folder, "sample_names" + str(id) + ".txt")
            variants_info_file = os.path.join(self.shared_folder, "data" + str(id) + ".txt")
            self.vp.get_variants( contig_id, str(start), str(stop),  "https://appdev.kbase.us/dynserv/b8fedfd6d8a1fc10372bcbad4f152b4b6d85507b.VariationFileServ/shock/a293a557-47b3-4fcc-8bef-d2049ad6368a", "https://appdev.kbase.us/dynserv/b8fedfd6d8a1fc10372bcbad4f152b4b6d85507b.VariationFileServ/shock/f19936ff-6f66-4a44-831f-1bfcdc6e88c4", id)
            variant_file = self.vp.getjson(sample_info_file, variants_info_file, outputdir, id)
            output = self.hr.create_html_report(self.callback_url, outputdir, workspace, id)
        
        report = KBaseReport(self.callback_url)

        #END run_VariationDataQuery

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_VariationDataQuery return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
