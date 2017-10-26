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

set SEV(src) chip_finish_icc
set SEV(dst) focal_opt_icc

set SEV(script_file) [info script]

source ./scripts/common_setting/lcrm_setup/lcrm_setup.tcl

sproc_script_start
source -echo ./scripts/common_setting/icc_setup.tcl 
set ICC_FOCAL_OPT_STARTING_CEL $SEV(src) 
set ICC_FOCAL_OPT_CEL $SEV(dst) 

###################################################
## focal_opt_icc: focal_opt
###################################################




open_mw_lib $MW_DESIGN_LIBRARY
redirect /dev/null "remove_mw_cel -version_kept 0 ${ICC_FOCAL_OPT_CEL}"
copy_mw_cel -from $ICC_FOCAL_OPT_STARTING_CEL -to $ICC_FOCAL_OPT_CEL
open_mw_cel $ICC_FOCAL_OPT_CEL


source -echo common_optimization_settings_icc.tcl
source -echo common_placement_settings_icc.tcl
source -echo common_post_cts_timing_settings.tcl



########################################
#    LOAD THE ROUTE AND SI SETTINGS    #
########################################

source -echo common_route_si_settings_zrt_icc.tcl


#############################
## COMPLETE POWER CONNECTIONS
#############################

 check_mv_design -verbose

if { [check_error -verbose] != 0} { echo "SCRIPT-Error, flagging ..." }
## focal_opt allows you to optimize a specific subset of post route violations for setup/hold/drc
## these violating endpoints can be provided via a simple ascii file, e.g. :
##          I_STACK_TOP/I3_STACK_MEM/Stack_Mem_reg_2__1_/D
## execute man focal_opt to find additional options

## Following variable can be set to improve correlation of hold time violations versus PTSI
## This variable will increase the runtime of post route analysis and optimization
# set_app_var si_use_partial_grounding_for_min_analysis true

 if {[file exists [which $ICC_FOCAL_OPT_HOLD_VIOLS]]} {
   focal_opt -hold_endpoints $ICC_FOCAL_OPT_HOLD_VIOLS
 } else {
   focal_opt -hold_endpoints all
   }

 if {[file exists [which $ICC_FOCAL_OPT_SETUP_VIOLS]]} {
   focal_opt -setup_endpoints $ICC_FOCAL_OPT_SETUP_VIOLS
 } else {
   focal_opt -setup_endpoints all
   }

 if {[file exists [which $ICC_FOCAL_OPT_DRC_NET_VIOLS]]} {
   focal_opt -drc_nets $ICC_FOCAL_OPT_DRC_NET_VIOLS   
 } else {
   focal_opt -drc_nets all
   }

 if {[file exists [which $ICC_FOCAL_OPT_DRC_PIN_VIOLS]]} {
   focal_opt -drc_pins $ICC_FOCAL_OPT_DRC_PIN_VIOLS   
 } else {
   focal_opt -drc_pins all
   }

 if {[file exists [which $ICC_FOCAL_OPT_XTALK_VIOLS]]} {
   focal_opt -xtalk_reduction $ICC_FOCAL_OPT_XTALK_VIOLS   
 }


if {$ICC_REPORTING_EFFORT != "OFF" } {
  redirect -tee -file $REPORTS_DIR_FOCAL_OPT/$ICC_FOCAL_OPT_CEL.qor {report_qor}
  redirect -tee -file $REPORTS_DIR_FOCAL_OPT/$ICC_FOCAL_OPT_CEL.qor -append {report_qor -summary}
  redirect -file $REPORTS_DIR_FOCAL_OPT/$ICC_FOCAL_OPT_CEL.con {report_constraints}
}

if {$ICC_REPORTING_EFFORT != "OFF" } {
     redirect -tee -file $REPORTS_DIR_FOCAL_OPT/$ICC_FOCAL_OPT_CEL.clock_tree {report_clock_tree -summary}     ;# global skew report
     redirect -file $REPORTS_DIR_FOCAL_OPT/$ICC_FOCAL_OPT_CEL.clock_timing {report_clock_timing -type skew} ;# local skew report
}
if {$ICC_REPORTING_EFFORT != "OFF" } {
 redirect -file $REPORTS_DIR_FOCAL_OPT/$ICC_FOCAL_OPT_CEL.max.tim {report_timing -crosstalk_delta -capacitance -transition_time -input_pins -nets -delay max} 
 redirect -file $REPORTS_DIR_FOCAL_OPT/$ICC_FOCAL_OPT_CEL.min.tim {report_timing -crosstalk_delta -capacitance -transition_time -input_pins -nets -delay min} 
}
if {$ICC_REPORTING_EFFORT != "OFF" } {
 redirect -tee -file $REPORTS_DIR_FOCAL_OPT/$ICC_FOCAL_OPT_CEL.sum {report_design_physical -all -verbose}
}

save_mw_cel -as $ICC_FOCAL_OPT_CEL


## Create Snapshot and Save

if {$ICC_REPORTING_EFFORT != "OFF" } {
 create_qor_snapshot -name $ICC_FOCAL_OPT_CEL
 redirect -file $REPORTS_DIR_FOCAL_OPT/$ICC_FOCAL_OPT_CEL.qor_snapshot.rpt {report_qor_snapshot -no_display}
}


# Lynx compatible procedure which produces design metrics based on reports
sproc_generate_metrics

# Lynx Compatible procedure which performs final metric processing and exits
sproc_script_stop
