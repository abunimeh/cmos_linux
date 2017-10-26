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
set SEV(dst) signoff_opt_icc

set SEV(script_file) [info script]

source ./scripts/common_setting/lcrm_setup/lcrm_setup.tcl

sproc_script_start
source -echo ./scripts/common_setting/icc_setup.tcl 
set ICC_CHIP_FINISH_CEL $SEV(src) 
set ICC_SIGNOFF_OPT_CEL $SEV(dst) 

###########################################################################
## signoff_opt_icc: Signoff optimization using StarRC and PT
###########################################################################

if {![file exists [which $PT_DIR/pt_shell]]} {
  echo "SCRIPT-Info : $PT_DIR/pt_shell does not exist. Skipping signoff_opt step"
  redirect -file signoff_opt_icc {echo "SCRIPT-Info : signoff_opt has not been run"}
  # Lynx Compatible procedure which performs final metric processing and exits
  sproc_script_stop
} 

open_mw_lib $MW_DESIGN_LIBRARY
redirect /dev/null "remove_mw_cel -version_kept 0 ${ICC_SIGNOFF_OPT_CEL}"
copy_mw_cel -from $ICC_CHIP_FINISH_CEL -to $ICC_SIGNOFF_OPT_CEL
open_mw_cel $ICC_SIGNOFF_OPT_CEL


source -echo common_optimization_settings_icc.tcl
source -echo common_placement_settings_icc.tcl
source -echo common_post_cts_timing_settings.tcl

#############################
## COMPLETE POWER CONNECTIONS
#############################

  check_mv_design -verbose


########################################
#    LOAD THE ROUTE AND SI SETTINGS    #
########################################

source -echo common_route_si_settings_zrt_icc.tcl


########################################
#       SIGNOFF_OPT CORE COMMAND       #
########################################

## setup PT
  if {[file exists [which $PT_SDC_FILE]]} {
    set_primetime_options  -exec_dir $PT_DIR -sdc_file $PT_SDC_FILE
  } else {
    set_primetime_options  -exec_dir $PT_DIR
  }

## setup StarRC
  if {$STARRC_MIN_NXTGRD == ""} {set STARRC_MIN_NXTGRD $STARRC_MAX_NXTGRD}
  set_starrcxt_options  -exec_dir $STARRC_DIR \
     -max_nxtgrd_file $STARRC_MAX_NXTGRD \
     -min_nxtgrd_file $STARRC_MIN_NXTGRD \
     -map_file        $STARRC_MAP_FILE

if { [check_error -verbose] != 0} { echo "SCRIPT-Error, flagging ..." }
report_primetime_options
report_starrcxt_options
run_signoff -check_only
run_signoff

if {$ICC_REPORTING_EFFORT != "OFF" } {
  redirect -file $REPORTS_DIR_SIGNOFF_OPT/$ICC_SIGNOFF_OPT_CEL.pre.max.tim {report_timing -capacitance -transition_time -input_pins -nets -delay max}
  redirect -file $REPORTS_DIR_SIGNOFF_OPT/$ICC_SIGNOFF_OPT_CEL.pre.min.tim {report_timing -capacitance -transition_time -input_pins -nets -delay min}
  redirect -tee -file $REPORTS_DIR_SIGNOFF_OPT/$ICC_SIGNOFF_OPT_CEL.pre.qor {report_qor}
  redirect -tee -file $REPORTS_DIR_SIGNOFF_OPT/$ICC_SIGNOFF_OPT_CEL.pre.qor -append {report_qor -summary}
  redirect -file $REPORTS_DIR_SIGNOFF_OPT/$ICC_SIGNOFF_OPT_CEL.pre.con {report_constraints}
}

##Run Signoff Opt
signoff_opt -skip_initial_analysis 

##To run when design doesn't meet initial criteria use:
# signoff_opt -ignore_design_readiness -num_iteration 2

if {$ICC_REPORTING_EFFORT != "OFF" } {
  redirect -file $REPORTS_DIR_SIGNOFF_OPT/$ICC_SIGNOFF_OPT_CEL.max.tim {report_timing -capacitance -transition_time -input_pins -nets -delay max}
  redirect -file $REPORTS_DIR_SIGNOFF_OPT/$ICC_SIGNOFF_OPT_CEL.min.tim {report_timing -capacitance -transition_time -input_pins -nets -delay min}
  redirect -tee -file $REPORTS_DIR_SIGNOFF_OPT/$ICC_SIGNOFF_OPT_CEL.qor {report_qor}
  redirect -tee -file $REPORTS_DIR_SIGNOFF_OPT/$ICC_SIGNOFF_OPT_CEL.qor -append {report_qor -summary}
  redirect -file $REPORTS_DIR_SIGNOFF_OPT/$ICC_SIGNOFF_OPT_CEL.con {report_constraints}
}

run_signoff -signoff_analysis false

if { [check_error -verbose] != 0} { echo "SCRIPT-Error, flagging ..." }

########################################
#          STD CELL FILLERS            #
########################################
if {$ADD_FILLER_CELL } {
  if {$FILLER_CELL != ""} {insert_stdcell_filler -cell_without_metal $FILLER_CELL}
}
## in case new nets are created that go from one VA to another, level shifters need to be inserted on these nets
#  insert_level_shifters -all_clock_nets -verbose
########################################
#           CONNECT P/G                #
########################################


## Connect Power & Ground for non-MV and MV-mode

 if {[file exists [which $CUSTOM_CONNECT_PG_NETS_SCRIPT]]} {
   source -echo $CUSTOM_CONNECT_PG_NETS_SCRIPT
 } else {
    if {!$ICC_TIE_CELL_FLOW} {derive_pg_connection -verbose -tie}
    redirect -file $REPORTS_DIR_SIGNOFF_OPT/sigoff_opt.mv {check_mv_design -verbose}
    save_upf $RESULTS_DIR/$ICC_SIGNOFF_OPT_CEL.upf
   }
if {$ICC_TIE_CELL_FLOW} {
  echo "SCRIPT-Info : List of TIE-CELL instances in your design :"
  all_tieoff_cells
} else { report_tie_nets
  }

if { [check_error -verbose] != 0} { echo "SCRIPT-Error, flagging ..." }

## Uncomment if you want detailed routing violation report with or without antenna info
# if {$ICC_FIX_ANTENNA} {
#    verify_zrt_route -antenna true ;
# } else {
#    verify_zrt_route -antenna false ;
#   }



save_mw_cel -as $ICC_SIGNOFF_OPT_CEL


# Lynx compatible procedure which produces design metrics based on reports
sproc_generate_metrics

# Lynx Compatible procedure which performs final metric processing and exits
sproc_script_stop
