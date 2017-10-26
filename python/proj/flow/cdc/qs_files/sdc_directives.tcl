# THIS FILE CONTAINS DIRECTIVES FOR CRYSTAL4S - just sdc load
# Define clocks
### directives taken from func mode
#  -- directivs for cornet block from func sdc
#

#memories to be treated as abstract
netlist memory -abstract ST_DPREG_RL_BB_16x64m1B2_T
netlist memory -abstract ST_DPREG_RL_BB_64x192m1B2_TR
netlist memory -abstract ST_DPREG_RL_BB_64x24m2B2_T
netlist memory -abstract ST_SPHD_RL_BB_4096x137m8B1_TR
netlist memory -abstract ST_SPREG_RL_BB_128x14m4B1_T
netlist memory -abstract ST_SPREG_RL_BB_128x20m4B1_T
netlist memory -abstract ST_SPREG_RL_BB_16x32m2B1_T
netlist memory -abstract ST_SPREG_RL_BB_256x14m4B1_T
netlist memory -abstract ST_SPREG_RL_BB_64x17m2B1_T

#
# Define constants
#sdc load data/CORNER_func_clock.sdc
#sdc load data/CORNER_func_io.sdc
#sdc load data/CORNER_func_except.sdc
# all together
#sdc load data/bug_sdc.sdc
#sdc load data/merged_sdc.sdc
#sdc load data/modified.sdc

source ../../../../../share/cdc/qs_files/base_tcl_from_sdc.tcl
#source qs_files/my_clock_groups.tcl

#reset
netlist reset rst_n
netlist reset en1200_resetn* ; #sounds like reset so I hope it is
#bist is ignored in these checks
netlist reset rst_bistctlr_n -ignore
###  additional setup
## unable bist
netlist constant u_CMEM1.bist_mode 0
netlist constant u_VW.u_OUT2_13.bist_mode 0
netlist constant *.bist_mode 0
netlist constant *.*.bist_mode 0

netlist constant *.atpg_at_speed 0
netlist constant atpg_at_speed 0

##  whateven bugs we found we can coner an continue
source ../../../../../share/cdc/qs_files/bugs_covr_assertions.tcl
#
## just set scan on 0 - might help the analysis in functional mode
netlist constant scan_enable_a* 0
netlist constant scan_enable_b* 0

#ignore bist clock
cdc clock attribute -group bist_group -ignore
cdc clock attribute -group meta_corner -ignore


# Add CDC constraints
cdc preference reconvergence -depth 1 -divergence_depth 1 
cdc preference -fifo_scheme -handshake_scheme

#read exception sdc
