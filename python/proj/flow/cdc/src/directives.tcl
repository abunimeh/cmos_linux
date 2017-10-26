####### Define clocks
######netlist clock cpu_clk_in -period 50
######netlist clock core_clk_in -period 60 
######netlist clock mac_clk_in -period 50 
######
####### Define constants
######netlist constant scan_mode 1'b0
######
####### Add CDC constraints
######cdc preference reconvergence -depth 1 -divergence_depth 1 
######cdc preference -fifo_scheme -handshake_scheme


# Define clocks
netlist clock { pll_clk } -period 2.22 -waveform { 0 1.11 } -group 1
netlist clock { ext_clk } -period 2.22 -waveform { 0 1.11 } -group 1
#netlist clock { u_core.u_clk_sel.clk_o } -period 2.22 -waveform { 0 1.11 } -group 1
#netlist clock { serial_clk } -period 40.00 -waveform { 0 20.00 } -group 2
netlist clock { serial_clk_x10 } -period 4.0 -waveform { 0 2.0} -group 3
netlist clock { tck_pad_i } -period 200 -waveform { 0 100} -group 4

# Define constants
netlist constant { clk_sel } 1'b1
netlist constant { core_clk_en } 1'b1

# Add CDC constraints
#cdc preference reconvergence -depth 1 -divergence_depth 1 
#cdc preference -fifo_scheme -handshake_scheme

#reset
#netlist reset core_rst_n -active_low -async
#netlist reset serial_rst_n -active_low -async
