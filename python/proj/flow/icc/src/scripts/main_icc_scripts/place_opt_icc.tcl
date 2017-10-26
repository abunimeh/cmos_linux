set TEV(num_cores) 1

set SEV(src) flat_dp
set SEV(dst) place_opt_icc

set SEV(script_file) [info script]
### ../../../scripts_block/lcrm_setup/lcrm_setup.tcl
source ./scripts/common_setting/lcrm_setup/lcrm_setup.tcl

sproc_script_start
### ../../../scripts_block/rm_setup/icc_setup.tcl
source -echo ./scripts/common_setting/icc_setup.tcl 
set ICC_FLOORPLAN_CEL $SEV(src) 
set ICC_PLACE_OPT_CEL $SEV(dst) 

set upf_create_implicit_supply_sets false

open_mw_lib $MW_DESIGN_LIBRARY
redirect /dev/null "remove_mw_cel -version_kept 0 ${ICC_PLACE_OPT_CEL}" 
copy_mw_cel -from $ICC_FLOORPLAN_CEL -to $ICC_PLACE_OPT_CEL
open_mw_cel $ICC_PLACE_OPT_CEL
## Optimization Common Session options - set in all sessions
### ./scripts/common_setting/common_optimization_settings_icc.tcl
### ./scripts/common_setting/common_placement_settings_icc.tcl
source -echo common_optimization_settings_icc.tcl 
source -echo common_placement_settings_icc.tcl 

## Source CTS Options CTS can be run during place_opt 
### ./scripts/common_setting/common_cts_settings_icc.tcl
source -echo common_cts_settings_icc.tcl 

## Set Ideal Network so place_opt doesn't buffer clock nets
## Remove before clock_opt cts
## Uncertainty handling pre-cts

  set_ideal_network [all_fanout -flat -clock_tree ]


set_app_var compile_instance_name_prefix icc_place  

  check_mv_design -verbose

#if {$DFT && !$ICC_DP_DFT_FLOW} {
  ##Read Scan Chain Information from DEF
#  if {[file exists [which $ICC_IN_SCAN_DEF_FILE]] } { 
#### ../../../rm_dc/work/dc/$DESIGN_NAME.mapped.scandef   ####
       #read_def $ICC_IN_SCAN_DEF_FILE
#  }  
#  if {[get_scan_chain] != 0} {
       #check_scan_chain
       #redirect -file $REPORTS_DIR_PLACE_OPT/scan_chain_pre_ordering.rpt {report_scan_chain}
#  }
#}

#if {$LEAKAGE_POWER} {
  set_multi_vth_constraint -reset
#}

#if {$ICC_SANITY_CHECK} {
	check_physical_design -stage pre_place_opt -no_display -output $REPORTS_DIR_CLOCK_OPT_CTS/check_physical_design.pre_place_opt
#}

if { [check_error -verbose] != 0} { echo "SCRIPT-Error, flagging ..." }

set_fix_multiple_port_nets -all -constant

###  set PLACE_OPT_EFFORT 	 "medium"  ###
set place_opt_cmd "place_opt -area_recovery -effort $PLACE_OPT_EFFORT" 

#if {$PLACE_OPT_CONGESTION} {
   lappend place_opt_cmd -congestion
#} 
#if {$DFT && [get_scan_chain] != 0} {
   lappend place_opt_cmd -optimize_dft
#}
#if {$LEAKAGE_POWER || $DYNAMIC_POWER || $ICC_LOW_POWER_PLACEMENT} {
   lappend place_opt_cmd -power
#}
echo $place_opt_cmd

####  place_opt -area_recovery -effort -congestion -optimize_dft -power  ####
eval $place_opt_cmd


if { [check_error -verbose] != 0} { echo "SCRIPT-Error, flagging ..." }

redirect -file $REPORTS_DIR_PLACE_OPT/place_opt.mv {check_mv_design -verbose}

########################################
#           CONNECT P/G                #
########################################


## Connect Power & Ground for non-MV and MV-mode

#if {[file exists [which $CUSTOM_CONNECT_PG_NETS_SCRIPT]]} {
#  source -echo $CUSTOM_CONNECT_PG_NETS_SCRIPT
#} else {
#   if {!$ICC_TIE_CELL_FLOW} {
      derive_pg_connection -verbose -tie
#   }
   redirect -file $REPORTS_DIR_PLACE_OPT/place_opt.mv {check_mv_design -verbose}
#}
if { [check_error -verbose] != 0} { echo "SCRIPT-Error, flagging ..." }
#if {$ICC_TIE_CELL_FLOW} { 
  echo "SCRIPT-Info : List of TIE-CELL instances in your design :"
  all_tieoff_cells
#} else { report_tie_nets
#  }

#  if {$ICC_REPORTING_EFFORT != "OFF" } {
#   redirect -file $REPORTS_DIR_PLACE_OPT/$ICC_PLACE_OPT_CEL.max.tim {report_timing -capacitance -transition_time -input_pins -nets -delay max}
#   redirect -file $REPORTS_DIR_PLACE_OPT/$ICC_PLACE_OPT_CEL.min.tim {report_timing -capacitance -transition_time -input_pins -nets -delay min}
#  }
#  if {$ICC_REPORTING_EFFORT == "MED" && $LEAKAGE_POWER } {
   redirect -file $REPORTS_DIR_PLACE_OPT/$ICC_PLACE_OPT_CEL.power {report_power}
#  }

save_mw_cel -as $ICC_PLACE_OPT_CEL  


## Create Snapshot and Save
#  if {$ICC_REPORTING_EFFORT != "OFF" } {
    redirect -file $REPORTS_DIR_PLACE_OPT/$ICC_PLACE_OPT_CEL.placement_utilization.rpt {report_placement_utilization -verbose}
    create_qor_snapshot -name $ICC_PLACE_OPT_CEL
    redirect -file $REPORTS_DIR_PLACE_OPT/$ICC_PLACE_OPT_CEL.qor_snapshot.rpt {report_qor_snapshot -no_display} 
    redirect -tee -file $REPORTS_DIR_PLACE_OPT/$ICC_PLACE_OPT_CEL.qor {report_qor}
    redirect -tee -file $REPORTS_DIR_PLACE_OPT/$ICC_PLACE_OPT_CEL.qor -append {report_qor -summary}
    # redirect -tee -file $REPORTS_DIR_PLACE_OPT/$ICC_PLACE_OPT_CEL.qor -append {report_timing_histogram -range_maximum 0}
    # redirect -tee -file $REPORTS_DIR_PLACE_OPT/$ICC_PLACE_OPT_CEL.qor -append {report_timing_histogram -range_minimum 0}
    redirect -file $REPORTS_DIR_PLACE_OPT/$ICC_PLACE_OPT_CEL.con {report_constraints}
#  }
 

# Lynx compatible procedure which produces design metrics based on reports
sproc_generate_metrics

# Lynx Compatible procedure which performs final metric processing and exits
sproc_script_stop
