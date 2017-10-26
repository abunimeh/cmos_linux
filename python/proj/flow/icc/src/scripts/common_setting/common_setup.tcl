puts "RM-Info: Running script [info script]\n"

##########################################################################################
# Variables common to all RM scripts
# Script: common_setup.tcl
# Version: D-2010.03-SP1 (May 24, 2010)
# Copyright (C) 2007-2010 Synopsys, Inc. All rights reserved.
##########################################################################################

#Changed the setup on july26 at 7:21 to point to lynx techlib which has latest memories and IO libs updated

set DESIGN_NAME                   "cordic_dff"  ;#  The name of the top-level design

set PWD [pwd]
set pwdlength [string length $PWD]
set rootindexfirst 0
set rootindexlast [expr ($pwdlength -32)]
set ROOT_DIR [string range $PWD $rootindexfirst $rootindexlast]
set DESIGN_REF_PATH /workspace/cpu1/hsbe/qianxf/cpu1/upf/SAED90NM.SNPS.A.2010_12_20.alpha
set DESIGN_REF_TECH_PATH          "${DESIGN_REF_PATH}/tech"

##########################################################################################
# Hierarchical Flow Design Variables
##########################################################################################

set HIERARCHICAL_DESIGNS           "" ;# List of hierarchical block design names "DesignA DesignB" ...
set HIERARCHICAL_CELLS             "" ;# List of hierarchical block cell instance names "u_DesignA u_DesignB" ...

##########################################################################################
# Library Setup Variables
##########################################################################################

# For the following variables, use a blank space to separate multiple entries
# Example: set TARGET_LIBRARY_FILES "lib1.db lib2.db lib3.db"
#        /global/pilot_support/techlib/montana/SAED_EDK90nm_July16/SAED_EDK90nm/level_shifters/models \

set ADDITIONAL_SEARCH_PATH      " \
        ${DESIGN_REF_PATH} \
        /workspace/cpu1/hsbe/meic/upf/std_cell "

set TARGET_LIBRARY_FILES    " \
   /workspace/cpu0/hsbe/chenyl/hl40lp18t/synopsys/siliconsmart/ccs/release/0518/lib/tt_1.1v_85.db "

set synthetic_library "/tools/synopsys/syn/syn_K-2015.06/libraries/syn/dw_foundation.sldb"




#set MW_REFERENCE_LIB_DIRS  " \
#       	/library/HL40LP/std_cell/18track/v1p3/milkway/hl40lp18t_mw \ 
#        /library/HL40LP/std_cell/18track/v2p0/milkway/mv_lp_mw \
#        /library/HL40LP/std_cell/18track/v2p0/milkway/mv_ls_mw \
#        /library/HL40LP/std_cell/18track/v2p0/milkway/mv_rdf_hd_mw \
#        /library/HL40LP/std_cell/18track/v2p0/milkway/mv_aon_mw \
#"
set MW_REFERENCE_LIB_DIRS  " \
       /workspace/cpu0/hsbe/chenyl/hl40lp18t/synopsys/siliconsmart/v2p0_BK/try_0517/milkyway/hl40lp18t_mw \ 
"



set MIN_LIBRARY_FILES   " \    
      /workspace/cpu0/hsbe/chenyl/hl40lp18t/synopsys/siliconsmart/ccs/release/0518/lib/tt_1.1v_85.db"


set MW_REFERENCE_CONTROL_FILE     ""  ;#  Reference Control file to define the MW ref libs
set TECH_FILE                     "/workspace/cpu1/hsbe/jiangz/LIB/techfile/ICC/HLMC_cl040lp_1p7m_601.tf"
set MAP_FILE                      "/workspace/cpu1/hsbe/jiangz/LIB/techfile/ICC/layer_1p7m.map"
set TLUPLUS_MAX_FILE              "/library/process/HL/40/deck/HLMC_cl040lp_1p7m_601_tlup_v1p3/HLMC_cl040lp_1p7m_601_cworst.tlup"
set TLUPLUS_MIN_FILE              "/library/process/HL/40/deck/HLMC_cl040lp_1p7m_601_tlup_v1p3/HLMC_cl040lp_1p7m_601_cbest.tlup"




set MW_POWER_NET                "VDD" ;#
set MW_POWER_PORT               "VDD" ;#
set MW_GROUND_NET               "GND" ;#
set MW_GROUND_PORT              "GND" ;#

set MIN_ROUTING_LAYER            "M2"   ;# Min routing layer
set MAX_ROUTING_LAYER            "M6"   ;# Max routing layer

set LIBRARY_DONT_USE_FILE        "./scripts/custom_scripts/use_tie.tcl"   ;# Tcl file with library modifications for dont_use

##########################################################################################
# Multi-Voltage Common Variables
#
# Define the following MV common variables for the RM scripts for multi-voltage flows.
# Use as few or as many of the following definitions as needed by your design.
##########################################################################################

set PD1                          ""           ;# Name of power domain/voltage area  1
set PD1_CELLS                    ""           ;# Instances to include in power domain/voltage area 1
set VA1_COORDINATES              {}           ;# Coordinates for voltage area 1
set MW_POWER_NET1                "VDD1"       ;# Power net for voltage area 1
set MW_POWER_PORT1               "VDD"        ;# Power port for voltage area 1

set PD2                          ""           ;# Name of power domain/voltage area  2
set PD2_CELLS                    ""           ;# Instances to include in power domain/voltage area 2
set VA2_COORDINATES              {}           ;# Coordinates for voltage area 2
set MW_POWER_NET2                "VDD2"       ;# Power net for voltage area 2
set MW_POWER_PORT2               "VDD"        ;# Power port for voltage area 2

set PD3                          ""           ;# Name of power domain/voltage area  3
set PD3_CELLS                    ""           ;# Instances to include in power domain/voltage area 3
set VA3_COORDINATES              {}           ;# Coordinates for voltage area 3
set MW_POWER_NET3                "VDD3"       ;# Power net for voltage area 3
set MW_POWER_PORT3               "VDD"        ;# Power port for voltage area 3

set PD4                          ""           ;# Name of power domain/voltage area  4
set PD4_CELLS                    ""           ;# Instances to include in power domain/voltage area 4
set VA4_COORDINATES              {}           ;# Coordinates for voltage area 4
set MW_POWER_NET4                "VDD4"       ;# Power net for voltage area 4
set MW_POWER_PORT4               "VDD"        ;# Power port for voltage area 4

puts "RM-Info: Completed script [info script]\n"
