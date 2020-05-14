/*
A KBase module: VariationDataQuery
*/

module VariationDataQuery {
    typedef structure {
        string report_name;
        string report_ref;
    } ReportResults;

    /*
        This example function accepts any number of parameters and returns results in a KBaseReport
    */

    typedef structure {
      list<string> input_contig_ids;
      string workspace_name;
      list <string> coordinates;
      string variation_object_name;
    } InputParams;
    funcdef run_VariationDataQuery(InputParams params) returns (ReportResults output) authentication required;

};
