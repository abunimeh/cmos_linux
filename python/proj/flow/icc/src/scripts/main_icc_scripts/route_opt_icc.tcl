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

set SEV(src) route_icc
set SEV(dst) route_opt_icc

set SEV(script_file) [info script]

source ./scripts/common_setting/lcrm_setup/lcrm_setup.tcl

sproc_script_start
source -echo ./scripts/common_setting/icc_setup.tcl 
set ICC_ROUTE_CEL $SEV(src) 
set ICC_ROUTE_OPT_CEL $SEV(dst) 

############################################
## route_opt_icc: Post Route optimization ##
############################################



set upf_create_implicit_supply_sets false
open_mw_lib $MW_DESIGN_LIBRARY
redirect /dev/null "remove_mw_cel -version_kept 0 ${ICC_ROUTE_OPT_CEL}"
copy_mw_cel -from $ICC_ROUTE_CEL -to $ICC_ROUTE_OPT_CEL
open_mw_cel $ICC_ROUTE_OPT_CEL



source -echo common_optimization_settings_icc.tcl
source -echo common_placement_settings_icc.tcl
source -echo common_post_cts_timing_settings.tcl

## Load the route and si settings
source -echo common_route_si_settings_icc.tcl



##############################
## RP : Relative Placement  ##     
##############################
## Ensuring that the RP cells are not changed during clock_opt
#set_rp_group_options [all_rp_groups] -route_opt_option fixed_placement
#set_rp_group_options [all_rp_groups] -route_opt_option "size_only"


if { [check_error -verbose] != 0} { echo "SCRIPT-Error, flagging ..." }
if {$LEAKAGE_POWER} {
  # The following is not needed if already set in place_opt_icc step: 
  # set_multi_vth_constraint -reset

  ############################################################
  # %LVT leakage optimization flow (edit before using it)
  ############################################################
  # For limiting the number of low Vth cells in the design, set a multithreshold
  # voltage constraint. This is a faster flow than the default leakage
  # optimization flow, and does not use the leakage power values in the library.

  # Edit the following to set the threshold voltage groups in the libraries.
  # Please use the same settings as used in place_opt_icc step.
  # set_attribute <my_hvt_lib> default_threshold_voltage_group HVT -type string
  # set_attribute <my_lvt_lib> default_threshold_voltage_group LVT -type string

  # If pre-existing, the <percent value> of set_multi_vth_constraint will be inherited 
  # from previous ICC step where it was last set. 
  # If needed, edit the following to set a differnt <percent value>
  # set_multi_vth_constraint -lvth_groups { LVT } -lvth_percentage <percent value>
}

## start the post route optimization
set_app_var compile_instance_name_prefix icc_route_opt
set_route_mode_options -zroute true

if {$ICC_SANITY_CHECK} {
	check_physical_design -stage pre_route_opt -no_display -output check_physical_design.pre_route_opt
}

if { [check_error -verbose] != 0} { echo "SCRIPT-Error, flagging ..." }

if {$ICC_ENABLE_CHECKPOINT} {
echo "SCRIPT-Info : Please ensure there's enough disk space before enabling the set_checkpoint_strategy feature."
set_checkpoint_strategy -enable -overwrite
# The -overwrite option is used by default. Remove it if needed.
}

set route_opt_cmd "route_opt -skip_initial_route -effort $ROUTE_OPT_EFFORT -xtalk_reduction" 

## route_opt -power performs both power aware optimization (PAO) and power recovery (PR).
#  If only PAO is desired and not PR, then please do the following:
#  1. set_route_opt_strategy power_aware_optimization true
#  2. comment out the line below (-power is not needed)
if {$LEAKAGE_POWER} {lappend route_opt_cmd -power}

echo $route_opt_cmd
eval $route_opt_cmd

if {$ICC_ENABLE_CHECKPOINT} {set_checkpoint_strategy -disable}

########################################
#   ADDITIONAL ROUTE_OPT FEATURES      #
########################################

## Additional Max_transition fixing :
#  By default, route_opt will prioritize WNS and TNS over DRC ( e.g. max_tran fixing). If you want to 
#  change this behavior, and give top priority to the DRC fixing, you need to set the variable below.
#  Keep in mind : this variable, only works with the -only_design_rule swich in route_opt itself.
#  violations.
#  set_app_var routeopt_drc_over_timing true
#  route_opt -effort high -incremental -only_design_rule

## Optimizing wirelenght and vias . Add the switch : -optimize_wire_via to the route_opt command :
#   route_opt -optimize_wire_via -effort low -xtalk_reduction 

## Improving QoR after the default route_opt run : 
#   route_opt -inc

## Limiting route_opt to specific optimization steps :
#   route_opt -size_only : do not insert buffers or move cells : limits the disturbance to the design
#   route_opt -only_xtalk_reduction : run only the Xtalk reduction engine
#   route_opt -only_hold_time : run only the Hold fixing engine
#   route_opt -(only_)wire_size : runs the wire size engine, that fixis timing violations by applying 
#                                 NDR's created by define_routing_rule

## Running size_only but still allowing buffers to be inserted for hold fixing :
#  set_app_var routeopt_allow_min_buffer_with_size_only true

if { [check_error -verbose] != 0} { echo "SCRIPT-Error, flagging ..." }
    ## in case new nets are created that go from one VA to another, level shifters need to be inserted on these nets
    # insert_level_shifters -all_clock_nets -verbose
########################################
#           CONNECT P/G                #
########################################


## Connect Power & Ground for non-MV and MV-mode

 if {[file exists [which $CUSTOM_CONNECT_PG_NETS_SCRIPT]]} {
   source -echo $CUSTOM_CONNECT_PG_NETS_SCRIPT
 } else {
    if {!$ICC_TIE_CELL_FLOW} {derive_pg_connection -verbose -tie}
    redirect -file $REPORTS_DIR_ROUTE_OPT/route_opt.mv {check_mv_design -verbose}
   }
if { [check_error -verbose] != 0} { echo "SCRIPT-Error, flagging ..." }
if {$ICC_REPORTING_EFFORT != "OFF" } {
 redirect -tee -file $REPORTS_DIR_ROUTE_OPT/$ICC_ROUTE_OPT_CEL.qor {report_qor}
 redirect -tee -file $REPORTS_DIR_ROUTE_OPT/$ICC_ROUTE_OPT_CEL.qor -append {report_qor -summary}
 # redirect -tee -file $REPORTS_DIR_PLACE_OPT/$ICC_ROUTE_OPT_CEL.qor -append {report_timing_histogram -range_maximum 0}
 # redirect -tee -file $REPORTS_DIR_PLACE_OPT/$ICC_ROUTE_OPT_CEL.qor -append {report_timing_histogram -range_minimum 0}
 redirect -file $REPORTS_DIR_ROUTE_OPT/$ICC_ROUTE_OPT_CEL.con {report_constraints}
}

if {$ICC_REPORTING_EFFORT != "OFF" } {
     redirect -tee -file $REPORTS_DIR_ROUTE_OPT/$ICC_ROUTE_OPT_CEL.clock_tree {report_clock_tree -summary}     ;# global skew report
     redirect -file $REPORTS_DIR_ROUTE_OPT/$ICC_ROUTE_OPT_CEL.clock_timing {report_clock_timing -type skew} ;# local skew report
}
if {$ICC_REPORTING_EFFORT != "OFF" } {
 redirect -file $REPORTS_DIR_ROUTE_OPT/$ICC_ROUTE_OPT_CEL.max.tim {report_timing -crosstalk_delta -capacitance -transition_time -input_pins -nets -delay max}
 redirect -file $REPORTS_DIR_ROUTE_OPT/$ICC_ROUTE_OPT_CEL.min.tim {report_timing -crosstalk_delta -capacitance -transition_time -input_pins -nets -delay min}
}
if {$ICC_REPORTING_EFFORT == "MED" && $LEAKAGE_POWER } {
 redirect -file $REPORTS_DIR_ROUTE_OPT/$ICC_ROUTE_OPT_CEL.power {report_power}
}
derive_pg_connection -power_net VDD -power_pin VDD -ground_net GND -ground_pin GND
save_mw_cel -as $ICC_ROUTE_OPT_CEL
## Create Snapshot and Save
if {$ICC_REPORTING_EFFORT != "OFF" } {
 create_qor_snapshot -name $ICC_ROUTE_OPT_CEL
 redirect -file $REPORTS_DIR_ROUTE_OPT/$ICC_ROUTE_OPT_CEL.qor_snapshot.rpt {report_qor_snapshot -no_display}
}
if {[file exists [which $ICC_SIGNOFF_OPT_CHECK_CORRELATION_POSTROUTE_SCRIPT]]} { 
  source $ICC_SIGNOFF_OPT_CHECK_CORRELATION_POSTROUTE_SCRIPT 
}

# Lynx compatible procedure which produces design metrics based on reports
sproc_generate_metrics

# Lynx Compatible procedure which performs final metric processing and exits
sproc_script_stop
