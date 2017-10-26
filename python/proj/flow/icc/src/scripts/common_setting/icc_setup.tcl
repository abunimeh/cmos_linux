puts "RM-Info: Running script [info script]\n"

##########################################################################################
# Variables for ICC-RM, ICC DP-RM, and ICC Hierarchical-RM
# Script: icc_setup.tcl
# Version: E-2010.12 (January 10, 2011)
# Copyright (C) 2007-2011 Synopsys, Inc. All rights reserved.
##########################################################################################

# sourcing the common variables
source -echo ./scripts/common_setting/common_setup.tcl 
#MM clean up noise
if {$synopsys_program_name != "mvrc"}  {
suppress_message MV-533
suppress_message PSYN-1042
suppress_message MV-038

set icc_skip_buffer_dangling_tie true
}
###############################
## General ICC variables
###############################
set ICC_INPUT_CEL                 "${DESIGN_NAME}_DCT" ;# CEL created in DCT
set PNET_METAL_LIST               ""           ;# List of metals in the design to be used for (partial) pnet options
set PNET_METAL_LIST_COMPLETE	  ""	       ;# List of metals in the design to be used for (complete) pnet options
set ICC_IN_DONT_USE_FILE          "$LIBRARY_DONT_USE_FILE" ;# file of master don't use commands 
set ICC_FIX_HOLD_PREFER_CELLS     ""           ;# Syntax: library/cell_name - Example: slow/DLY1X1 slow/DLY1X4
set ICC_MAX_AREA                  ""           ;# max_area value used during area optimization
set AREA_CRITICAL_RANGE_PRE_CTS   ""           ;# area critical range use during area opto during place_opt
set AREA_CRITICAL_RANGE_POST_CTS  ""           ;# area critical range use during area opto during post CTS opt
set AREA_CRITICAL_RANGE_POST_RT   ""           ;# area critical range use during area opto during route_opt
set POWER_CRITICAL_RANGE_PRE_CTS  ""           ;# power critical range use during area opto during place_opt
set POWER_CRITICAL_RANGE_POST_CTS ""           ;# power critical range use during area opto during post CTS opt
set POWER_CRITICAL_RANGE_POST_RT  ""           ;# power critical range use during area opto during route_opt
set ICC_NUM_CPUS                  1            ;# number of cpus for distributed processing
					       ;# specify a number greater than 1 to enable it for classic router based route_opt and insert_redundant_via commands
if {![info exists TEV(num_cores)]} {
set TEV(num_cores) 8
}
set ICC_NUM_CORES $TEV(num_cores)              ;# number of cores on the local host for multicore support
set ICC_REPORTING_EFFORT          "MED"        ;# OFF|MED|LOW when set to OFF,no reporting is done; when set to LOW, report_timing/report_qor are skipped in clock_opt_cts 
set ICC_SANITY_CHECK              TRUE        ;# TRUE|FALSE, set TRUE to perform check_physical_design
set ICC_ENABLE_CHECKPOINT	  FALSE	       ;# TRUE|FALSE, set TRUE to perform checkpoint strategy for optimization commands 
					       ;# Please ensure there's enough disk space before enabling this feature. Refer to set_checkpoint_strategy man page for details. 

set ICC_TIE_CELL_FLOW             TRUE        ;# TRUE|FALSE, set TRUE if you want TIE-CELLS to be used during opto instead of TIE-nets
set ICC_LOW_POWER_PLACEMENT	  FALSE	       ;# TRUE|FALSE, when set to TRUE, set_power_options -low_power_placement will be set to true
set LEAKAGE_POWER                 TRUE       ;# TRUE|FALSE; set to TRUE to enable leakage optimization flow
set DYNAMIC_POWER                 FALSE	       ;# TRUE|FALSE; set to TRUE to enable dynamic power optimization flow
set DFT                           TRUE	       ;# TRUE|FALSE; set to TRUE to enable scan reordering flow
set ICC_DBL_VIA                   TRUE         ;# TRUE|FALSE; set to TRUE to enable detail route wire spreading
set ICC_FIX_ANTENNA               FALSE        ;# TRUE|FALSE: set to TRUE to enable antenna fixing
set ADD_FILLER_CELL               FALSE        ;# TRUE|FALSE; set to TRUE to enable std cells filler insertion
set ICC_REDUCE_CRITICAL_AREA      TRUE         ;# TRUE|FALSE; set to TRUE to enable detail route wire spreading
set ICC_CREATE_MODEL              FALSE        ;# TRUE|FALSE; used for ILM/FRAM creation for the blocks in HRM
set ICC_INIT_DESIGN_INPUT         "VERILOG"         ;# VERILOG|DDC|MW; specify starting point
					       ;# If MW is specified, script will copy MW design library from rm_dc/work/dc to rm_icc/work 
set ADD_METAL_FILL                "ICC"        ;# NONE|ICC|HERCULES|ICV; will start metal fill
                                               ;# ICC : will start timing driven metal fill using ICC's command
                                               ;# HERCULES : will start signoff metal fill using Hercules
                                               ;# ICV : will start signoff metal fill using ICV

set PLACE_OPT_EFFORT 		 "medium"      ;# low|medium|high; choose effort level for place_opt command
set ROUTE_OPT_EFFORT 		 "medium"      ;# low|medium|high; choose effort level for route_opt command
set PLACE_OPT_CONGESTION         TRUE          ;# TRUE|FALSE; set TRUE to enable congestion removal during place_opt 


###############################
## Timing variables
###############################
set ICC_APPLY_RM_DERATING               FALSE 	;# TRUE|FALSE; when set to FALSE, the derating is assumed to be in the SDC
set ICC_LATE_DERATING_FACTOR	        1.01 	;# Late derating factor, used for both data and clock 
set ICC_EARLY_DERATING_FACTOR	        0.99 	;# Early derating factor, used for both data and clock 

set ICC_APPLY_RM_UNCERTAINTY_PRECTS     FALSE	;# TRUE|FALSE; when set to TRUE, user uncertainty will be replaced by $ICC_UNCERTAINTY_PRECTS
set ICC_APPLY_RM_UNCERTAINTY_POSTCTS    FALSE	;# TRUE|FALSE; when set to TRUE, user uncertainty will be replaced by $ICC_UNCERTAINTY_POSTCTS
set ICC_UNCERTAINTY_PRECTS_FILE         ""   	;# pre-cts uncertainty file used during place_opt
set ICC_UNCERTAINTY_POSTCTS_FILE        ""   	;# post-cts uncertainty file used during post cts opto and route_opt
set ICC_MAX_TRANSITION                  ""   	;# max_transition value set on the design
set ICC_CRITICAL_RANGE                  ""   	;# critical_range set on the design ; default = 50% of each clock period
set ICC_MAX_FANOUT                      ""   	;# max_fanout value set on the design
set ICC_FULL_ARNOLDI                    FALSE	;# TRUE|FALSE; when set to TRUE, will enable full arnoldi, i.e. no net filtering


###############################
## Floorplan Input variables          		    
###############################
set ICC_FLOORPLAN_INPUT           	"USER_FILE"   ;# DEF | FP_FILE | CREATE | USER_FILE | SKIP; "DEF" reads $ICC_IN_DEF_FILE; "FP_FILE" reads ICC_IN_FLOORPLAN_FILE;
						;# "CREATE" uses initialize_floorplan command; "USER_FILE" sources $ICC_IN_FLOORPLAN_USER_FILE; 
						;# "SKIP" skips floorplanning section
set ICC_IN_DEF_FILE		  	"./data/cordic_dff_1.def"	;# Complete floorplan file in DEF format
set ICC_IN_FLOORPLAN_FILE	  	""	;# Complete floorplan file generated by write_floorplan 
set ICC_IN_FLOORPLAN_USER_FILE	  	"./scripts/custom_scripts/custom_floorplan.tcl"	;# Complete floorplan file generated by user ;this file will simply be sourced
set ICC_IN_PIN_PAD_PHYSICAL_CONSTRAINTS_FILE ""	;# I/O constraint file generated by write_pin_pad_physical_constraints which contains pin or pad information
						;# only applies to   
set ICC_IN_PHYSICAL_ONLY_CELLS_CREATION_FILE "" ;# a file to include physical only cell creation commands to be sourced
                                                ;# e.g. create_cell {vdd1left vdd1right vdd1top vdd1bottom} pvdi
set ICC_IN_PHYSICAL_ONLY_CELLS_CONNECTION_FILE "" ;# a file to include physical only cell connection commands to be sourced
                                                  ;# e.g. derive_pg_connection -power_net $MW_POWER_NET -power_pin $MW_POWER_PORT -ground_net $MW_GROUND_NET -ground_pin $MW_GROUND_PORT -cells {vdd1left vdd1right vdd1top vdd1bottom}

set ICC_PHYSICAL_CONSTRAINTS_FILE 	""	;# script to add incremental floorplan constraints which will be sourced after read_def, read_floorplan, or floorplan creation
set CUSTOM_CONNECT_PG_NETS_SCRIPT 	"./scripts/custom_scripts/custom_derive_pg.tcl"      ;# script for customized derive_pg_connection commands which replaces the default derive_pg_connection commands in the scripts   


###############################
## MV Input variables                       
###############################
set CUSTOM_LOAD_ASCII_UPF_SCRIPT_LIST   "./scripts/custom_scripts/cordic_dff_ss_diff_supply.ICC.upf"     	;# for UPF flow with VERILOG inputs, provide a list of scripts for each power domain and top
set AO_INSTANCES                        {}     	;# list of instances that require AO synthesis (e.g. {TOP/INST2, TOP/INST3}
set CUSTOM_CREATE_VA_SCRIPT             "./scripts/custom_scripts/custom_voltage_area.tcl"     	;# script to define the voltage area creation commands for your design
set ICC_DP_AUTO_CREATE_VA               FALSE  	;# TRUE|FALSE; if TRUE, automatically creates voltage area based on user specified utilization
set CUSTOM_POWER_SWITCH_SCRIPT          "./scripts/custom_scripts/custom_power_switch.tcl"     	;# script to define the headers_footers and connect the sleep pin
set CUSTOM_SECONDARY_POWER_ROUTE_SCRIPT ""     	;# script to define the pre_route_standard_cells command for AO/RR cells.
set RR_CELLS                            ""     	;# e.g. "RSD" if each Retention Register contains RSD in its name
set ICC_UPF_PM_CELL_EXISTING		TRUE	;# TRUE|FALSE; specify if design contains pre-existing power_management cells
#set ICC_UPF_PM_CELL_EXISTING		FALSE	;# TRUE|FALSE; specify if design contains pre-existing power_management cells
set ICC_UPF_PM_CELL_INSERTION		FALSE	;# TRUE|FALSE; if TRUE, runs insert_mv_cells
set ICC_AO_STRATEGY_SINGLE_POWER_POWER_DOMAIN_LIST ""		;# list of power domains for single_power always on strategy.
set CUSTOM_AO_STRATEGY_SINGLE_POWER_CREATE_BOUND_SCRIPT ""	;# script to create bound for single power always on cells
#set ICC_AO_STRATEGY_SINGLE_POWER_POWER_DOMAIN_LIST "LEON3_misc LEON3_p1 LEON3_p3"		;# list of power domains for single_power always on strategy.
#set CUSTOM_AO_STRATEGY_SINGLE_POWER_CREATE_BOUND_SCRIPT "../../DATA_SAED/ICC_DATA/fp/leon3mp.iso_region.tcl"	;# script to create bound for single power always on cells
set CUSTOM_AO_STRATEGY_SINGLE_POWER_SET_POWER_GUIDE_SCRIPT ""	;# script to associate power guide with bounds created by $CUSTOM_AO_STRATEGY_SINGLE_POWER_CREATE_BOUND_SCRIPT

###############################
## MCMM Input variables                             
###############################
set ICC_MCMM_SCENARIOS_FILE             ""     	;# file containing all scenario definitions - example in rm_icc_scripts/mcmm.scenarios.example
set ICC_MCMM_PLACE_OPT_SCENARIOS        ""     	;# list of scenarios to be made active during place_opt; optional; by default all scenarios will be made active
set ICC_MCMM_CLOCK_OPT_PSYN_SCENARIOS   ""     	;# list of scenarios to be made active during post CTS opto (pre-route); optional; by default all scenarios will be made active
set ICC_MCMM_CLOCK_OPT_ROUTE_SCENARIOS  ""     	;# list of scenarios to be made active during clock routing; optional; by default all scenarios will be made active
set ICC_MCMM_ROUTE_SCENARIOS            ""     	;# list of scenarios to be made active during signal routing; optional; by default all scenarios will be made active
set ICC_MCMM_ROUTE_OPT_SCENARIOS        ""     	;# list of scenarios to be made active during route_opt; optional; by default all scenarios will be made active
set ICC_MCMM_CHIP_FINISH_SCENARIOS      ""     	;# list of scenarios to be made active during route_opt post chipfinish; optional; by default all scenarios will be made active
set ICC_MCMM_METAL_FILL_SCENARIOS       ""     	;# list of scenarios to be made active during metal filling; optional; by default all scenarios will be made active

set ICC_MCMM_PLACE_OPT_HIGH_CAP         FALSE  	;# TRUE|FALSE : if TRUE, enables High Capacity MCMM mode for place_opt (Adaptive MCMM)
set ICC_MCMM_CLOCK_OPT_HIGH_CAP         FALSE  	;# TRUE|FALSE : if TRUE, enables High Capacity MCMM mode for post cts opto ( pre-route) (Adaptive MCMM)

###############################
## ECO FLOW VARIABLES
###############################
set ICC_ECO_FLOW                        "NONE" 	;# NONE|UNCONSTRAINED|FREEZE_SILICON
                                               	;# UNCONSTRAINED : NO spare cell insertion ; cells can be added (pre tapeout)
                                               	;# FREEZE_SILICON : spare cell insertion/freeze silicon ECO

set ICC_SPARE_CELL_FILE                 ""     	;# TCL script to insert the spare cells, e.g. :
                                               	;# insert_spare_cells -lib_cell {INV8 DFF1} -cell_name spares -num_instances 300

set ICC_ECO_NETLIST                     ""     	;# new verilog netlist containing the ECO changes




#################################
## Clock Tree Synthesis variables
#################################
set ICC_CTS_RULE_NAME		"iccrm_clock_double_spacing" ;# specify clock routing rule name  
						;# ICC-RM will apply 2x NDR to all layers if the rule name is set to "iccrm_clock_double_spacing"
set ICC_CTS_LAYER_LIST          "M5 M4 M3 M2"           ;# clock tree layers, usually M3 and above; e.g. set ICC_CTS_LAYER_LIST "M3 M4 M5"

set ICC_CTS_REF_LIST ""
set ICC_CTS_REF_DEL_INS_ONLY ""
set ICC_CTS_REF_SIZING_ONLY ""





set ICC_CTS_SHIELD_MODE		"OFF"		;# OFF|ALL|NAMES: Default is "OFF", clock shielding is not enabled. set "ALL" or "NAMES" to enable it.
						;# set "ALL" to apply the specified $ICC_CTS_SHIELD_RULE_NAME to all clks;
						;# set "NAMES" to apply specified $ICC_CTS_SHIELD_RULE_NAME to selected $ICC_CTS_SHIELD_CLK_NAMES
						;# while rest of clks will be applied with $ICC_CTS_RULE_NAME (if specified) 
set ICC_CTS_SHIELD_RULE_NAME	""		;# specify clock shielding rule name; requires $ICC_CTS_SHIELD_SPACINGS, $ICC_CTS_SHIELD_WIDTHS to be also specified    
set ICC_CTS_SHIELD_SPACINGS	""		;# specify clock shielding spacing associated with shielding rule; a list of layer name and spacing pairs
set ICC_CTS_SHIELD_WIDTHS	""		;# specify clock shielding width associated with shielding rule: a list of layer name and width pair
set ICC_CTS_SHIELD_CLK_NAMES	""		;# specify a sub set of clock names to apply the clock shielding rule: $ICC_CTS_SHIELD_RULE_NAME; 
						;# required if $ICC_CTS_SHIELD_MODE is set to "NAMES"

set ICC_CTS_CLOCK_GATE_MERGE	FALSE		;# set TRUE to enable clock gate merging for power reduction
set ICC_CTS_CLOCK_GATE_SPLIT	FALSE		;# set TRUE to enable clock gate splitting for reducing enable pin violations

set ICC_CTS_INTERCLOCK_BALANCING	FALSE	;# set TRUE to perform ICDB
set ICC_CTS_INTERCLOCK_BALANCING_OPTIONS_FILE	"" ;# set interclock_delay options

set ICC_CTS_UPDATE_LATENCY	FALSE		;# set TRUE to perform clock latency update post CTS
set ICC_CTS_LATENCY_OPTIONS_FILE	""	;# define here the latency adjustment options options

set ICC_POST_CLOCK_ROUTE_CTO	FALSE  	       	;# set TRUE if you want to run Post route CTO after clock routing

set ICC_CTS_SELF_GATING_SAIF_FILE	""	;# SAIF file with clock activity information for self-gating logic insertion during clock tree synthesis
						;# A SAIF file is required in order to enable the self-gating feature.
			

###############################
## EMULATION TLU+ FILES
###############################
set TLUPLUS_MAX_EMULATION_FILE         ""  ;#  Max TLUplus file
set TLUPLUS_MIN_EMULATION_FILE         ""  ;#  Min TLUplus file


###############################
## PNG creation
###############################
set ICC_CREATE_GR_PNG                  FALSE  ;# set to TRUE to create the Global route congestion map PNG after initial route


###############################
## SIGNOFF_OPT Input variables
###############################
set PT_DIR ""                          ;# path to PT bin directory
set PT_SDC_FILE ""                     ;# optional file in case PT has different SDC that what is available in the ICC database
set STARRC_DIR ""                      ;# path to StarRC bin directory
set STARRC_MAX_NXTGRD ""               ;# MAX NXTGRD file
set STARRC_MIN_NXTGRD ""               ;# MIN NXTGRD file
set STARRC_MAP_FILE "$MAP_FILE"        ;# NXTGRD mapping file, defaults to TLUPlus mapping file, but could be different

set ICC_SIGNOFF_OPT_CHECK_CORRELATION_PREROUTE_SCRIPT "" ;# a file to be sourced to run check_signoff_correlation at end of place_opt_icc step; 
							 ;# example - rm_icc_scripts/signoff_opt_check_correlation_preroute_icc.example.tcl
set ICC_SIGNOFF_OPT_CHECK_CORRELATION_POSTROUTE_SCRIPT "" ;# a file to be sourced to run at check_signoff_correlation end of route_opt_icc step; 
							  ;# example - rm_icc_scripts/signoff_opt_check_correlation_postroute_icc.example.tcl

###############################
## SIGNOFF Physical variables
###############################
## Hercules - ensure env variable HERCULES_HOME_DIR is set and that hercules is included in path in shell ICC executed from
## ICV Metal Fill - ensure env variable PRIMEYIELD_HOME_DIR is set and that icv is included in path in shell ICC executed from
## ICV DRC - ensure env variable ICV_HOME_DIR is set and that icv is included in path in shell ICC executed from

set SIGNOFF_FILL_RUNSET ""             ;# ICV|Hercules runset for signoff_metal_fill
set SIGNOFF_DRC_RUNSET  ""             ;# ICV|Hercules runset for signoff_drc
set SIGNOFF_MAPFILE     ""             ;# Mapping file for ICV|Hercules signoff_metal_fill|signoff_drc
set SIGNOFF_DRC_ENGINE	"HERCULES"     ;# ICV|HERCULES 

set SIGNOFF_METAL_FILL_TIMING_DRIVEN FALSE  ;# TRUE|FALSE : set this to TRUE to enable timing driven for ICV metal fill 	
set TIMING_PRESERVE_SLACK_SETUP	"0.1"  ;# float : setup slack threshold for wire_spreading/widening/timing driven ICV metal fill; default 0.1
set TIMING_PRESERVE_SLACK_HOLD "0"     ;# float : hold slack threshold for wire_spreading/widening; default 0


###############################
## Chipfinishing variables
###############################
set ICC_METAL_FILL_SPACE           2                   ;# space amount used during ICC's insert_metal_fill command
set ICC_METAL_FILL_TIMING_DRIVEN  TRUE                 ;# enables timing driven metal fill for ICC's insert_metal_fill

## end cap cels 
set ICC_H_CAP_CEL                  ""           ;# defines the horizontal CAP CELL libcell 
set ICC_V_CAP_CEL                  ""           ;# defines the vertical CAP CELL libcell (for the Well Proximity Effect)

## antenna fixing
set ANTENNA_RULES_FILE           ""             ;# defines the antenna rules
set ICC_USE_DIODES               FALSE          ;# TRUE|FALSE; control variable to allow diodes to be inserted both by the 
                                                ;# insert_port_protection_diodes command as well as the router
set ICC_ROUTING_DIODES           ""             ;# space separated list of diode names
set ICC_PORT_PROTECTION_DIODE    ""             ;# diode name for insert_port_protection_diodes
						;# Format = library_name/diode_name
set ICC_PORT_PROTECTION_DIODE_EXCLUDE_PORTS ""  ;# a list of ports to be excluded by insert_port_protection_diodes

## filler cell insertion
set FILLER_CELL_METAL            ""             ;# space separated list of filler cells 
set FILLER_CELL             "FILL1 FILL2 FILL3 FILL4 FILL5 FILL6 FILL7 FILL7_CORNER FILL8"           ;# ADD_FILLER_CELL - space separated 

## double via insertion 
set ICC_DBL_VIA_FLOW_EFFORT      LOW            ;# LOW|MED|HIGH  - MED enables concurrent soft-rule dbl via insertion
                                                ;# HIGH runs another dbl via, timing driven, after chipfinishing
set ICC_CUSTOM_DBL_VIA_DEFINE_SCRIPT ""         ;# script to define the dbl via definitions

## signal em
set ICC_FIX_SIGNAL_EM		 FALSE		;# TRUE|FALSE; set TRUE to enable signal em fixing; please uncomment the section and follow instruction in chip_finish_icc.tcl 

## focal opt
set ICC_FOCAL_OPT_HOLD_VIOLS     ""             ;# filename|all - blank to skip; filename to fix violations from a file; specify "all" to fix all hold violations
set ICC_FOCAL_OPT_SETUP_VIOLS    ""             ;# filename|all - blank to skip; filename to fix violations from a file; specify "all" to fix all setup violations
set ICC_FOCAL_OPT_DRC_NET_VIOLS  ""             ;# filename|all - blank to skip; filename to fix violations from a file; specify "all" to fix all DRC net violations
set ICC_FOCAL_OPT_DRC_PIN_VIOLS  ""             ;# filename|all - blank to skip; filename to fix violations from a file; specify "all" to fix all DRC pin violations
set ICC_FOCAL_OPT_XTALK_VIOLS    ""             ;# filename - blank to skip; filename to fix crosstalk violations from a file



######################################################################################################################
#####################   ICC DESIGN PLANNING SPECIFIC (variables for ICC DP-RM and ICC Hierarchical-RM)  ##############
######################################################################################################################

#######################################################################
## Common variables (applied to both ICC DP RM and ICC Hierarchical RM)
#######################################################################

set ICC_DP_VERBOSE_REPORTING		FALSE		;# TRUE|FALSE; generate additional reports before placement
set ICC_DP_SET_HFNS_AS_IDEAL_THRESHOLD	""		;# integer; specify a threshold to set nets with fanout larger than it as ideal nets
set ICC_DP_SET_MIXED_AS_IDEAL		TRUE		;# TRUE|FALSE; set mixed clock/signal paths as ideal nets

set ICC_DP_FIX_MACRO_LIST		"skip"		;# ""|skip|"a_list_of_macros"; unfix all macos OR skip fix OR fix specified macros before placement
set CUSTOM_ICC_DP_PLACE_CONSTRAINT_SCRIPT ""            ;# Put your set_keepout_margin and fp_set_macro_placement_constraint in this file 
set CUSTOM_ICC_DP_PREROUTE_STD_CELL_SCRIPT "./scripts/custom_scripts/custom_preroute.tcl"		;# File to perform customized preroute_standard_cell commands
set ICC_DP_USE_ZROUTE                   TRUE            ;# TRUE|FALSE; use zroute for ICC DP RM and pin assignment of ICC Hierarchical RM

## PNS and PNA control variables
set CUSTOM_ICC_DP_PNS_CONSTRAINT_SCRIPT "./scripts/custom_scripts/custom_pns_constraint.tcl"              ;# File to add PNS constraints which is loaded before running PNS
set PNS_POWER_NETS         		"${MW_POWER_NET} ${MW_GROUND_NET}" ;# Target nets for PNS; syntax is "your_power_net your_ground_net" 
set PNS_POWER_BUDGET       		1000          	;# Unit in milliWatts; default is 1000
set PNS_VOLTAGE_SUPPLY     		1.08           	;# Unit in Volts; default is 1.5
set PNS_VIRTUAL_RAIL_LAYER 		""              ;# Specify the metal layer you want to use as virtual rail
set PNS_OUTPUT_DIR         		"./pna_output"  ;# Output directory for PNS and PNA output files

###################################################
## ICC Hierarchical RM specific variables
###################################################

set ICC_SKIP_IN_BLOCK_IMPLEMENTATION    FALSE           ;# TRUE|FALSE; set TRUE to disable "Creating the physical MV objects" and "MTCMOS CELL INSTANTIATION"
							;# sections in init_design_icc.tcl if you have already done so on full chip level
set MW_ILM_LIBS                         ""              ;# add ILMs for block level FRAMs not used by DCT
set BUDGETING_SDC_OUTPUT_DIR            "./outputs"         ;# budgeting SDC output directory; default is "./sdc"

set ICC_DP_PLANGROUP_FILE               "./scripts/custom_scripts/custom_plangroup.tcl"              ;# floorplan file containing plan group creation and location which should be the output of write_floorplan

set ICC_DP_CTP				FALSE		;# TRUE|FALSE; set TRUE to enable clock tree planning; please uncomment the section in hierarchical_dp.tcl first
set ICC_DP_CTP_ANCHOR_CEL               ""              ;# anchor cell for clock tree planning (anchor cell is required if you uncomment clock tree planning in scripts);
							;#   cell master of one mid-sized buffer
set ICC_DP_ALLOW_FEEDTHROUGH	        FALSE		;# TRUE|FALSE; allow feedthrough creation during pin assignment 

set CUSTOM_ICC_DP_PNS_SCRIPT 		"./scripts/custom_scripts/custom_pns.tcl"              ;# customized PNS script; replacing PNS section in scripts
set CUSTOM_ICC_DP_PNA_SCRIPT 		""              ;# customized PNA script; replacing PNA section in scripts

## DFT-aware hierarchical design planning variables 
set ICC_DP_DFT_FLOW			TRUE		;# TRUE|FALSE; enable DFT-aware hierarchical design planning flow; requires ICC_IN_FULL_CHIP_SCANDEF_FILE
set ICC_IN_FULL_CHIP_SCANDEF_FILE "./data/$DESIGN_NAME.mapped.scandef"		
							;# ASCII full-chip SCANDEF file for DFT-aware hierarchical design planning flow (ICC_DP_DFT_FLOW)
							;# it is used for hierarchical design planning phase; not needed for block level implementations




##########################################################################################
#####################      NO NEED TO CHANGE IF DC-RM IS USED BEFORE          ##############
##########################################################################################

set ICC_IN_VERILOG_NETLIST_FILE "./data/cordic_dff.syn.v" ;#1 to n verilog input files, spaced by blanks
set ICC_IN_SDC_FILE             "./data/cordic_dff.syn.sdc"
set ICC_IN_DDC_FILE             "./data/$DESIGN_NAME.mapped.ddc"
set ICC_IN_UPF_FILE             "./data/top_gates.upf"
set ICC_IN_SCAN_DEF_FILE        "./data/$DESIGN_NAME.mapped.scandef"

##########################################################################################
#########################     USAGE OF ABOVE VARIABLES      ##############################
#########################   DO NOT CHANGE BELOW THIS LINE   ##############################
##########################################################################################

set ICC_IN_SAIF_FILE            "$DESIGN_NAME.saif"     ;# SAIF file for dynamic power opto
set ICC_SAIF_INSTANCE_NAME      $DESIGN_NAME            ;# the instance in the SAIF file containing the switching activity

if {[info exists SEV(rpt_dir)]} {
  set REPORTS_DIR $SEV(rpt_dir)				;# Directory to write reports.
} else {
  set REPORTS_DIR "../reports/null"				;# Directory to write reports.
}
if {[info exists SEV(dst_dir)]} {
  set RESULTS_DIR $SEV(dst_dir)				;# Directory to write output data files
} else {
  set RESULTS_DIR "../outputs/null"				;# Directory to write output data files
}
set MW_DESIGN_LIBRARY           "./${DESIGN_NAME}_LIB"    ;# milkyway design library
###Colin Comment - Added the following variable to define the Block Level Design Library for LAB3: 
set MW_DESIGN_LIBRARY_LAB3      "./lib_switchable_0"    ;# Block Level milkyway design library

set REPORTS_DIR_INIT_DESIGN                     $REPORTS_DIR
set REPORTS_DIR_PLACE_OPT                       $REPORTS_DIR
set REPORTS_DIR_CLOCK_OPT_CTS                   $REPORTS_DIR
set REPORTS_DIR_CLOCK_OPT_PSYN                  $REPORTS_DIR
set REPORTS_DIR_CLOCK_OPT_ROUTE                 $REPORTS_DIR
set REPORTS_DIR_ROUTE                           $REPORTS_DIR
set REPORTS_DIR_ROUTE_OPT                       $REPORTS_DIR
set REPORTS_DIR_CHIP_FINISH                     $REPORTS_DIR
set REPORTS_DIR_ECO                        	$REPORTS_DIR
set REPORTS_DIR_FOCAL_OPT                       $REPORTS_DIR
set REPORTS_DIR_SIGNOFF_OPT                     $REPORTS_DIR
set REPORTS_DIR_METAL_FILL                      $REPORTS_DIR
set REPORTS_DIR_DP            			$REPORTS_DIR
set REPORTS_DIR_DP_CREATE_PLANGROUPS		$REPORTS_DIR
set REPORTS_DIR_DP_ROUTEABILITY_ON_PLANGROUPS   $REPORTS_DIR
set REPORTS_DIR_DP_PIN_ASSIGNMENT_BUDGETING     $REPORTS_DIR
set REPORTS_DIR_DP_COMMIT                       $REPORTS_DIR
set REPORTS_DIR_DP_PREPARE_BLOCK                $REPORTS_DIR
set REPORTS_DIR_FORMALITY			$REPORTS_DIR

if { ! [file exists $REPORTS_DIR_INIT_DESIGN] } { file mkdir $REPORTS_DIR_INIT_DESIGN }
if { ! [file exists $REPORTS_DIR_PLACE_OPT] } { file mkdir $REPORTS_DIR_PLACE_OPT }
if { ! [file exists $REPORTS_DIR_CLOCK_OPT_CTS] } { file mkdir $REPORTS_DIR_CLOCK_OPT_CTS }
if { ! [file exists $REPORTS_DIR_CLOCK_OPT_PSYN] } { file mkdir $REPORTS_DIR_CLOCK_OPT_PSYN }
if { ! [file exists $REPORTS_DIR_CLOCK_OPT_ROUTE] } { file mkdir $REPORTS_DIR_CLOCK_OPT_ROUTE }
if { ! [file exists $REPORTS_DIR_ROUTE] } { file mkdir $REPORTS_DIR_ROUTE }
if { ! [file exists $REPORTS_DIR_ROUTE_OPT] } { file mkdir $REPORTS_DIR_ROUTE_OPT }
if { ! [file exists $REPORTS_DIR_CHIP_FINISH] } { file mkdir $REPORTS_DIR_CHIP_FINISH }
if { ! [file exists $REPORTS_DIR_ECO] } { file mkdir $REPORTS_DIR_ECO }
if { ! [file exists $REPORTS_DIR_FOCAL_OPT] } { file mkdir $REPORTS_DIR_FOCAL_OPT }
if { ! [file exists $REPORTS_DIR_SIGNOFF_OPT] } { file mkdir $REPORTS_DIR_SIGNOFF_OPT }
if { ! [file exists $REPORTS_DIR_METAL_FILL] } { file mkdir $REPORTS_DIR_METAL_FILL }
if { ! [file exists $REPORTS_DIR_DP] } { file mkdir $REPORTS_DIR_DP }
if { ! [file exists $REPORTS_DIR_DP_CREATE_PLANGROUPS] } { file mkdir $REPORTS_DIR_DP_CREATE_PLANGROUPS }
if { ! [file exists $REPORTS_DIR_DP_ROUTEABILITY_ON_PLANGROUPS] } { file mkdir $REPORTS_DIR_DP_ROUTEABILITY_ON_PLANGROUPS }
if { ! [file exists $REPORTS_DIR_DP_PIN_ASSIGNMENT_BUDGETING] } { file mkdir $REPORTS_DIR_DP_PIN_ASSIGNMENT_BUDGETING }
if { ! [file exists $REPORTS_DIR_DP_COMMIT] } { file mkdir $REPORTS_DIR_DP_COMMIT }
if { ! [file exists $REPORTS_DIR_DP_PREPARE_BLOCK] } { file mkdir $REPORTS_DIR_DP_PREPARE_BLOCK }
if { ! [file exists $REPORTS_DIR_FORMALITY] } { file mkdir $REPORTS_DIR_FORMALITY }


## Logical libraries
  set_app_var search_path	". ./scripts/custom_scripts ./scripts/common_setting ../../scripts_block/rm_icc_dp_scripts $ADDITIONAL_SEARCH_PATH $search_path" 
if {$synopsys_program_name != "mvrc"}  {
  set_app_var target_library	"$TARGET_LIBRARY_FILES"
}
  set_app_var link_library	"* $TARGET_LIBRARY_FILES $synthetic_library"

if { ! [file exists $RESULTS_DIR] } {
  file mkdir $RESULTS_DIR
}
if { ! [file exists $REPORTS_DIR] } {
  file mkdir $REPORTS_DIR
}


#################################################################################


puts "RM-Info: Completed script [info script]\n"
