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

set SEV(src) signoff_opt_icc
set SEV(dst) metal_fill_icc

set SEV(script_file) [info script]

source ./scripts/common_setting/lcrm_setup/lcrm_setup.tcl

sproc_script_start
source -echo ./scripts/common_setting/icc_setup.tcl 
set ICC_SIGNOFF_OPT_CEL $SEV(src) 
set ICC_METAL_FILL_CEL $SEV(dst) 

###################################################
## chip_finish_icc: Several chipfinishing steps  ##
###################################################




open_mw_lib $MW_DESIGN_LIBRARY
redirect /dev/null "remove_mw_cel -version_kept 0 ${ICC_METAL_FILL_CEL}"

  copy_mw_cel -from $ICC_SIGNOFF_OPT_CEL -to $ICC_METAL_FILL_CEL 

open_mw_cel $ICC_METAL_FILL_CEL



source -echo common_optimization_settings_icc.tcl
source -echo common_placement_settings_icc.tcl
source -echo common_post_cts_timing_settings.tcl
source -echo common_route_si_settings_zrt_icc.tcl 



#############################
## COMPLETE POWER CONNECTIONS
#############################

 check_mv_design -verbose

if { [check_error -verbose] != 0} { echo "SCRIPT-Error, flagging ..." }

if {$ADD_METAL_FILL != "NONE" } {

  ########################################
  #     REAL METAL FILL EXTRACTION       #
  ########################################

  ## Can be set to FLOATING|GROUNDED when required - default  = AUTO
  set_extraction_options -real_metalfill_extraction FLOATING

  if { [check_error -verbose] != 0} { echo "SCRIPT-Error, flagging ..." }
}
save_mw_cel -as $ICC_METAL_FILL_CEL

if {$ADD_METAL_FILL == "ICC"} {

  ########################################
  #       TIMING DRIVEN METAL FILL       # 
  ########################################
  
  if {$ICC_METAL_FILL_TIMING_DRIVEN} {
    set_extraction_options -real_metalfill_extraction NONE
    insert_metal_filler -routing_space $ICC_METAL_FILL_SPACE -timing_driven
  } else {
    insert_metal_filler -routing_space $ICC_METAL_FILL_SPACE
  }

  set_extraction_options -real_metalfill_extraction FLOATING

  if { [check_error -verbose] != 0} { echo "SCRIPT-Error, flagging ..." }
}
if {$ADD_METAL_FILL == "HERCULES" } {

  ########################################
  #      HERCULES DRIVEN METAL FILL      # 
  ########################################
  
  if {[file exists [which $SIGNOFF_FILL_RUNSET]] } {
    set_physical_signoff_options -exec_cmd hercules -fill_runset $SIGNOFF_FILL_RUNSET
  }

  if {$SIGNOFF_MAPFILE != ""} {set_physical_signoff_options -mapfile $SIGNOFF_MAPFILE}

  report_physical_signoff_options
  signoff_metal_fill

  set_extraction_options -real_metalfill_extraction FLOATING

  if { [check_error -verbose] != 0} { echo "SCRIPT-Error, flagging ..." }
}


if {$ADD_METAL_FILL == "ICV" } {

  ########################################
  #         ICV DRIVEN METAL FILL        # 
  ########################################
  
  if {[file exists [which $SIGNOFF_FILL_RUNSET]] } {
    set_physical_signoff_options -exec_cmd icv -fill_runset $SIGNOFF_FILL_RUNSET
  }

  if {$SIGNOFF_MAPFILE != ""} {set_physical_signoff_options -mapfile $SIGNOFF_MAPFILE}

  report_physical_signoff_options
  if { !$SIGNOFF_METAL_FILL_TIMING_DRIVEN } {
    signoff_metal_fill 
  } else {
    set_extraction_options -real_metalfill_extraction NONE
    signoff_metal_fill -timing_preserve_setup_slack_threshold $TIMING_PRESERVE_SLACK_SETUP
  }

  set_extraction_options -real_metalfill_extraction FLOATING

  if { [check_error -verbose] != 0} { echo "SCRIPT-Error, flagging ..." }
}


  redirect -file $REPORTS_DIR_METAL_FILL/${ICC_METAL_FILL_CEL}.mv {check_mv_design -verbose}
  save_upf $RESULTS_DIR/${ICC_METAL_FILL_CEL}.upf  
if {$ICC_REPORTING_EFFORT != "OFF" } {
 redirect -tee -file $REPORTS_DIR_METAL_FILL/$ICC_METAL_FILL_CEL.qor {report_qor}
 redirect -tee -file $REPORTS_DIR_METAL_FILL/$ICC_METAL_FILL_CEL.qor -append {report_qor -summary}
 redirect -file $REPORTS_DIR_METAL_FILL/$ICC_METAL_FILL_CEL.con {report_constraints}
}

if {$ICC_REPORTING_EFFORT != "OFF" } {
     redirect -tee -file $REPORTS_DIR_METAL_FILL/$ICC_METAL_FILL_CEL.clock_tree {report_clock_tree -summary}     ;# global skew report
     redirect -file $REPORTS_DIR_METAL_FILL/$ICC_METAL_FILL_CEL.clock_timing {report_clock_timing -type skew} ;# local skew report
}
if {$ICC_REPORTING_EFFORT != "OFF" } {
 redirect -file $REPORTS_DIR_METAL_FILL/$ICC_METAL_FILL_CEL.max.tim {report_timing -crosstalk_delta -capacitance -transition_time -input_pins -nets -delay max} 
 redirect -file $REPORTS_DIR_METAL_FILL/$ICC_METAL_FILL_CEL.min.tim {report_timing -crosstalk_delta -capacitance -transition_time -input_pins -nets -delay min} 
}
if {$ICC_REPORTING_EFFORT != "OFF" } {
 redirect -tee -file $REPORTS_DIR_METAL_FILL/$ICC_METAL_FILL_CEL.sum {report_design_physical -all -verbose}
}


if {$ICC_REPORTING_EFFORT != "OFF" } {
 create_qor_snapshot -clock_tree -name $ICC_METAL_FILL_CEL
 redirect -file $REPORTS_DIR_METAL_FILL/$ICC_METAL_FILL_CEL.qor_snapshot.rpt {report_qor_snapshot -no_display}
}


# Lynx compatible procedure which produces design metrics based on reports
sproc_generate_metrics

# Lynx Compatible procedure which performs final metric processing and exits
sproc_script_stop
