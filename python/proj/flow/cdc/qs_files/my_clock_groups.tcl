netlist clock clk400_i -group clockmacros  -add
netlist clock clk300_i -group clockmacros  -add
netlist clock clk200_i -group clockmacros  -add
netlist clock clk100_i -group clockmacros  -add
netlist clock clk400_i -group clockmacros  -add
netlist clock clk100_virt -group clockmacros -add
netlist clock clk200_virt -group clockmacros -add
netlist clock clk300_virt -group clockmacros -add

netlist clock clkP   -group allPclock -add
netlist clock u_leg_corner_b.u_leg_pma.u_clk_mux_2_u_ckmux2.d0 -group allPclock -add
netlist clock u_leg_corner_b.u_leg_pmb.u_clk_mux_2_u_ckmux2.d0 -group allPclock -add
netlist clock u_leg_corner_b.u_leg_pmb.u_clk_mux_0_u_ckmux2.d0 -group allPclock -add
netlist clock u_leg_corner_b.u_leg_pmb.u_clk_mux_3_u_ckmux2.d0 -group allPclock -add

netlist clock clk_shift  -group allShifts -add 
netlist clock clk_shift_prog -group allShifts -add
netlist clock clk_shift_bist -group allShifts -add

## add clcokP to it's virtual  sons
netlist clock { clkP }  -group Group_LOADER_clkP_virt  -add

netlist clock clk_bist -group  meta_corner -add
netlist clock clk_edt -group  meta_corner -add
netlist clock clk25_virt -group  meta_corner -add

