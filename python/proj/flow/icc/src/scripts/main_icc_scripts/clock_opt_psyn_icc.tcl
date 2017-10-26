
set TEV(num_cores) 1

set SEV(src) clock_opt_cts_icc
set SEV(dst) clock_opt_psyn_icc

set SEV(script_file) [info script]

source ./scripts/common_setting/lcrm_setup/lcrm_setup.tcl

sproc_script_start
source -echo ./scripts/common_setting/icc_setup.tcl 
set ICC_CLOCK_OPT_CTS_CEL $SEV(src) 
set ICC_CLOCK_OPT_PSYN_CEL $SEV(dst) 

###############################################
## clock_opt_psyn_icc: Post CTS optimization ##
###############################################
set upf_create_implicit_supply_sets false
 
open_mw_lib $MW_DESIGN_LIBRARY
redirect /dev/null "remove_mw_cel -version_kept 0 ${ICC_CLOCK_OPT_PSYN_CEL}" 
copy_mw_cel -from $ICC_CLOCK_OPT_CTS_CEL -to $ICC_CLOCK_OPT_PSYN_CEL
open_mw_cel $ICC_CLOCK_OPT_PSYN_CEL



## Optimization Common Session Options - set in all sessions
### ./scripts/common_setting/common_optimization_settings_icc.tcl
### ./scripts/common_setting/common_placement_settings_icc.tcl
source -echo common_optimization_settings_icc.tcl
source -echo common_placement_settings_icc.tcl



## Source CTS Options 
### ./scripts/common_setting/common_cts_settings_icc.tcl
source -echo common_cts_settings_icc.tcl

## Source Post CTS Options
### ./scripts/common_setting/common_post_cts_timing_settings.tcl
source -echo common_post_cts_timing_settings.tcl


set_app_var compile_instance_name_prefix icc_clock 

if { [check_error -verbose] != 0} { echo "SCRIPT-Error, flagging ..." }

extract_rc
if { [check_error -verbose] != 0} { echo "SCRIPT-Error, flagging ..." }

set clock_opt_psyn_cmd "clock_opt -no_clock_route -only_psyn -area_recovery" 
#if {$LEAKAGE_POWER || $DYNAMIC_POWER} {
   lappend clock_opt_psyn_cmd -power
#}
echo $clock_opt_psyn_cmd
eval $clock_opt_psyn_cmd
## Use -optimize_dft if you have SCANDEF and there are scan nets with hold violations.
#  Note that scan wirelength can increase and may impact QoR.

route_zrt_group -all_clock_nets -reuse_existing_global_route true -stop_after_global_route true
if { [check_error -verbose] != 0} { echo "SCRIPT-Error, flagging ..." }
############################################################################################################
# ADDITIONAL FEATURES FOR THE POST CTS OPTIMIZATION
############################################################################################################

## When the design has congestion issues post CTS, use :
# refine_placement -congestion_effort medium

## Additional optimization can be done using the psynopt command
# psynopt -effort "medium|high"


########################################
#         ANTENNA PREVENTION           #
########################################

    ## in case new nets are created that go from one VA to another, level shifters need to be inserted on these nets
    # insert_level_shifters -all_clock_nets -verbose




########################################
#           CONNECT P/G                #
########################################


## Connect Power & Ground for non-MV and MV-mode

#if {[file exists [which $CUSTOM_CONNECT_PG_NETS_SCRIPT]]} {
#  source -echo $CUSTOM_CONNECT_PG_NETS_SCRIPT
#} else {
    if {!$ICC_TIE_CELL_FLOW} {derive_pg_connection -verbose -tie}
    redirect -file $REPORTS_DIR_CLOCK_OPT_PSYN/clock_opt_psyn.mv {check_mv_design -verbose}
  #}
if { [check_error -verbose] != 0} { echo "SCRIPT-Error, flagging ..." }

#if {$ICC_REPORTING_EFFORT != "OFF" } {
 redirect -tee -file $REPORTS_DIR_CLOCK_OPT_PSYN/$ICC_CLOCK_OPT_PSYN_CEL.qor {report_qor}
 redirect -tee -file $REPORTS_DIR_CLOCK_OPT_PSYN/$ICC_CLOCK_OPT_PSYN_CEL.qor -append {report_qor -summary}
 # redirect -tee -file $REPORTS_DIR_PLACE_OPT/$ICC_CLOCK_OPT_PSYN_CEL.qor -append {report_timing_histogram -range_maximum 0}
 # redirect -tee -file $REPORTS_DIR_PLACE_OPT/$ICC_CLOCK_OPT_PSYN_CEL.qor -append {report_timing_histogram -range_minimum 0}
 redirect -file      $REPORTS_DIR_CLOCK_OPT_PSYN/$ICC_CLOCK_OPT_PSYN_CEL.con {report_constraints}
#}

if {$ICC_REPORTING_EFFORT != "OFF" } {
     redirect -tee -file $REPORTS_DIR_CLOCK_OPT_PSYN/$ICC_CLOCK_OPT_PSYN_CEL.clock_tree {report_clock_tree -summary}     ;# global skew report
     redirect -file $REPORTS_DIR_CLOCK_OPT_PSYN/$ICC_CLOCK_OPT_PSYN_CEL.clock_timing {report_clock_timing -type skew} ;# local skew report
}
if {$ICC_REPORTING_EFFORT != "OFF" } {
 redirect -file $REPORTS_DIR_CLOCK_OPT_PSYN/$ICC_CLOCK_OPT_PSYN_CEL.max.tim {report_timing -capacitance -transition_time -input_pins -nets -delay max} 
 redirect -file $REPORTS_DIR_CLOCK_OPT_PSYN/$ICC_CLOCK_OPT_PSYN_CEL.min.tim {report_timing -capacitance -transition_time -input_pins -nets -delay min} 
}
if {$ICC_REPORTING_EFFORT == "MED" && $LEAKAGE_POWER } {
 redirect -file $REPORTS_DIR_CLOCK_OPT_PSYN/$ICC_CLOCK_OPT_PSYN_CEL.power {report_power}
}

save_mw_cel -as $ICC_CLOCK_OPT_PSYN_CEL 

## Create Snapshot and Save
if {$ICC_REPORTING_EFFORT != "OFF" } {
 redirect -file $REPORTS_DIR_CLOCK_OPT_PSYN/$ICC_CLOCK_OPT_PSYN_CEL.placement_utilization.rpt {report_placement_utilization -verbose}
 create_qor_snapshot -clock_tree -name $ICC_CLOCK_OPT_PSYN_CEL
 redirect -file $REPORTS_DIR_CLOCK_OPT_PSYN/$ICC_CLOCK_OPT_PSYN_CEL.qor_snapshot.rpt {report_qor_snapshot -no_display}
}

# Lynx compatible procedure which produces design metrics based on reports
sproc_generate_metrics

# Lynx Compatible procedure which performs final metric processing and exits
sproc_script_stop
