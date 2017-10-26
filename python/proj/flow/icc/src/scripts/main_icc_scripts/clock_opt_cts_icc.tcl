
set TEV(num_cores) 1

set SEV(src) place_opt_icc
set SEV(dst) clock_opt_cts_icc

set SEV(script_file) [info script]

source ./scripts/common_setting/lcrm_setup/lcrm_setup.tcl

sproc_script_start
source -echo ./scripts/common_setting/icc_setup.tcl 
set ICC_PLACE_OPT_CEL $SEV(src) 
set ICC_CLOCK_OPT_CTS_CEL $SEV(dst) 

###########################################################
## clock_opt_cts_icc: Clock Tree Synthesis and Optimization 
###########################################################
set upf_create_implicit_supply_sets false

 
open_mw_lib $MW_DESIGN_LIBRARY
redirect /dev/null "remove_mw_cel -version_kept 0 ${ICC_CLOCK_OPT_CTS_CEL}" 
copy_mw_cel -from $ICC_PLACE_OPT_CEL -to $ICC_CLOCK_OPT_CTS_CEL
open_mw_cel $ICC_CLOCK_OPT_CTS_CEL

## Optimization Common Session Options - set in all sessions
### ./scripts/common_setting/common_optimization_settings_icc.tcl
### ./scripts/common_setting/common_placement_settings_icc.tcl
source -echo common_optimization_settings_icc.tcl
source -echo common_placement_settings_icc.tcl



## Source CTS Options 
### ./scripts/common_setting/common_cts_settings_icc.tcl
source -echo common_cts_settings_icc.tcl


set_app_var cts_instance_name_prefix CTS

  check_mv_design -verbose

##############################
## RP : Relative Placement  ##                
##############################
## Ensuring that the RP cells are not changed during clock_opt
#set_rp_group_options [all_rp_groups] -cts_option fixed_placement
#set_rp_group_options [all_rp_groups] -cts_option "size_only"


set_delay_calculation -routed_clock arnoldi


#if {$ICC_CTS_CLOCK_GATE_SPLIT} {
# report_split_clock_gates_options
# set_optimize_pre_cts_power_options -split_clock_gates true
#}


#if {$ICC_SANITY_CHECK} {
        check_physical_design -stage pre_clock_opt -no_display -output $REPORTS_DIR_CLOCK_OPT_CTS/check_physical_design.pre_clock_opt 
#}

#if {$ICC_ENABLE_CHECKPOINT} {
echo "SCRIPT-Info : Please ensure there's enough disk space before enabling the set_checkpoint_strategy feature."
set_checkpoint_strategy -enable -overwrite
# The -overwrite option is used by default. Remove it if needed.
#}

# A SAIF file is required in order to enable the self-gating feature.
#if {[file exists [which $ICC_CTS_SELF_GATING_SAIF_FILE]]} {read_saif -input $ICC_CTS_SELF_GATING_SAIF_FILE -instance_name $ICC_SAIF_INSTANCE_NAME}

set clock_opt_cts_cmd "clock_opt -only_cts -no_clock_route"
#if {$ICC_CTS_CLOCK_GATE_MERGE || $ICC_CTS_CLOCK_GATE_SPLIT || $ICC_LOW_POWER_PLACEMENT} {lappend clock_opt_cts_cmd -power}
#if {$ICC_CTS_INTERCLOCK_BALANCING && [file exists [which $ICC_CTS_INTERCLOCK_BALANCING_OPTIONS_FILE]]} {lappend clock_opt_cts_cmd -inter_clock_balance}
#if {$ICC_CTS_UPDATE_LATENCY} {lappend clock_opt_cts_cmd -update_clock_latency}
#if {[file exists [which $ICC_CTS_SELF_GATING_SAIF_FILE]]} {lappend clock_opt_cts_cmd -insert_self_gating}
echo $clock_opt_cts_cmd
eval $clock_opt_cts_cmd

#if {$ICC_ENABLE_CHECKPOINT} {set_checkpoint_strategy -disable}

if { [check_error -verbose] != 0} { echo "SCRIPT-Error, flagging ..." }

########################################
#           CONNECT P/G                #
########################################


## Connect Power & Ground for non-MV and MV-mode

#if {[file exists [which $CUSTOM_CONNECT_PG_NETS_SCRIPT]]} {
#  source -echo $CUSTOM_CONNECT_PG_NETS_SCRIPT
#} else {
#   if {!$ICC_TIE_CELL_FLOW} {derive_pg_connection -verbose -tie}
    redirect -file $REPORTS_DIR_CLOCK_OPT_CTS/clock_opt_cts.mv {check_mv_design -verbose}
#  }
if { [check_error -verbose] != 0} { echo "SCRIPT-Error, flagging ..." }

### ../../../scripts_block/rm_icc_scripts/common_post_cts_timing_settings.tcl
source -echo common_post_cts_timing_settings.tcl
  #ideal network
  remove_ideal_network [all_fanout -flat -clock_tree]

  #set fix hold 
  set_fix_hold [all_clocks]


#if {$ICC_REPORTING_EFFORT != "OFF" } {
    redirect -tee -file $REPORTS_DIR_CLOCK_OPT_CTS/$ICC_CLOCK_OPT_CTS_CEL.clock_tree {report_clock_tree -summary}     ;# global skew report
     redirect -file $REPORTS_DIR_CLOCK_OPT_CTS/$ICC_CLOCK_OPT_CTS_CEL.clock_timing {report_clock_timing -type skew} ;# local skew report
#}

#if {$ICC_REPORTING_EFFORT == "MED" } {
 redirect -file $REPORTS_DIR_CLOCK_OPT_CTS/$ICC_CLOCK_OPT_CTS_CEL.max.tim {report_timing -capacitance -transition_time -input_pins -nets -delay max} 
 redirect -file $REPORTS_DIR_CLOCK_OPT_CTS/$ICC_CLOCK_OPT_CTS_CEL.min.tim {report_timing -capacitance -transition_time -input_pins -nets -delay min} 
#}
#if {$ICC_REPORTING_EFFORT == "MED" } {
   redirect -tee -file $REPORTS_DIR_CLOCK_OPT_CTS/$ICC_CLOCK_OPT_CTS_CEL.qor {report_qor}
   redirect -tee -file $REPORTS_DIR_CLOCK_OPT_CTS/$ICC_CLOCK_OPT_CTS_CEL.qor -append {report_qor -summary}
   redirect -file $REPORTS_DIR_CLOCK_OPT_CTS/$ICC_CLOCK_OPT_CTS_CEL.con {report_constraints}
#}


save_mw_cel -as $ICC_CLOCK_OPT_CTS_CEL

#if {$ICC_REPORTING_EFFORT != "OFF" } {
   redirect -file $REPORTS_DIR_CLOCK_OPT_CTS/$ICC_CLOCK_OPT_CTS_CEL.placement_utilization.rpt {report_placement_utilization -verbose}
   create_qor_snapshot -clock_tree -name $ICC_CLOCK_OPT_CTS_CEL
   redirect -file $REPORTS_DIR_CLOCK_OPT_CTS/$ICC_CLOCK_OPT_CTS_CEL.qor_snapshot.rpt {report_qor_snapshot -no_display}
#}

# Lynx compatible procedure which produces design metrics based on reports
sproc_generate_metrics

# Lynx Compatible procedure which performs final metric processing and exits
sproc_script_stop
