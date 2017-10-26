################################################################
#  changes by ezra to reflect clock groups
################################################################

netlist clock clk400_i -group clockmacros  
netlist clock clk300_i -group clockmacros  
netlist clock clk200_i -group clockmacros  
netlist clock clk100_i -group clockmacros  
netlist clock clk400_i -group clockmacros  
netlist clock clk100_virt -group clockmacros 
netlist clock clk200_virt -group clockmacros 
netlist clock clk300_virt -group clockmacros 
netlist clock clkM300_virt -group clockmacros 
netlist clock u_CORNER0.clk100_MA_virt -group clockmacros 
netlist clock u_CORNER1.clk100_MA_virt -group clockmacros 
netlist clock u_CORNER2.clk100_MA_virt -group clockmacros 
netlist clock u_CRY0.u_CORNER0.clk200_to_trace_virt -group clockmacros 
netlist clock u_CRY0.u_CORNER1.clk200_to_trace_virt -group clockmacros 
#derived clock
netlist clock u_CLOCK_200_u_CKI.Z -group clockmacros 
#I am not sure about this - it's external pins which are asynchronous to the group of macro clock 
#netlist clock macro_clk_0 -group clockmacros 
#netlist clock macro_clk_1 -group clockmacros 
#netlist clock macro_clk_2 -group clockmacros 
#netlist clock macro_clk_3 -group clockmacros 
#netlist clock macro_clk_4 -group clockmacros 


netlist clock clk_shift  -group allShifts  
netlist clock clk_shift_prog -group allShifts 
netlist clock clk_shift_bist -group allShifts 

netlist clock clk_bist -group  meta_corner 
netlist clock clk_edt -group  meta_corner 
netlist clock clk25_virt -group  meta_corner 

## add clcokP to it's virtual  sons
netlist clock { clkP }  -group Group_LOADER_clkP_virt  
# put all the clkP derived clock as synchronus to each other (take the group name from the generated_clock from SDC)
netlist clock u_leg_corner_b.u_leg_pma.u_clk_mux_2_u_ckmux2.d0 -group Group_LOADER_clkP_virt 
netlist clock u_leg_corner_b.u_leg_pmb.u_clk_mux_2_u_ckmux2.d0 -group Group_LOADER_clkP_virt 
netlist clock u_leg_corner_b.u_leg_pmb.u_clk_mux_0_u_ckmux2.d0 -group Group_LOADER_clkP_virt 
netlist clock u_leg_corner_b.u_leg_pmb.u_clk_mux_3_u_ckmux2.d0 -group Group_LOADER_clkP_virt 

#virtual clk_25 to the same group
netlist clock clk25_virt -group Group_LOADER_clkP_virt 
#LOADER/clkP in the sdc assign to the same group
netlist clock clk_a_i -group Group_LOADER_clkP_virt 
netlist clock clk_b_i -group Group_LOADER_clkP_virt 
netlist clock clk_c_i -group Group_LOADER_clkP_virt 

netlist clock u_CORNER1.clkP_virt -group Group_LOADER_clkP_virt 
netlist clock u_CORNER0.clkP_virt -group Group_LOADER_clkP_virt 
netlist clock u_CORNER0.u_PR_FIFO_B.fifo.clkP_virt -group Group_LOADER_clkP_virt 
netlist clock u_CORNER1.u_PR_FIFO_B.fifo.clkP_virt -group Group_LOADER_clkP_virt 
netlist clock u_CORNER3.clkP_virt -group Group_LOADER_clkP_virt 
netlist clock u_CORNER3.u_PR_FIFO_B.fifo.clkP_virt -group Group_LOADER_clkP_virt 
netlist clock u_FUMEM_0.clkP_virt -group Group_LOADER_clkP_virt 
netlist clock u_FUMEM_0.u_PR_FIFO.fifo.clkP_virt -group Group_LOADER_clkP_virt 
netlist clock u_LOADER_0.u_PR_FIFO_RI.fifo.clkP_virt -group Group_LOADER_clkP_virt 
netlist clock u_TRACE_0.clkP_virt -group Group_LOADER_clkP_virt 
netlist clock u_TRACE_0.u_PR_FIFO.fifo.clkP_virt -group Group_LOADER_clkP_virt 
#netlist clock clk_default_virt -group Group_LOADER_clkP_virt 
#
#These wrappers - I realy dont know if and how to group them
##netlist clock u_LEG_CORNER_A.u_LEG_PMB.u_C32_PM_CONTROL.gen_logic_lprvt_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_u_logic_lprvt.SPEEDOUT_NMOS -group Group_LOADER_clkP_virt 
##netlist clock u_LEG_CORNER_A.u_LEG_PMB.u_C32_PM_CONTROL.gen_logic_lprvt_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_u_logic_lprvt.SPEEDOUT_PMOS -group Group_LOADER_clkP_virt 
##netlist clock u_LEG_CORNER_A.u_LEG_PMB.u_C32_PM_CONTROL.gen_logic_lprvt_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_u_logic_lprvt.LEAK_OUT -group Group_LOADER_clkP_virt 
##netlist clock u_LEG_CORNER_A.u_LEG_PMB.u_C32_PM_CONTROL.gen_logic_lplvt_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_u_logic_lplvt.SPEEDOUT_NMOS -group Group_LOADER_clkP_virt 
##netlist clock u_LEG_CORNER_A.u_LEG_PMB.u_C32_PM_CONTROL.gen_logic_lplvt_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_u_logic_lplvt.SPEEDOUT_PMOS -group Group_LOADER_clkP_virt 
##netlist clock u_LEG_CORNER_A.u_LEG_PMB.u_C32_PM_CONTROL.gen_logic_lplvt_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_u_logic_lplvt.LEAK_OUT -group Group_LOADER_clkP_virt 
##netlist clock u_LEG_CORNER_A.u_LEG_PMB.u_C32_PM_CONTROL.gen_logic_lprvt_p4_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_p4_u_logic_lprvt_p4.SPEEDOUT_NMOS -group Group_LOADER_clkP_virt 
##netlist clock u_LEG_CORNER_A.u_LEG_PMB.u_C32_PM_CONTROL.gen_logic_lprvt_p4_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_p4_u_logic_lprvt_p4.SPEEDOUT_PMOS -group Group_LOADER_clkP_virt 
##netlist clock u_LEG_CORNER_A.u_LEG_PMB.u_C32_PM_CONTROL.gen_logic_lprvt_p4_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_p4_u_logic_lprvt_p4.LEAK_OUT -group Group_LOADER_clkP_virt 
##netlist clock u_LEG_CORNER_A.u_LEG_PMB.u_C32_PM_CONTROL.gen_logic_lplvt_p4_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_p4_u_logic_lplvt_p4.SPEEDOUT_NMOS -group Group_LOADER_clkP_virt 
##netlist clock u_LEG_CORNER_A.u_LEG_PMB.u_C32_PM_CONTROL.gen_logic_lplvt_p4_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_p4_u_logic_lplvt_p4.SPEEDOUT_PMOS -group Group_LOADER_clkP_virt 
##netlist clock u_LEG_CORNER_A.u_LEG_PMB.u_C32_PM_CONTROL.gen_logic_lplvt_p4_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_p4_u_logic_lplvt_p4.LEAK_OUT -group Group_LOADER_clkP_virt 
##netlist clock u_LEG_CORNER_A.u_LEG_PMB.u_C32_PM_CONTROL.gen_logic_lprvt_p10_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_p10_u_logic_lprvt_p10.SPEEDOUT_NMOS -group Group_LOADER_clkP_virt 
##netlist clock u_LEG_CORNER_A.u_LEG_PMB.u_C32_PM_CONTROL.gen_logic_lprvt_p10_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_p10_u_logic_lprvt_p10.SPEEDOUT_PMOS -group Group_LOADER_clkP_virt 
##netlist clock u_LEG_CORNER_A.u_LEG_PMB.u_C32_PM_CONTROL.gen_logic_lprvt_p10_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_p10_u_logic_lprvt_p10.LEAK_OUT -group Group_LOADER_clkP_virt 
##netlist clock u_LEG_CORNER_A.u_LEG_PMB.u_C32_PM_CONTROL.gen_logic_lplvt_p10_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_p10_u_logic_lplvt_p10.SPEEDOUT_NMOS -group Group_LOADER_clkP_virt 
##netlist clock u_LEG_CORNER_A.u_LEG_PMB.u_C32_PM_CONTROL.gen_logic_lplvt_p10_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_p10_u_logic_lplvt_p10.SPEEDOUT_PMOS -group Group_LOADER_clkP_virt 
##netlist clock u_LEG_CORNER_A.u_LEG_PMB.u_C32_PM_CONTROL.gen_logic_lplvt_p10_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_p10_u_logic_lplvt_p10.LEAK_OUT -group Group_LOADER_clkP_virt 
##netlist clock u_LEG_CORNER_A.u_LEG_PMB.u_C32_PM_CONTROL.gen_sram_lprvt_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_sram_lprvt_u_sram_lprvt.SPEEDOUT_NMOS -group Group_LOADER_clkP_virt 
##netlist clock u_LEG_CORNER_A.u_LEG_PMB.u_C32_PM_CONTROL.gen_sram_lprvt_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_sram_lprvt_u_sram_lprvt.SPEEDOUT_PMOS -group Group_LOADER_clkP_virt 
##netlist clock u_LEG_CORNER_A.u_LEG_PMB.u_C32_PM_CONTROL.gen_sram_lprvt_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_sram_lprvt_u_sram_lprvt.LEAK_OUT -group Group_LOADER_clkP_virt 
##netlist clock u_LEG_CORNER_B.u_LEG_PMB.u_C32_PM_CONTROL.gen_logic_lprvt_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_u_logic_lprvt.SPEEDOUT_NMOS -group Group_LOADER_clkP_virt 
##netlist clock u_LEG_CORNER_B.u_LEG_PMB.u_C32_PM_CONTROL.gen_logic_lprvt_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_u_logic_lprvt.SPEEDOUT_PMOS -group Group_LOADER_clkP_virt 
##netlist clock u_LEG_CORNER_B.u_LEG_PMB.u_C32_PM_CONTROL.gen_logic_lprvt_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_u_logic_lprvt.LEAK_OUT -group Group_LOADER_clkP_virt 
##netlist clock u_LEG_CORNER_B.u_LEG_PMB.u_C32_PM_CONTROL.gen_logic_lplvt_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_u_logic_lplvt.SPEEDOUT_NMOS -group Group_LOADER_clkP_virt 
##netlist clock u_LEG_CORNER_B.u_LEG_PMB.u_C32_PM_CONTROL.gen_logic_lplvt_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_u_logic_lplvt.SPEEDOUT_PMOS -group Group_LOADER_clkP_virt 
##netlist clock u_LEG_CORNER_B.u_LEG_PMB.u_C32_PM_CONTROL.gen_logic_lplvt_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_u_logic_lplvt.LEAK_OUT -group Group_LOADER_clkP_virt 
##netlist clock u_LEG_CORNER_B.u_LEG_PMB.u_C32_PM_CONTROL.gen_logic_lprvt_p4_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_p4_u_logic_lprvt_p4.SPEEDOUT_NMOS -group Group_LOADER_clkP_virt 
##netlist clock u_LEG_CORNER_B.u_LEG_PMB.u_C32_PM_CONTROL.gen_logic_lprvt_p4_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_p4_u_logic_lprvt_p4.SPEEDOUT_PMOS -group Group_LOADER_clkP_virt 
##netlist clock u_LEG_CORNER_B.u_LEG_PMB.u_C32_PM_CONTROL.gen_logic_lprvt_p4_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_p4_u_logic_lprvt_p4.LEAK_OUT -group Group_LOADER_clkP_virt 
##netlist clock u_LEG_CORNER_B.u_LEG_PMB.u_C32_PM_CONTROL.gen_logic_lplvt_p4_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_p4_u_logic_lplvt_p4.SPEEDOUT_NMOS -group Group_LOADER_clkP_virt 
##netlist clock u_LEG_CORNER_B.u_LEG_PMB.u_C32_PM_CONTROL.gen_logic_lplvt_p4_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_p4_u_logic_lplvt_p4.SPEEDOUT_PMOS -group Group_LOADER_clkP_virt 
##netlist clock u_LEG_CORNER_B.u_LEG_PMB.u_C32_PM_CONTROL.gen_logic_lplvt_p4_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_p4_u_logic_lplvt_p4.LEAK_OUT -group Group_LOADER_clkP_virt 
##netlist clock u_LEG_CORNER_B.u_LEG_PMB.u_C32_PM_CONTROL.gen_logic_lprvt_p10_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_p10_u_logic_lprvt_p10.SPEEDOUT_NMOS -group Group_LOADER_clkP_virt 
##netlist clock u_LEG_CORNER_B.u_LEG_PMB.u_C32_PM_CONTROL.gen_logic_lprvt_p10_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_p10_u_logic_lprvt_p10.SPEEDOUT_PMOS -group Group_LOADER_clkP_virt 
##netlist clock u_LEG_CORNER_B.u_LEG_PMB.u_C32_PM_CONTROL.gen_logic_lprvt_p10_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_p10_u_logic_lprvt_p10.LEAK_OUT -group Group_LOADER_clkP_virt 
##netlist clock u_LEG_CORNER_B.u_LEG_PMB.u_C32_PM_CONTROL.gen_logic_lplvt_p10_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_p10_u_logic_lplvt_p10.SPEEDOUT_NMOS -group Group_LOADER_clkP_virt 
##netlist clock u_LEG_CORNER_B.u_LEG_PMB.u_C32_PM_CONTROL.gen_logic_lplvt_p10_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_p10_u_logic_lplvt_p10.SPEEDOUT_PMOS -group Group_LOADER_clkP_virt 
##netlist clock u_LEG_CORNER_B.u_LEG_PMB.u_C32_PM_CONTROL.gen_logic_lplvt_p10_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_p10_u_logic_lplvt_p10.LEAK_OUT -group Group_LOADER_clkP_virt 
##netlist clock u_LEG_CORNER_B.u_LEG_PMB.u_C32_PM_CONTROL.gen_sram_lprvt_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_sram_lprvt_u_sram_lprvt.SPEEDOUT_NMOS -group Group_LOADER_clkP_virt 
##netlist clock u_LEG_CORNER_B.u_LEG_PMB.u_C32_PM_CONTROL.gen_sram_lprvt_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_sram_lprvt_u_sram_lprvt.SPEEDOUT_PMOS -group Group_LOADER_clkP_virt 
##netlist clock u_LEG_CORNER_B.u_LEG_PMB.u_C32_PM_CONTROL.gen_sram_lprvt_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_sram_lprvt_u_sram_lprvt.LEAK_OUT -group Group_LOADER_clkP_virt 

#netlist clock u_vclk_gate_u_CKGATE.Q -group Group_LOADER_clkP_virt 
#netlist clock u_VW.u_CG_400B_u_CKGATE.Q -group Group_LOADER_clkP_virt 

### derived clocks
#netlist clock u_LEG_CORNER_B.u_LEG_PMB.u_CLK_MUX_2_u_CKMUX2.D0 -group Group_LOADER_clkP_virt 
#netlist clock u_LEG_CORNER_B.u_LEG_PMB.u_CLK_MUX_0_u_CKMUX2.D0 -group Group_LOADER_clkP_virt 
#netlist clock u_LEG_CORNER_B.u_LEG_PMB.u_CLK_MUX_3_u_CKMUX2.D0 -group Group_LOADER_clkP_virt 
#netlist clock u_LEG_CORNER_A.u_LEG_PMB.u_CLK_MUX_2_u_CKMUX2.D0 -group Group_LOADER_clkP_virt 
#netlist clock u_LEG_CORNER_A.u_LEG_PMB.u_CLK_MUX_3_u_CKMUX2.D0 -group Group_LOADER_clkP_virt 
#netlist clock u_LEG_CORNER_A.u_LEG_PMB.u_CLK_MUX_4_u_CKMUX2.D0 -group Group_LOADER_clkP_virt 
#netlist clock u_LEG_CORNER_A.u_LEG_PMB.u_CLK_MUX_1_u_CKMUX2.D0 -group Group_LOADER_clkP_virt 
#netlist clock u_LEG_CORNER_A.u_LEG_PMB.u_CLK_MUX_0_u_CKMUX2.D0 -group Group_LOADER_clkP_virt 
#netlist clock u_LEG_CORNER_B.u_LEG_PMB.u_CLK_MUX_1_u_CKMUX2.D0 -group Group_LOADER_clkP_virt 
#netlist clock u_LEG_CORNER_B.u_LEG_PMB.u_CLK_MUX_4_u_CKMUX2.D0 -group Group_LOADER_clkP_virt 

### Fifo are kept intependent althogh the pins in the sdc is called clkcP because I can't see the clock diagram and the grouping to the other clockP
#netlist clock u_PR_FIFO_A.u_CLK.u_CKMUX2.Z -group Group_LOADER_clkP_virt 
#netlist clock u_PR_FIFO_B.u_CLK.u_CKMUX2.Z -group Group_LOADER_clkP_virt 
#netlist clock u_PR_FIFO_C.u_CLK.u_CKMUX2.Z -group Group_LOADER_clkP_virt 


