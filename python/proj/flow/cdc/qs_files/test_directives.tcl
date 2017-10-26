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
sdc load test.sdc

# Add CDC constraints
cdc preference reconvergence -depth 1 -divergence_depth 1 
cdc preference -fifo_scheme -handshake_scheme

#read exception sdc
