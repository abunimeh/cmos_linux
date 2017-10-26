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
set SEV(dst) outputs_icc 

set SEV(script_file) [info script]

source ./scripts/common_setting/lcrm_setup/lcrm_setup.tcl

sproc_script_start
source -echo ./scripts/common_setting/icc_setup.tcl 
set ICC_METAL_FILL_CEL $SEV(src) 

#######################################
####Outputs Script
#######################################

##Open Design
open_mw_cel $ICC_METAL_FILL_CEL -lib $MW_DESIGN_LIBRARY
set upf_create_implicit_supply_sets false

  ########################
  #     SIGNOFF DRC      #
  ########################

if {[file exists [which $SIGNOFF_DRC_RUNSET]] } {

  if {$SIGNOFF_DRC_ENGINE == "HERCULES"} {
    set_physical_signoff_options -exec_cmd hercules -drc_runset $SIGNOFF_DRC_RUNSET
  } elseif { $SIGNOFF_DRC_ENGINE == "ICV"} {
    set_physical_signoff_options -exec_cmd icv -drc_runset $SIGNOFF_DRC_RUNSET
    }

  if {$SIGNOFF_MAPFILE != ""} {set_physical_signoff_options -mapfile $SIGNOFF_MAPFILE}
  report_physical_signoff_options
  signoff_drc

}

##Change Names
change_names -rules verilog -hierarchy
save_mw_cel -as change_names_icc
close_mw_cel
open_mw_cel change_names_icc


##Verilog
write_verilog -diode_ports  -no_physical_only_cells  -supply_statement none $RESULTS_DIR/$DESIGN_NAME.output.v

## For comparison with a Design Compiler netlist,the option -diode_ports is removed
write_verilog -no_physical_only_cells -supply_statement none $RESULTS_DIR/$DESIGN_NAME.output.dc.v

## For Prime Time use,to include DCAP cells for leakage power analysis,add the option -force_output_references
#  write_verilog -diode_ports -no_physical_only_cells -pg -supply_statement none -force_output_references [list of your DCAP cells] \
#  $RESULTS_DIR/$DESIGN_NAME.output.pt.v

## For LVS use,the option -no_physical_only_cells is removed
write_verilog -diode_ports  $RESULTS_DIR/$DESIGN_NAME.output.lvs.v


##SDC
set_app_var write_sdc_output_lumped_net_capacitance false
set_app_var write_sdc_output_net_resistance false

  write_sdc $RESULTS_DIR/$DESIGN_NAME.output.sdc
  save_upf $RESULTS_DIR/$DESIGN_NAME.output.upf 

extract_rc -coupling_cap
#write_parasitics  -format SPEF -output $RESULTS_DIR/$DESIGN_NAME.output.spef
write_parasitics  -format SBPF -output $RESULTS_DIR/$DESIGN_NAME.output.sbpf

##DEF
write_def -output  $RESULTS_DIR/$DESIGN_NAME.output.def


###GDSII
##Set options - usually also include a mapping file (-map_layer)
##  set_write_stream_options \
#	-child_depth 99 \
#       -output_filling fill \
#       -output_outdated_fill \
#       -output_pin geometry \
#       -keep_data_type
#   write_stream -lib_name $MW_DESIGN_LIBRARY -format gds $RESULTS_DIR/$DESIGN_NAME.gds

## Since C-2009.06, in case of MCMM, all scenarios are made active during ILM creation.
## No need to do this anymore separately

if {$ICC_CREATE_MODEL } {
  save_mw_cel -as $DESIGN_NAME
  close_mw_cel
  open_mw_cel $DESIGN_NAME
  create_ilm -include_xtalk
  ## Validating ILM using write_interface_timing and compare_interface_timing
  #  	write_interface_timing cel.rpt
  #  	close_mw_cel
  #  	open_mw_cel $DESIGN_NAME.ILM
  #  	write_interface_timing ilm.rpt
  #  	compare_interface_timing cel.rpt ilm.rpt -output compare_interface_timing.rpt
  #  	close_mw_cel
  #  	open_mw_cel $DESIGN_NAME

  create_macro_fram
  if {$ICC_FIX_ANTENNA} {
  ##create Antenna Info
    set_droute_options -name doAntennaConx -value 4
    extract_hier_antenna_property -cell_name $DESIGN_NAME
  }
  close_mw_cel 
}
# Lynx Compatible procedure which performs final metric processing and exits
sproc_script_stop
