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

set SEV(src) clock_opt_route_icc
set SEV(dst) route_icc

set SEV(script_file) [info script]

source ./scripts/common_setting/lcrm_setup/lcrm_setup.tcl

sproc_script_start
source -echo ./scripts/common_setting/icc_setup.tcl 
set ICC_CLOCK_OPT_ROUTE_CEL $SEV(src) 
set ICC_ROUTE_CEL $SEV(dst) 

########################
## route_icc: Routing ##
########################


set upf_create_implicit_supply_sets false


open_mw_lib $MW_DESIGN_LIBRARY
redirect /dev/null "remove_mw_cel -version_kept 0 ${ICC_ROUTE_CEL}"
copy_mw_cel -from $ICC_CLOCK_OPT_ROUTE_CEL -to $ICC_ROUTE_CEL
open_mw_cel $ICC_ROUTE_CEL


source -echo common_optimization_settings_icc.tcl
source -echo common_placement_settings_icc.tcl
source -echo common_post_cts_timing_settings.tcl



########################################
#    LOAD THE ROUTE AND SI SETTINGS    #
########################################

source -echo common_route_si_settings_icc.tcl

  ##########################
  ## FIX SPECIAL MV CELLS
  ##########################

  if {[all_level_shifters] != ""} {
    set_dont_touch [all_level_shifters]
    set_attribute [all_level_shifters] is_fixed true
  }

  if {[all_ao_cells] != ""} {
    set_dont_touch [all_ao_cells]
    set_attribute [all_ao_cells] is_fixed true
  }

  if {$RR_CELLS != ""} {
    set RR [get_cells -hier -f "ref_name =~ ${RR_CELLS}*"]
    set_dont_touch $RR
    set_attribute $RR is_fixed true
  }

  #############################
  ## COMPLETE POWER CONNECTIONS
  #############################
  check_mv_design -verbose
  
####Pre route_opt checks
##Check for Ideal Nets
set num_ideal [sizeof_collection [all_ideal_nets]]
if {$num_ideal >= 1} {echo "SCRIPT-Error-Info: $num_ideal Nets are ideal prior to route_opt. Please investigate."}

##Check for HFNs
set hfn_thres "41 101 501"
foreach thres $hfn_thres {
  set num_hfn [sizeof_collection [all_high_fanout -nets -threshold $thres]]
  echo "SCRIPT-Info: Number of nets with fanout > $thres = $num_hfn"
  if {$thres == 501 && $num_hfn >=1} {
    echo "SCRIPT-Error-Info: $num_hfn Nets with fanout > 500 exist prior to route_opt - Please check if marked ideal - possibly add buffer tree"
  }
}



if { [check_error -verbose] != 0} { echo "SCRIPT-Error, flagging ..." }

########################################
#       ROUTE_OPT CORE COMMAND         #
########################################

## some checks upfront 
#check_routeability
report_preferred_routing_direction

## Route first the design 
  report_tlu_plus_files

  ## Enabling a different distributed algorithm for Detail Route
  # set_app_var droute_enable_one_pass_partitioning 1
  route_opt -initial_route_only 
if { [check_error -verbose] != 0} { echo "SCRIPT-Error, flagging ..." }
if {$ICC_CTS_UPDATE_LATENCY} {
   update_clock_latency
} 


if {$ICC_DBL_VIA} {
  save_mw_cel -as ${ICC_ROUTE_CEL}_NO_DBL_VIA
## To get optimal double via rate, perform first a non-timing driven double via insertion.
## Later on, during chipfinishing, we will execute a Timing Driven double via insertion.

## Auto mode for insert_redundant_via
insert_zrt_redundant_vias  
## Optionally, manual mode for insert_redundant_via
# insert_redundant_vias \
   #-num_cpus $ICC_NUM_CPUS \
   #-from_via "from_via_list" \
   #-to_via "to_via_list" \
   #-to_via_x_size "list_of_via_x_sizes" \
   #-to_via_y_size "list_of_via_y_sizes"

   ##example: -from_via "VIA45 VIA45 VIA12A" -to_via "VIA45f VIA45 VIA12f" -to_via_x_size "1 1 1" -to_via_y_size "2 2 2"
}

########################################
#           CONNECT P/G                #
########################################


## Connect Power & Ground for non-MV and MV-mode

 if {[file exists [which $CUSTOM_CONNECT_PG_NETS_SCRIPT]]} {
   source -echo $CUSTOM_CONNECT_PG_NETS_SCRIPT
 } else {
    if {!$ICC_TIE_CELL_FLOW} {derive_pg_connection -verbose -tie}
    redirect -file $REPORTS_DIR_ROUTE/route.mv {check_mv_design -verbose}
   }
if { [check_error -verbose] != 0} { echo "SCRIPT-Error, flagging ..." }
if {$ICC_REPORTING_EFFORT != "OFF" } {
    redirect -tee -file $REPORTS_DIR_ROUTE/$ICC_ROUTE_CEL.clock_tree {report_clock_tree -summary}     ;# global skew report
    redirect -file $REPORTS_DIR_ROUTE/$ICC_ROUTE_CEL.clock_timing {report_clock_timing -type skew} ;# local skew report
}
if {$ICC_REPORTING_EFFORT != "OFF" } {
 redirect -tee -file $REPORTS_DIR_ROUTE/$ICC_ROUTE_CEL.qor {report_qor}
 redirect -tee -file $REPORTS_DIR_ROUTE/$ICC_ROUTE_CEL.qor -append {report_qor -summary}
 redirect -file $REPORTS_DIR_ROUTE/$ICC_ROUTE_CEL.con {report_constraints}
}
if {$ICC_REPORTING_EFFORT != "OFF" } {
 redirect -file $REPORTS_DIR_ROUTE/$ICC_ROUTE_CEL.max.tim {report_timing -capacitance -transition_time -input_pins -nets -delay max} 
 redirect -file $REPORTS_DIR_ROUTE/$ICC_ROUTE_CEL.min.tim {report_timing -capacitance -transition_time -input_pins -nets -delay min} 
}

save_mw_cel -as $ICC_ROUTE_CEL

if {$ICC_REPORTING_EFFORT != "OFF" } {
 create_qor_snapshot -clock_tree -name $ICC_ROUTE_CEL
 redirect -file $REPORTS_DIR_ROUTE/$ICC_ROUTE_CEL.qor_snapshot.rpt {report_qor_snapshot -no_display}
}




if {$ICC_CREATE_GR_PNG} {
  # start GUI
  gui_start
  
  # turn off DR
  gui_set_setting -window [gui_get_current_window -types Layout -mru] -setting showRoute -value false
  gui_execute_events

  # show congestion overlay
  gui_set_setting -window [gui_get_current_window -types Layout -mru] -setting mmName -value AREAPARTITION 
  gui_zoom -window [gui_get_current_window -view] -full
  gui_execute_events
  
  # save snapshots
  gui_write_window_image -window [gui_get_current_window -view -mru] -file ${REPORTS_DIR_ROUTE}/${ICC_ROUTE_CEL}.GR.png
  
  # stop GUI
  gui_stop
}

# Lynx compatible procedure which produces design metrics based on reports
sproc_generate_metrics

# Lynx Compatible procedure which performs final metric processing and exits
sproc_script_stop
