
do {{qs_file}};
cdc run -d {{design_top}};
cdc generate report cdc_detail.rpt;
exit
