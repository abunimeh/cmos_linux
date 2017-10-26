set TEV(num_cores) 1

set SEV(src) init_design_icc
set SEV(dst) flat_dp

set SEV(script_file) [info script]

source ./scripts/common_setting/lcrm_setup/lcrm_setup.tcl

sproc_script_start
source -echo ./scripts/common_setting/icc_setup.tcl 
set ICC_FLOORPLAN_CEL $SEV(src) 
gui_set_current_task -name {Design Planning}
set upf_create_implicit_supply_sets false
open_mw_lib $MW_DESIGN_LIBRARY
copy_mw_cel -from $ICC_FLOORPLAN_CEL -to flat_dp
open_mw_cel flat_dp
link

source ./scripts/common_setting/common_placement_settings_icc.tcl
source ./scripts/common_setting/common_optimization_settings_icc.tcl
set_ideal_network [all_fanout -flat -clock_tree]
###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%###
###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%###
### customize power network synthesis constraints ###
### ../../../DATA_SAED/ICC_DATA/fp/leon3mp.pns_constraint.tcl
#source $CUSTOM_ICC_DP_PNS_CONSTRAINT_SCRIPT
###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%###
###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%###

#####################################################################
## Flat Design Planning Flow : Virtual Flat Placement, Power Network Synthesis/Analysis, In Place Optimization, and Proto Route 
#####################################################################
### ../../../scripts_block/rm_icc_dp_scripts/baseline.tcl ####
### source -echo baseline.tcl 
#####################################################################
#set_fp_placement_strategy -sliver_size 10

#create_fp_placement

#route_zrt_global -exploration true 

#save_mw_cel -as flat_dp_groute_after_place
#remove_route_by_type -signal_detail_route -clock_tie_off -pg_tie_off
#extract_rc -estimate
#create_qor_snapshot -name flat_dp_place
#report_qor_snapshot -name flat_dp_place > ${REPORTS_DIR_DP}/pre.qor
###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%###
###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%###
#################################################################
### Additional options for Multivoltage Design    	       ##
#################################################################
### synthesize power networks in selected voltage areas  ########
### synthesize power switch in the shutdown voltage area ########
### ../../../DATA_SAED/ICC_DATA/fp/leon3mp.pns.tcl       ########
#source -echo $CUSTOM_ICC_DP_PNS_SCRIPT
###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%###
###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%###
#create_fp_virtual_pad -point {1.635 204.120} -nets VDD
#create_fp_virtual_pad -point {6.165 228.360} -nets GND
#analyze_fp_rail -power_budget $PNS_POWER_BUDGET -voltage_supply $PNS_VOLTAGE_SUPPLY -output_directory $PNS_OUTPUT_DIR -nets $PNS_POWER_NETS


 
read_def $ICC_IN_DEF_FILE -no_incremental


#source common_optimization_settings_icc.tcl
#extract_rc -estimate
#report_timing -cap -tran -input -net -delay max > $REPORTS_DIR_DP/optimize_fp_timing_before.rpt
#set compile_instance_name_prefix dp_ipo
#optimize_fp_timing

#derive_pg_connection -power_net VDD -power_pin VDD -ground_net GND -ground_pin GND
###########    preroute std_cell       ##########################
### ../../../DATA_SAED/ICC_DATA/fp/leon3mp.preroute.tcl #########
 #### need to adjust the width of rings by hands#####
#source $CUSTOM_ICC_DP_PREROUTE_STD_CELL_SCRIPT  
create_fp_placement
route_zrt_global -exploration true

save_mw_cel -as flat_dp_groute
remove_route_by_type -signal_detail_route -clock_tie_off -pg_tie_off

extract_rc -estimate
create_qor_snapshot -name flat_dp
report_qor_snapshot -name flat_dp > ${REPORTS_DIR_DP}/final.qor
report_timing -cap -tran -input -net -delay max > ${REPORTS_DIR_DP}/final.rpt

if {[all_macro_cells] != "" } { 
  set_dont_touch_placement [all_macro_cells]  
}
save_mw_cel -overwrite
write_floorplan -placement {io hard_macro soft_macro} ${RESULTS_DIR}/dump.floorplan
write_floorplan -preroute ${RESULTS_DIR}/dump.route
write_floorplan -all ${RESULTS_DIR}/dump.complete_floorplan
write_pin_pad_physical_constraints -cel [get_object_name  [current_mw_cel]] -io_only -constraint_type side_order ${RESULTS_DIR}/dump.tdf

### Outputs for DCT ###
write_def -version 5.7 -rows_tracks_gcells -macro -pins -blockages -specialnets -vias -regions_groups -verbose -output ${RESULTS_DIR}/dump.DCT.def
write_floorplan -create_terminal -create_bound -row -preroute -placement {io hard_macro soft_macro} ${RESULTS_DIR}/dump.DCT.fp

# Lynx compatible procedure which produces design metrics based on reports
sproc_generate_metrics


close_mw_cel

###########################################################################

sproc_script_stop
