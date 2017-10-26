##########################################################################################
# Version: E-2010.12 (January 10, 2011)
# Copyright (C) 2007-2011 Synopsys, Inc. All rights reserved.
##########################################################################################

#################################################################################
# Lynx Compatible Setup : Overview
#
# This LCRM script contains support for running standalone or within the Lynx
# Design System without change. Note that Lynx is not required to run standalone.
#
# Features available when running within Lynx Design System include:
#
# * Graphical flow configuration and execution monitoring
# * Tool setup and version management
# * Job distribution handling
# * Visual execution status and error checking
# * Design and System metric capture for analysis in Lynx Manager Cockpit
#################################################################################

#################################################################################
# Lynx Compatible Setup : Task Environment Variables (TEV)
#
# Task Environment Variables allow configuration of this tool script.
# The Lynx Design System will automatically recognize the TEV definitions
# in this script and make them visible for configuration in the Lynx Design
# System graphical user interface.
#################################################################################

## NAME: TEV(num_cores)
## TYPE: integer
## INFO:
## * Specifies the number of cores to be used for multicore optimization.
## * Use a value of 1 to indicate single-core optimization (default).
set TEV(num_cores) 1

#################################################################################
# Lynx Compatible Setup : Script Initialization
#
# This section is used to initialize the scripts for use with the Lynx Design
# System.  Users should not make modifications to this section.
#################################################################################

set SEV(src) route_opt_icc
set SEV(dst) chip_finish_icc

set SEV(script_file) [info script]

source ./scripts/common_setting/lcrm_setup/lcrm_setup.tcl

sproc_script_start
source -echo ./scripts/common_setting/icc_setup.tcl 
set ICC_ROUTE_OPT_CEL $SEV(src) 
set ICC_CHIP_FINISH_CEL $SEV(dst) 

###################################################
## chip_finish_icc: Several chipfinishing steps  ##
###################################################




open_mw_lib $MW_DESIGN_LIBRARY
redirect /dev/null "remove_mw_cel -version_kept 0 ${ICC_CHIP_FINISH_CEL}"
copy_mw_cel -from $ICC_ROUTE_OPT_CEL -to $ICC_CHIP_FINISH_CEL
open_mw_cel $ICC_CHIP_FINISH_CEL


source -echo common_optimization_settings_icc.tcl
source -echo common_placement_settings_icc.tcl
source -echo common_post_cts_timing_settings.tcl



########################################
#    LOAD THE ROUTE AND SI SETTINGS    #
########################################

source -echo common_route_si_settings_icc.tcl


#############################
## COMPLETE POWER CONNECTIONS
#############################

 check_mv_design -verbose

if { [check_error -verbose] != 0} { echo "SCRIPT-Error, flagging ..." }
if {$ICC_FIX_ANTENNA } {

  ########################################
  #           ANTENNA FIXING             #
  ########################################
  
  ## do antenna fixing during seach&repair
   if { [file exists [which $ANTENNA_RULES_FILE]]} {
       set_droute_options -name doAntennaConx -value 4
       source -echo $ANTENNA_RULES_FILE
       report_antenna_rules
       route_search_repair -rerun_drc -loop 10
       report_antenna_ratio
   }


   if { $ICC_USE_DIODES && [file exists [which $ANTENNA_RULES_FILE]] && $ICC_ROUTING_DIODES != "" } {
       insert_diode -no_auto_cell_selection -diode_cells $ICC_ROUTING_DIODES 
       route_search_repair -rerun_drc -loop 3
       report_antenna_ratio

   }




   if { [check_error -verbose] != 0} { echo "SCRIPT-Error, flagging ..." }
}
  

if {$ICC_REDUCE_CRITICAL_AREA } {

  ########################################
  #      CRITICAL AREA REDUCTION          #
  ########################################
  
  ## Timing driven wire spreading for shorts and widening for opens
  ## It is recommended to define a slack threshold to avoid that nets with too small slack are touched
  ## the unit of $TIMING_PRESERVE_SLACK_SETUP and $TIMING_PRESERVE_SLACK_HOLD is the library unit, so make sure that you provide the correct
  ## values in case your library has ps as unit. Default are 0.1 and 0, i.e. 0.1ns and 0ns, respectively.
  route_spreadwires -timing_driven -setup_slack_threshold $TIMING_PRESERVE_SLACK_SETUP -search_repair_loop 3
  route_widen_wire -timing_driven -setup_slack_threshold $TIMING_PRESERVE_SLACK_SETUP -hold_slack_threshold $TIMING_PRESERVE_SLACK_HOLD -search_repair_loop 3
  if { [check_error -verbose] != 0} { echo "SCRIPT-Error, flagging ..." }
}
  
if {$ICC_DBL_VIA } {

  ########################################
  #           REDUNDANT VIA              #
  ########################################
  
  ## Running Timing driven redundant via insertion
  set_app_var droute_optViaTimingDriven 1
  
  ## Auto mode
  insert_redundant_vias -auto_mode insert -num_cpus $ICC_NUM_CPUS

  
  ## Optionally, manual mode
  # insert_redundant_vias \
          #-num_cpus $ICC_NUM_CPUS \
          #-from_via "from_via_list" \
          #-to_via "to_via_list" \
          #-to_via_x_size "list_of_via_x_sizes" \
          #-to_via_y_size "list_of_via_y_sizes"
  
          ##example: -from_via "VIA45 VIA45 VIA12A" -to_via "VIA45f VIA45 VIA12f" -to_via_x_size "1 1 1" -to_via_y_size "2 2 2"
  
 if { [check_error -verbose] != 0} { echo "SCRIPT-Error, flagging ..." }
}
  ########################################
  #          AUTO SHIELDING              #
  ########################################
## Generate shieldign wires for clocks (if not done in clock_opt_route_icc step) or selected signal nets  
#  create_auto_shield
#  set_extraction_options -virtual_shield_extraction false
  
if {$ADD_FILLER_CELL } {

  ########################################
  #          STD CELL FILLERS            #
  ########################################
  
##Filler Cells
    source insert_mv_filler_cells.tcl


if { [check_error -verbose] != 0} { echo "SCRIPT-Error, flagging ..." }

}
  
if {$ICC_FIX_ANTENNA || $ICC_REDUCE_CRITICAL_AREA || $ICC_DBL_VIA || $ADD_FILLER_CELL } {

  ########################################
  #     INCREMENTAL TIMING OPTO          #
  ########################################
  
  route_opt -incremental -size_only

  ##include -rerun_drc to ensure DRC count is correct
  route_search_repair -rerun_drc -num_cpus 1 -loop 2  
  if { [check_error -verbose] != 0} { echo "SCRIPT-Error, flagging ..." }

}
if {$ADD_FILLER_CELL } {

  ########################################
  #          STD CELL FILLERS            #
  ########################################
  
##Filler Cells
   source insert_mv_filler_cells.tcl


if { [check_error -verbose] != 0} { echo "SCRIPT-Error, flagging ..." }

}
  
  
    ## in case new nets are created that go from one VA to another, level shifters need to be inserted on these nets 
    # insert_level_shifters -all_clock_nets -verbose
if {$ICC_FIX_SIGNAL_EM} {
## Signal EM
#  All details of the ICC Signal EM flow can be found here :
#  https://solvnet.synopsys.com/retrieve/023849.html
#
#  Loading EM constraint is required for EM analysis and fixing. 
#  It can be in plib or ALF format.
#     ex, set_mw_technology_file -plib plib_file_name.plib $MW_DESIGN_LIBRARY  
#     ex, set_mw_technology_file -alf alf_file_name $MW_DESIGN_LIBRARY 
#  Loading and setting switching activity steps are optional.
#     ex, read_saif -input your_switching.saif
#     ex, set_switching_activity -toggle_rate <positive number> -static_probability <0to1> [get_nets -hier *]
#  To fix signal EM, please uncomment the following commands (after route_opt is completed)
#     propagate_switching_activity 
#     fix_signal_em
}
########################################
#           CONNECT P/G                #
########################################


## Connect Power & Ground for non-MV and MV-mode

 if {[file exists [which $CUSTOM_CONNECT_PG_NETS_SCRIPT]]} {
   source -echo $CUSTOM_CONNECT_PG_NETS_SCRIPT
 } else {
    if {!$ICC_TIE_CELL_FLOW} {derive_pg_connection -verbose -tie}
    redirect -file $REPORTS_DIR_CHIP_FINISH/chip_finish.mv {check_mv_design -verbose}
   }
if { [check_error -verbose] != 0} { echo "SCRIPT-Error, flagging ..." }

  redirect -file $REPORTS_DIR_CHIP_FINISH/${ICC_CHIP_FINISH_CEL}.mv {check_mv_design -verbose}
  save_upf $RESULTS_DIR/${ICC_CHIP_FINISH_CEL}.upf  
if {$ICC_REPORTING_EFFORT != "OFF" } {
  redirect -tee -file $REPORTS_DIR_CHIP_FINISH/$ICC_CHIP_FINISH_CEL.qor {report_qor}
  redirect -tee -file $REPORTS_DIR_CHIP_FINISH/$ICC_CHIP_FINISH_CEL.qor -append {report_qor -summary}
  redirect -file $REPORTS_DIR_CHIP_FINISH/$ICC_CHIP_FINISH_CEL.con {report_constraints}
}

if {$ICC_REPORTING_EFFORT != "OFF" } {
     redirect -tee -file $REPORTS_DIR_CHIP_FINISH/$ICC_CHIP_FINISH_CEL.clock_tree {report_clock_tree -summary}     ;# global skew report
     redirect -file $REPORTS_DIR_CHIP_FINISH/$ICC_CHIP_FINISH_CEL.clock_timing {report_clock_timing -type skew} ;# local skew report
}
if {$ICC_REPORTING_EFFORT != "OFF" } {
 redirect -file $REPORTS_DIR_CHIP_FINISH/$ICC_CHIP_FINISH_CEL.max.tim {report_timing -crosstalk_delta -capacitance -transition_time -input_pins -nets -delay max} 
 redirect -file $REPORTS_DIR_CHIP_FINISH/$ICC_CHIP_FINISH_CEL.min.tim {report_timing -crosstalk_delta -capacitance -transition_time -input_pins -nets -delay min} 
}
if {$ICC_REPORTING_EFFORT != "OFF" } {
 redirect -tee -file $REPORTS_DIR_CHIP_FINISH/$ICC_CHIP_FINISH_CEL.sum {report_design_physical -all -verbose}
}

save_mw_cel -as $ICC_CHIP_FINISH_CEL


## Create Snapshot and Save

if {$ICC_REPORTING_EFFORT != "OFF" } {
 create_qor_snapshot -name $ICC_CHIP_FINISH_CEL
 redirect -file $REPORTS_DIR_CHIP_FINISH/$ICC_CHIP_FINISH_CEL.qor_snapshot.rpt {report_qor_snapshot -no_display}
}


# Lynx compatible procedure which produces design metrics based on reports
sproc_generate_metrics

# Lynx Compatible procedure which performs final metric processing and exits
sproc_script_stop
