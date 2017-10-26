source -echo -verbose {{dc_dic.dc__tcl.DcTcl_DIR}}/dc_setup.tcl
source -echo -verbose {{dc_dic.dc__tcl.DcTcl_DIR}}/set_args.tcl
#################################################################################
# Design Compiler Reference Methodology Script for Top-Down Flow
# Script: dc.tcl
# Version: D-2010.03 (March 29, 2010)
# Copyright (C) 2007-2010 Synopsys, Inc. All rights reserved.
#################################################################################

# SVF should always be written to allow Formality verification
# for advanced optimizations.
set_svf ${RESULTS_DIR}/${DCRM_SVF_OUTPUT_FILE}

#################################################################################
# Read in the RTL Design
# Read in the RTL source files or read in the elaborated design (DDC).
# Use the -format option to specify: verilog, sverilog, or vhdl as needed.
#################################################################################

define_design_lib WORK -path {{dc_dic.dc__tcl.DT_DIR}}/WORK

analyze -format verilog -define LIB ${RTL_SOURCE_FILES}
elaborate ${DESIGN_NAME}

# read_ddc ${DCRM_ELABORATED_DESIGN_DDC_OUTPUT_FILE}
write -hierarchy -format ddc -output ${RESULTS_DIR}/${DCRM_ELABORATED_DESIGN_DDC_OUTPUT_FILE}

#################################################################################
# Apply Logical Design Constraints
#################################################################################

source -echo -verbose {{dc_dic.dc__tcl.DcTcl_DIR}}/common.sdc
source -echo -verbose {{dc_dic.dc__tcl.DcTcl_DIR}}/constraints.tcl

set_app_var compile_ultra_ungroup_dw false

#group_path settings
set ports_clock_root [filter_collection [get_attribute [get_clocks] sources] object_class==port]
group_path -name reg2reg -from [all_registers -clock_pins] -to [all_registers -data_pins]
group_path -name reg2out -from [all_registers -clock_pins] -to [all_outputs]
group_path -name in2reg  -from [remove_from_collection [all_inputs] $ports_clock_root] -to [all_registers -data_pins]
group_path -name in2out  -from [remove_from_collection [all_inputs] $ports_clock_root] -to [all_outputs]
#group_path -name zszx2cczx -from u_zszx -to u_cczx -weight 5

    if {[shell_is_in_topographical_mode]} {
      # Use the following command to enable power prediction using clock tree estimation.

      # set_power_prediction true -ct_references <LIB CELL LIST>
    }

if {[shell_is_in_topographical_mode]} {

  # Specify ignored layers for routing to improve correlation
  # Use the same ignored layers that will be used during place and route
  if { ${MIN_ROUTING_LAYER} != ""} {
    set_ignored_layers -min_routing_layer ${MIN_ROUTING_LAYER}
  }
  if { ${MAX_ROUTING_LAYER} != ""} {
    set_ignored_layers -max_routing_layer ${MAX_ROUTING_LAYER}
  }

  report_ignored_layers


  if {[file exists [which ${DCRM_DCT_DEF_INPUT_FILE}]]} {
    extract_physical_constraints ${DCRM_DCT_DEF_INPUT_FILE}
  }

  ## For floorplan file input
  # The floorplan file for DCT can be written from ICC using the following recommended options
  # icc_shell> write_floorplan -placement {io hard_macro soft_macro} -create_terminal \
  #                            -row -create_bound -preroute ${DCRM_DCT_FLOORPLAN_INPUT_FILE}

  if {[file exists [which ${DCRM_DCT_FLOORPLAN_INPUT_FILE}]]} {
    read_floorplan ${DCRM_DCT_FLOORPLAN_INPUT_FILE}
  }


  ## For Tcl file input

  # For Tcl constraints, the name matching feature must be explicitly enabled
  # and will also use the set_fuzzy_query_options setttings.  This should 
  # be turned off after the constraint read in order to minimize runtime.

#  if {[file exists [which ${DCRM_DCT_PHYSICAL_CONSTRAINTS_INPUT_FILE}]]} {
#    set_app_var fuzzy_matching_enabled true 
#    source -echo -verbose ${DCRM_DCT_PHYSICAL_CONSTRAINTS_INPUT_FILE}
#    set_app_var fuzzy_matching_enabled false 
#  }

if {[file exists [which {{dc_dic.dc__tcl.DcTcl_DIR}}/constraints.tcl]]} {
     set_app_var fuzzy_matching_enabled true
     source -echo -verbose {{dc_dic.dc__tcl.DcTcl_DIR}}/constraints.tcl
     set_app_var fuzzy_matching_enabled false
   }

  # Use write_floorplan to save the applied floorplan.
  # Note: write_physical_constraints should no longer be used.
  write_floorplan -all ${RESULTS_DIR}/${DCRM_DCT_FLOORPLAN_OUTPUT_FILE}

  # Verify that all the desired physical constraints have been applied
  # Add the -pre_route option to include pre-routes in the report
  report_physical_constraints > ${REPORTS_DIR}/${DCRM_DCT_PHYSICAL_CONSTRAINTS_REPORT}
}

#################################################################################
# Apply Additional Optimization Constraints
#################################################################################

# Prevent assignment statements in the Verilog netlist.
set_fix_multiple_port_nets -all -buffer_constants

set_boundary_optimization ${DESIGN_NAME} false

set_host_options -max_cores {{dc_dic.dc__tcl.max_cores}} 
if {[shell_is_in_topographical_mode]} {
# Use the "-check_only" option of "compile_ultra" to verify that your
# libraries and design are complete and that optimization will not fail
# in topographical mode.  Use the same options as will be used in compile_ultra.

# compile_ultra -scan -gate_clock -check_only
}

set compile_seqmap_identify_shift_registers false
set_max_fanout {{dc_dic.dc__tcl.set_max_fanout}} ${DESIGN_NAME}
{{dc_dic.dc__tcl.pre_compile}}
compile_ultra {{dc_dic.dc__tcl.compile_ultra}} 
{{dc_dic.dc__tcl.post_compile}}
#-spg 
#compile_ultra -scan -gate_clock -no_autoungroup

#################################################################################
# Save Design after First Compile
#################################################################################
write -format ddc -hierarchy -output ${RESULTS_DIR}/${DCRM_COMPILE_ULTRA_DDC_OUTPUT_FILE}
change_names -rules verilog -hierarchy

#################################################################################
# Write out Design
#################################################################################

# Write and close SVF file and make it available for immediate use
#set_svf -of
{{dc_dic.dc__tcl.pre_write}}
write -format ddc -hierarchy -output ${RESULTS_DIR}/${DCRM_FINAL_DDC_OUTPUT_FILE}
write -f verilog -hierarchy -output ${RESULTS_DIR}/${DCRM_FINAL_VERILOG_OUTPUT_FILE}

#################################################################################
# Write out Design Data
#################################################################################

if {[shell_is_in_topographical_mode]} {

  # Note: write_physical_constraints should no longer be used.
  write_floorplan -all ${RESULTS_DIR}/${DCRM_DCT_FINAL_FLOORPLAN_OUTPUT_FILE}

  # Write parasitics data from DCT placement for static timing analysis
  write_parasitics -output ${RESULTS_DIR}/${DCRM_DCT_FINAL_SPEF_OUTPUT_FILE}

  # Write SDF backannotation data from DCT placement for static timing analysis
  write_sdf ${RESULTS_DIR}/${DCRM_DCT_FINAL_SDF_OUTPUT_FILE}

  # Do not write out net RC info into SDC
  set_app_var write_sdc_output_lumped_net_capacitance false
  set_app_var write_sdc_output_net_resistance false
}

write_sdc -nosplit ${RESULTS_DIR}/${DCRM_FINAL_SDC_OUTPUT_FILE}
{{dc_dic.dc__tcl.post_write}}
#################################################################################
# Generate Final Reports
#################################################################################

report_qor > ${REPORTS_DIR}/${DCRM_FINAL_QOR_REPORT}
report_timing -slack_lesser_than {{dc_dic.dc__tcl.slack_lesser_than}} -max_paths {{dc_dic.dc__tcl.max_paths}} -transition_time -nets -attributes -nosplit > ${REPORTS_DIR}/${DCRM_FINAL_TIMING_REPORT}

if {[shell_is_in_topographical_mode]} {
  report_area -physical -nosplit -hierarchy > ${REPORTS_DIR}/${DCRM_FINAL_AREA_REPORT}
} else {
  report_area -nosplit -hierarchy > ${REPORTS_DIR}/${DCRM_FINAL_AREA_REPORT}
}

if {[shell_is_in_topographical_mode]} {
  # report_congestion (topographical mode only) reports estimated routing related congestion
  # after topographical mode synthesis.
  # This command requires a license for Design Compiler Graphical.

  report_congestion > ${REPORTS_DIR}/${DCRM_DCT_FINAL_CONGESTION_REPORT}

  # Use the following to generate and write out a congestion map from batch mode
  # This requires a GUI session to be temporarily opened and closed so a valid DISPLAY
  # must be set in your UNIX environment.

  if {[info exists env(DISPLAY)]} {
    gui_start

    # Create a layout window
    set MyLayout [gui_create_window -type LayoutWindow]

    # Build congestion map in case report_congestion was not previously run
    report_congestion -build_map

    # Display congestion map in layout window
    gui_show_map -map "Global Route Congestion" -show true

    # Zoom full to display complete floorplan
    gui_zoom -window [gui_get_current_window -view] -full

    # Write the congestion map out to an image file
    # You can specify the output image type with -format png | xpm | jpg | bmp

    # The following saves only the congestion map without the legends
    gui_write_window_image -format png -file ${REPORTS_DIR}/${DCRM_DCT_FINAL_CONGESTION_MAP_OUTPUT_FILE}

    # The following saves the entire congestion map layout window with the legends
    gui_write_window_image -window ${MyLayout} -format png -file ${REPORTS_DIR}/${DCRM_DCT_FINAL_CONGESTION_MAP_WINDOW_OUTPUT_FILE}

    gui_stop
  } else {
    puts "Information: The DISPLAY environment variable is not set. Congestion map generation has been skipped."
  }
}

# Use SAIF file for power analysis
# read_saif -auto_map_names -input ${DESIGN_NAME}.saif -instance < DESIGN_INSTANCE > -verbose

report_power -nosplit > ${REPORTS_DIR}/${DCRM_FINAL_POWER_REPORT}
report_clock_gating -nosplit > ${REPORTS_DIR}/${DCRM_FINAL_CLOCK_GATING_REPORT}
check_design > ${REPORTS_DIR}/${DCRM_FINAL_CHECK_DESIGN_REPORT}

#################################################################################
# Write out Milkyway Design for Top-Down Flow
#
# This should be the last step in the script
#################################################################################

if {[shell_is_in_topographical_mode]} {
  # write_milkyway uses: mw_logic1_net, mw_logic0_net and mw_design_library variables from dc_setup.tcl
  write_milkyway -overwrite -output ${DCRM_FINAL_MW_CEL_NAME}
}

exit
