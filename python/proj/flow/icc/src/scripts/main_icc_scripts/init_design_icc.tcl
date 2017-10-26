set TEV(num_cores) 1
set SEV(src) init_design_icc
set SEV(dst) init_design_icc

set SEV(script_file) [info script]

### ./scripts/common_setting/lcrm_setup/lcrm_setup.tcl
source -echo -verbose  ./scripts/common_setting/lcrm_setup/lcrm_setup.tcl

sproc_script_start
### ./scripts/common_setting/icc_setup.tcl
source -echo -verbose ./scripts/common_setting/icc_setup.tcl 
set ICC_FLOORPLAN_CEL $SEV(dst) 


if {[file exists  $MW_DESIGN_LIBRARY] } {
        sh rm -r $MW_DESIGN_LIBRARY
}

create_mw_lib \
            -tech $TECH_FILE \
            -bus_naming_style {[%d]} \
            -mw_reference_library $MW_REFERENCE_LIB_DIRS \
            $MW_DESIGN_LIBRARY 

########################################################################################
# Ascii as the format between DCT and ICC
########################################################################################
open_mw_lib $MW_DESIGN_LIBRARY

### netlist : ./data/cordic_dff.syn.v ###
read_verilog -top $DESIGN_NAME $ICC_IN_VERILOG_NETLIST_FILE
uniquify_fp_mw_cel 
current_design $DESIGN_NAME

#set upf_create_implicit_supply_sets false
###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%###
###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%###
## load upf : ./data/leon3mp_ss_diff_supply.ICC.upf ####
#foreach load_ascii_upf_script $CUSTOM_LOAD_ASCII_UPF_SCRIPT_LIST {
#    source $load_ascii_upf_script
#}

#load_upf $ICC_IN_UPF_FILE

###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%###
###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%###

#### ./data/cordic_dff.syn.sdc ###
read_sdc $ICC_IN_SDC_FILE 

#### ./data/leon3mp.mapped.scandef ###
#read_def $ICC_IN_FULL_CHIP_SCANDEF_FILE


#redirect -file $REPORTS_DIR_INIT_DESIGN/$DESIGN_NAME.full_chip_check_scan_chain.rpt {check_scan_chain}

set ports_clock_root {} 
foreach_in_collection a_clock [get_clocks -quiet] { 
    set src_ports [filter_collection [get_attribute $a_clock sources] @object_class==port] 
    set ports_clock_root  [add_to_collection $ports_clock_root $src_ports] 
}
  
group_path -name REGOUT -to [all_outputs]
group_path -name REGIN -from [remove_from_collection [all_inputs] $ports_clock_root]
group_path -name FEEDTHROUGH -from [remove_from_collection [all_inputs] $ports_clock_root] -to [all_outputs]

remove_propagated_clock [all_fanout -clock_tree -flat]
remove_propagated_clock *

set_tlu_plus_files -max_tluplus $TLUPLUS_MAX_FILE -min_tluplus $TLUPLUS_MIN_FILE -tech2itf_map $MAP_FILE

report_tlu_plus_files

########################################
# Floorplan Creation: FLOORPLAN FILE  
########################################
### creat floorplan & place macro ./scripts/custom_scripts/leon3mp.floorplan.tcl ### 
#source $ICC_IN_FLOORPLAN_USER_FILE

### ./scripts/common_setting/common_optimization_settings_icc.tcl
### ./scripts/common_setting/common_placement_settings_icc.tcl
source -echo -verbose  common_optimization_settings_icc.tcl
source -echo -verbose common_placement_settings_icc.tcl


derive_pg_connection -power_net VDD -power_pin VDD 
derive_pg_connection -ground_net GND -ground_pin GND
derive_pg_connection -power_net VDD -ground_net GND -tie
#derive_pg_connection -create_net 
#report_power_domain
###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%###
###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%###
########################################################################################
#########    MV mode : Creating the physical MV objects
########################################################################################
### create voltage area  ./scripts/custom_scripts/leon3mp.voltage_area.tcl ###
#source -echo $CUSTOM_CREATE_VA_SCRIPT

#report_voltage_area -all

#associate_mv_cells

#MM addedsteps to handle the single rail isolation cells and make sure they are put 
#in the proper bounds
### create bounds for p1/p3/misc iso region ###
### ./scripts/custom_scripts/leon3mp.iso_region.tcl
#source -echo -verbose  ./scripts/custom_scripts/leon3mp.iso_region.tcl

#############################################
## MTCMOS CELL INSTANTIATION + CONNECTION  ##
#############################################
### create power switch array ./scripts/custom_scripts/leon3mp.power_switch.tcl ###
#source -echo $CUSTOM_POWER_SWITCH_SCRIPT


###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%###
###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%###



########################################
#           CONNECT P/G                #
########################################
#derive_pg_connection -verbose
#check_mv_design -verbose

# redirect -file $REPORTS_DIR_INIT_DESIGN/$DESIGN_NAME.ao_nets.rpt {get_always_on_logic -nets}
# redirect -file $REPORTS_DIR_INIT_DESIGN/$DESIGN_NAME.ao_cells.rpt  {get_always_on_logic -cells}
# redirect -file $REPORTS_DIR_INIT_DESIGN/$DESIGN_NAME.ao_all.rpt  {get_always_on_logic}
# redirect -file $REPORTS_DIR_INIT_DESIGN/$DESIGN_NAME.ao_all_boundary.rpt  {get_always_on_logic -boundary}
# save_upf $RESULTS_DIR/$ICC_FLOORPLAN_CEL.upf 


save_mw_cel -as $ICC_FLOORPLAN_CEL


########################################################################################
# Saving the cell + snapshot creation
########################################################################################
create_qor_snapshot -name $ICC_FLOORPLAN_CEL
redirect -file $REPORTS_DIR_INIT_DESIGN/$ICC_FLOORPLAN_CEL.qor_snapshot.rpt {report_qor_snapshot -no_display}

sproc_generate_metrics

########################################################################################
# Additional reporting: zero interconnect timing report and design summaries 
########################################################################################
redirect -tee -file $REPORTS_DIR_INIT_DESIGN/$ICC_FLOORPLAN_CEL.sum {report_design_physical -all -verbose}

set_zero_interconnect_delay_mode true
redirect -tee -file $REPORTS_DIR_INIT_DESIGN/$ICC_FLOORPLAN_CEL.zic.qor {report_qor}
set_zero_interconnect_delay_mode false

########################################################################################
# Checks : Library + technology checks
########################################################################################
set_check_library_options -all
redirect -file $REPORTS_DIR_INIT_DESIGN/check_library.sum {check_library}
sproc_script_stop

