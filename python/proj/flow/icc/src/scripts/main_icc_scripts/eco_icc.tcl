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

set SEV(src) metal_fill_icc
set SEV(dst) eco_icc

set SEV(script_file) [info script]

source ./scripts/common_setting/lcrm_setup/lcrm_setup.tcl

sproc_script_start
source -echo ./scripts/common_setting/icc_setup.tcl 
set ICC_ECO_STARTING_CEL $SEV(src) 
set ICC_ECO_CEL $SEV(dst) 

#######################################
####ECO Script
#######################################




##Open Design
open_mw_lib $MW_DESIGN_LIBRARY

redirect /dev/null "remove_mw_cel -version_kept 0 $ICC_ECO_CEL"
copy_mw_cel -from $ICC_ECO_STARTING_CEL -to $ICC_ECO_CEL
open_mw_cel $ICC_ECO_CEL




source -echo common_optimization_settings_icc.tcl
source -echo common_placement_settings_icc.tcl
source -echo common_post_cts_timing_settings.tcl
source -echo common_route_si_settings_icc.tcl



if {$ICC_ECO_FLOW == "UNCONSTRAINED"} {

 echo "SCRIPT-Info: starting the unconstrained ECO flow, executing the ECO steps"

 if {[file exists [which $ICC_ECO_NETLIST]]} {
   eco_netlist -compare_pg -by_verilog_file $ICC_ECO_NETLIST
   legalize_placement -eco -incremental
   route_eco
 } else {
   echo "SCRIPT-Error - can't perform eco, eco netlist $ICC_ECO_NETLIST can't be found ..."
 }
}



if {$ICC_ECO_FLOW == "FREEZE_SILICON"} {

 echo "SCRIPT-Info: starting the Freeze Silicon ECO flow, executing the ECO steps"

 if {[file exists [which $ICC_ECO_NETLIST]]} {
   eco_netlist -compare_pg -freeze_silicon -by_verilog_file $ICC_ECO_NETLIST
   place_freeze_silicon
   route_eco
 } else {
   echo "SCRIPT-Error - can't perform eco, eco netlist $ICC_ECO_NETLIST can't be found ..."
 }
}



########################################
#           CONNECT P/G                #
########################################


## Connect Power & Ground for non-MV and MV-mode

 if {[file exists [which $CUSTOM_CONNECT_PG_NETS_SCRIPT]]} {
   source -echo $CUSTOM_CONNECT_PG_NETS_SCRIPT
 } else {
    if {!$ICC_TIE_CELL_FLOW} {derive_pg_connection -verbose -tie}
    redirect -file $REPORTS_DIR_ECO/route.mv {check_mv_design -verbose}
   }
if { [check_error -verbose] != 0} { echo "SCRIPT-Error, flagging ..." }
if {$ICC_REPORTING_EFFORT != "OFF" } {
    redirect -tee -file $REPORTS_DIR_ECO/$ICC_ECO_CEL.clock_tree {report_clock_tree -summary}     ;# global skew report
    redirect -file $REPORTS_DIR_ECO/$ICC_ECO_CEL.clock_timing {report_clock_timing -type skew} ;# local skew report
}
if {$ICC_REPORTING_EFFORT != "OFF" } {
 redirect -tee -file $REPORTS_DIR_ECO/$ICC_ECO_CEL.qor {report_qor}
 redirect -tee -file $REPORTS_DIR_ECO/$ICC_ECO_CEL.qor -append {report_qor -summary}
 redirect -file $REPORTS_DIR_ECO/$ICC_ECO_CEL.con {report_constraints}
}
if {$ICC_REPORTING_EFFORT != "OFF" } {
 redirect -file $REPORTS_DIR_ECO/$ICC_ECO_CEL.max.tim {report_timing -capacitance -transition_time -input_pins -nets -delay max} 
 redirect -file $REPORTS_DIR_ECO/$ICC_ECO_CEL.min.tim {report_timing -capacitance -transition_time -input_pins -nets -delay min} 
}

save_mw_cel -as $ICC_ECO_CEL

if {$ICC_REPORTING_EFFORT != "OFF" } {
  create_qor_snapshot -clock_tree -name $ICC_ECO_CEL
  redirect -file $REPORTS_DIR_ECO/$ICC_ECO_CEL.qor_snapshot.rpt {report_qor_snapshot -no_display}
}




# Lynx compatible procedure which produces design metrics based on reports
sproc_generate_metrics

# Lynx Compatible procedure which performs final metric processing and exits
sproc_script_stop
