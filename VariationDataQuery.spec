/*
A KBase module: VariationDataQuery
*/

module VariationDataQuery {
    typedef structure {
        string report_name;
        string report_ref;
    } ReportResults;

    typedef structure {
      string workspace_name;
      string coordinates;
      string variation_object_name;
    } InputParams;
    funcdef run_VariationDataQuery(InputParams params) returns (ReportResults output) authentication required;
};
