puts "RM-Info: Running script [info script]\n"

##########################################################################################
# Version: E-2010.12 (January 10, 2011)
# Copyright (C) 2007-2011 Synopsys, Inc. All rights reserved.
##########################################################################################

## Optimization Common Session Options - set in all sessions

set_host_options -max_cores $ICC_NUM_CORES

## General Optimization
set_app_var timing_enable_multiple_clocks_per_reg true 
set_app_var case_analysis_with_logic_constants true 
set_fix_multiple_port_nets -all -buffer_constants  
#if {$ICC_TIE_CELL_FLOW} {
	set_auto_disable_drc_nets -constant false
#
#} else {
#	set_auto_disable_drc_nets -constant true
#} 
set timing_scgc_override_library_setup_hold false
##Evaluate whether you library and design requires timing_use_enhanced_capacitance_modeling or not. Also only needed for OCV
#set_app_var timing_use_enhanced_capacitance_modeling true ;#PT default -  libraries with capacitance ranges (also see Solvnet 021686)


#   if {$ICC_MAX_AREA != ""} {
#     set_max_area $ICC_MAX_AREA
#   }


## Set Area Critical Range
## Typical value: 10 percent of critical clock period
#if {$AREA_CRITICAL_RANGE_PRE_CTS != ""} {set_app_var physopt_area_critical_range $AREA_CRITICAL_RANGE_PRE_CTS} 


## Set Power Critical Range
## Typical value: 9 percent of critical clock period
#if {$POWER_CRITICAL_RANGE_PRE_CTS != ""} {set_app_var physopt_power_critical_range $POWER_CRITICAL_RANGE_PRE_CTS} 


## Set dont use cells
## Examples, big drivers (EM issues), very weak drivers, delay cells, 
## clock cells

#if {[file exists [which $ICC_IN_DONT_USE_FILE]] } {
###  ../../../DATA_SAED/use_tie.tcl ###
   #     source -echo  $ICC_IN_DONT_USE_FILE 
#} 


## Fixing the locations of the hard macros
#if {[all_macro_cells] != "" } { 
  #set_dont_touch_placement [all_macro_cells]  
#} 


## To reset power options to default to override what is stored in Milkyway database
#  set_optimize_pre_cts_power_options -default

#if {$ICC_CTS_CLOCK_GATE_MERGE} {
# set_optimize_pre_cts_power_options -merge_clock_gates true
#} else {
 set_optimize_pre_cts_power_options -merge_clock_gates false
#}

#if {$ICC_LOW_POWER_PLACEMENT} {
#  set_optimize_pre_cts_power_options -low_power_placement true
#} else {
  set_optimize_pre_cts_power_options -low_power_placement false
#}

#if {$LEAKAGE_POWER} {
### Turn on leakage 
#  set_optimize_pre_cts_power_options -leakage true 
#} else {
### Turn off leakage 
#  set_optimize_pre_cts_power_options -leakage false
#}
#
#if {$DYNAMIC_POWER} {
### Dynamic power opto throughout the flow
#  set_optimize_pre_cts_power_options -dynamic true
#} else {
### No dynamic power opto 
#  set_optimize_pre_cts_power_options -dynamic false
#}

## End of Common Optimization Session Options

puts "RM-Info: Completed script [info script]\n"
