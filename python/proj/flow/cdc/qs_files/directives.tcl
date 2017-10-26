# THIS FILE CONTAINS DIRECTIVES FOR CRYSTAL3S
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
# Splitted by Mentor   on Wed Feb 12 08:17:26 CET 2014
#set_units -time ns -capacitance pF -current mA -voltage V -resistance kOhm -power mW
#
#  clock from ports only
#

#virtual clocks
netlist clock  clk25_virt -virtual -period 40 -waveform  0 20 
netlist clock  LOADER_clkP_virt -virtual -period 5 -waveform  0 1.25 
netlist clock  clk100_virt -virtual -period 10 -waveform  0 5 
netlist clock  clk200_virt -virtual -period 5 -waveform  0 5 
netlist clock  clk300_virt -virtual -period 3.33 -waveform  0 1.66 
netlist clock  u_CORNER0/clk100_MA_virt -virtual -period 10 -waveform  0 5 
netlist clock  u_CORNER0/clkP_virt -virtual -period 5 -waveform  0 1.25 
netlist clock  u_CORNER0/u_PR_FIFO_B/fifo/clkP_virt -virtual -period 5 -waveform  0 1.25 
netlist clock  u_CORNER1/clk100_MA_virt -virtual -period 10 -waveform  0 5 
netlist clock  u_CORNER1/clkP_virt -virtual -period 5 -waveform  0 1.25 
netlist clock  u_CORNER1/u_PR_FIFO_B/fifo/clkP_virt -virtual -period 5 -waveform  0 1.25 
netlist clock  u_CORNER2/clk100_MA_virt -virtual -period 10 -waveform  0 5 
netlist clock  u_CORNER3/clkP_virt -virtual -period 5 -waveform  0 1.25 
netlist clock  u_CORNER3/u_PR_FIFO_B/fifo/clkP_virt -virtual -period 5 -waveform  0 1.25 
netlist clock  u_CRY0/u_CORNER0/clk200_to_trace_virt -virtual -period 5 -waveform  0 5 
netlist clock  u_CRY0/u_CORNER1/clk200_to_trace_virt -virtual -period 5 -waveform  0 5 
netlist clock  u_FUMEM_0/clkP_virt -virtual -period 5 -waveform  0 1.25 
netlist clock  u_FUMEM_0/u_PR_FIFO/fifo/clkP_virt -virtual -period 5 -waveform  0 1.25 
netlist clock  u_LOADER_0/u_PR_FIFO_RI/fifo/clkP_virt -virtual -period 5 -waveform  0 1.25 
netlist clock  u_TRACE_0/clkP_virt -virtual -period 5 -waveform  0 1.25 
netlist clock  u_TRACE_0/u_PR_FIFO/fifo/clkP_virt -virtual -period 5 -waveform  0 1.25 
netlist clock  clk_default_virt -virtual -period 10 -waveform  0 5 
netlist clock  clkM300_virt -virtual -period 3.33 -waveform  0 1.66 



netlist clock clk1200_i -period 0.83
netlist clock clk400_i -period 2.5
netlist clock clk300_i -period 3.33
netlist clock clk200_i -period 5
netlist clock clk100_i -period 10
netlist clock edt_clock -period 40
netlist clock clkP -period 2.5
netlist clock clk_a_i -period 2.5
netlist clock clk_b_i -period 2.5
netlist clock clk_c_i -period 2.5
netlist clock clk_shift -period 25 
netlist clock clk_shift_prog -period 25 
netlist clock clk_shift_bist -period 25 
netlist clock bist_clk_i -period 40
netlist clock macro_clk_0 -period 3.33 
netlist clock macro_clk_1 -period 3.33 
netlist clock macro_clk_2 -period 3.33 
netlist clock macro_clk_3 -period 3.33 
netlist clock macro_clk_4 -period 3.33 


# Splitted by Mentor   on Wed Feb 12 08:17:26 CET 2014
##netlist clock u_LEG_CORNER_A.u_LEG_PMB.u_C32_PM_CONTROL.gen_logic_lprvt_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_u_logic_lprvt.SPEEDOUT_NMOS -period 4
##netlist clock u_LEG_CORNER_A/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lprvt_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_u_logic_lprvt/SPEEDOUT_PMOS -period 4
##netlist clock u_LEG_CORNER_A/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lprvt_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_u_logic_lprvt/LEAK_OUT -period 4
##netlist clock u_LEG_CORNER_A/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lplvt_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_u_logic_lplvt/SPEEDOUT_NMOS -period 4
##netlist clock u_LEG_CORNER_A/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lplvt_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_u_logic_lplvt/SPEEDOUT_PMOS -period 4
##netlist clock u_LEG_CORNER_A/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lplvt_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_u_logic_lplvt/LEAK_OUT -period 4
##netlist clock u_LEG_CORNER_A/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lprvt_p4_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_p4_u_logic_lprvt_p4/SPEEDOUT_NMOS -period 4
##netlist clock u_LEG_CORNER_A/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lprvt_p4_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_p4_u_logic_lprvt_p4/SPEEDOUT_PMOS -period 4
##netlist clock u_LEG_CORNER_A/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lprvt_p4_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_p4_u_logic_lprvt_p4/LEAK_OUT -period 4
##netlist clock u_LEG_CORNER_A/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lplvt_p4_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_p4_u_logic_lplvt_p4/SPEEDOUT_NMOS -period 4
##netlist clock u_LEG_CORNER_A/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lplvt_p4_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_p4_u_logic_lplvt_p4/SPEEDOUT_PMOS -period 4
##netlist clock u_LEG_CORNER_A/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lplvt_p4_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_p4_u_logic_lplvt_p4/LEAK_OUT -period 4
##netlist clock u_LEG_CORNER_A/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lprvt_p10_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_p10_u_logic_lprvt_p10/SPEEDOUT_NMOS -period 4
##netlist clock u_LEG_CORNER_A/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lprvt_p10_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_p10_u_logic_lprvt_p10/SPEEDOUT_PMOS -period 4
##netlist clock u_LEG_CORNER_A/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lprvt_p10_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_p10_u_logic_lprvt_p10/LEAK_OUT -period 4
##netlist clock u_LEG_CORNER_A/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lplvt_p10_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_p10_u_logic_lplvt_p10/SPEEDOUT_NMOS -period 4
##netlist clock u_LEG_CORNER_A/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lplvt_p10_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_p10_u_logic_lplvt_p10/SPEEDOUT_PMOS -period 4
##netlist clock u_LEG_CORNER_A/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lplvt_p10_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_p10_u_logic_lplvt_p10/LEAK_OUT -period 4
##netlist clock u_LEG_CORNER_A/u_LEG_PMB/u_C32_PM_CONTROL/gen_sram_lprvt_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_sram_lprvt_u_sram_lprvt/SPEEDOUT_NMOS -period 4
##netlist clock u_LEG_CORNER_A/u_LEG_PMB/u_C32_PM_CONTROL/gen_sram_lprvt_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_sram_lprvt_u_sram_lprvt/SPEEDOUT_PMOS -period 4
##netlist clock u_LEG_CORNER_A/u_LEG_PMB/u_C32_PM_CONTROL/gen_sram_lprvt_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_sram_lprvt_u_sram_lprvt/LEAK_OUT -period 4
##netlist clock u_LEG_CORNER_B/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lprvt_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_u_logic_lprvt/SPEEDOUT_NMOS -period 4
##netlist clock u_LEG_CORNER_B/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lprvt_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_u_logic_lprvt/SPEEDOUT_PMOS -period 4
##netlist clock u_LEG_CORNER_B/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lprvt_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_u_logic_lprvt/LEAK_OUT -period 4
##netlist clock u_LEG_CORNER_B/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lplvt_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_u_logic_lplvt/SPEEDOUT_NMOS -period 4
##netlist clock u_LEG_CORNER_B/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lplvt_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_u_logic_lplvt/SPEEDOUT_PMOS -period 4
##netlist clock u_LEG_CORNER_B/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lplvt_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_u_logic_lplvt/LEAK_OUT -period 4
##netlist clock u_LEG_CORNER_B/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lprvt_p4_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_p4_u_logic_lprvt_p4/SPEEDOUT_NMOS -period 4
##netlist clock u_LEG_CORNER_B/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lprvt_p4_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_p4_u_logic_lprvt_p4/SPEEDOUT_PMOS -period 4
##netlist clock u_LEG_CORNER_B/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lprvt_p4_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_p4_u_logic_lprvt_p4/LEAK_OUT -period 4
##netlist clock u_LEG_CORNER_B/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lplvt_p4_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_p4_u_logic_lplvt_p4/SPEEDOUT_NMOS -period 4
##netlist clock u_LEG_CORNER_B/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lplvt_p4_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_p4_u_logic_lplvt_p4/SPEEDOUT_PMOS -period 4
##netlist clock u_LEG_CORNER_B/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lplvt_p4_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_p4_u_logic_lplvt_p4/LEAK_OUT -period 4
##netlist clock u_LEG_CORNER_B/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lprvt_p10_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_p10_u_logic_lprvt_p10/SPEEDOUT_NMOS -period 4
##netlist clock u_LEG_CORNER_B/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lprvt_p10_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_p10_u_logic_lprvt_p10/SPEEDOUT_PMOS -period 4
##netlist clock u_LEG_CORNER_B/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lprvt_p10_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_p10_u_logic_lprvt_p10/LEAK_OUT -period 4
##netlist clock u_LEG_CORNER_B/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lplvt_p10_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_p10_u_logic_lplvt_p10/SPEEDOUT_NMOS -period 4
##netlist clock u_LEG_CORNER_B/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lplvt_p10_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_p10_u_logic_lplvt_p10/SPEEDOUT_PMOS -period 4
##netlist clock u_LEG_CORNER_B/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lplvt_p10_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_p10_u_logic_lplvt_p10/LEAK_OUT -period 4
##netlist clock u_LEG_CORNER_B/u_LEG_PMB/u_C32_PM_CONTROL/gen_sram_lprvt_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_sram_lprvt_u_sram_lprvt/SPEEDOUT_NMOS -period 4
##netlist clock u_LEG_CORNER_B/u_LEG_PMB/u_C32_PM_CONTROL/gen_sram_lprvt_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_sram_lprvt_u_sram_lprvt/SPEEDOUT_PMOS -period 4
##netlist clock u_LEG_CORNER_B/u_LEG_PMB/u_C32_PM_CONTROL/gen_sram_lprvt_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_sram_lprvt_u_sram_lprvt/LEAK_OUT -period 4

### generated clocks from u_LEG_CORNER_B/u_LEG_PMB/u_CLK_div_0_u_REGN/CP
# assume - dirive from clockP of period 2.5
netlist clock u_LEG_CORNER_B.u_LEG_PMB.u_CLK_MUX_0_u_CKMUX2.D0 -period 2.5 -group u_LEG_CORNER_B
netlist clock u_LEG_CORNER_B.u_LEG_PMB.u_CLK_MUX_1_u_CKMUX2.D0 -period 5   -group u_LEG_CORNER_B 
netlist clock u_LEG_CORNER_B.u_LEG_PMB.u_CLK_MUX_2_u_CKMUX2.D0 -period 10  -group u_LEG_CORNER_B
netlist clock u_LEG_CORNER_B.u_LEG_PMB.u_CLK_MUX_3_u_CKMUX2.D0 -period 20  -group u_LEG_CORNER_B
netlist clock u_LEG_CORNER_B.u_LEG_PMB.u_CLK_MUX_4_u_CKMUX2.D0 -period 40  -group u_LEG_CORNER_B`


##create_generated_clock -name u_LEG_CORNER_A/u_LEG_PMB/clkP_div_8 -source [get_pins {u_LEG_CORNER_A/u_LEG_PMB/u_CLK_div_0_u_REGN/CP}]  -divide_by 8  -add -master_clock [get_clocks {clkP}] [get_pins {u_LEG_CORNER_A/u_LEG_PMB/u_CLK_MUX_2_u_CKMUX2/D0}] 
##create_generated_clock -name u_LEG_CORNER_A/u_LEG_PMB/clkP_div_16 -source [get_pins {u_LEG_CORNER_A/u_LEG_PMB/u_CLK_div_0_u_REGN/CP}]  -divide_by 16  -add -master_clock [get_clocks {clkP}] [get_pins {u_LEG_CORNER_A/u_LEG_PMB/u_CLK_MUX_3_u_CKMUX2/D0}] 
##create_generated_clock -name u_LEG_CORNER_A/u_LEG_PMB/clkP_div_32 -source [get_pins {u_LEG_CORNER_A/u_LEG_PMB/u_CLK_div_0_u_REGN/CP}]  -divide_by 32  -add -master_clock [get_clocks {clkP}] [get_pins {u_LEG_CORNER_A/u_LEG_PMB/u_CLK_MUX_4_u_CKMUX2/D0}] 
##create_generated_clock -name u_LEG_CORNER_A/u_LEG_PMB/clkP_div_4 -source [get_pins {u_LEG_CORNER_A/u_LEG_PMB/u_CLK_div_0_u_REGN/CP}]  -divide_by 4  -add -master_clock [get_clocks {clkP}] [get_pins {u_LEG_CORNER_A/u_LEG_PMB/u_CLK_MUX_1_u_CKMUX2/D0}] 
##create_generated_clock -name u_LEG_CORNER_A/u_LEG_PMB/clkP_div_2 -source [get_pins {u_LEG_CORNER_A/u_LEG_PMB/u_CLK_div_0_u_REGN/CP}]  -divide_by 2  -add -master_clock [get_clocks {clkP}] [get_pins {u_LEG_CORNER_A/u_LEG_PMB/u_CLK_MUX_0_u_CKMUX2/D0}] 
# assume - dirive from clockP of period 2.5
netlist clock u_LEG_CORNER_A.u_LEG_PMB.u_CLK_MUX_0_u_CKMUX2.D0 -period 2.5 -group u_LEG_CORNER_A
netlist clock u_LEG_CORNER_A.u_LEG_PMB.u_CLK_MUX_1_u_CKMUX2.D0 -period 5   -group u_LEG_CORNER_A
netlist clock u_LEG_CORNER_A.u_LEG_PMB.u_CLK_MUX_2_u_CKMUX2.D0 -period 10  -group u_LEG_CORNER_A
netlist clock u_LEG_CORNER_A.u_LEG_PMB.u_CLK_MUX_3_u_CKMUX2.D0 -period 20  -group u_LEG_CORNER_A
netlist clock u_LEG_CORNER_A.u_LEG_PMB.u_CLK_MUX_4_u_CKMUX2.D0 -period 40  -group u_LEG_CORNER_A

# generated clock from u_vclk_gate_u_CKGATE/CP - master clock clk100
netlist clock u_vclk_gate_u_CKGATE.Q -period  10
# generated clock from u_VW/u_CG_400B_u_CKGATE/CP - master clock clk400 (edges { 1 2 3} ???)
netlist clock u_VW.u_CG_400B_u_CKGATE.Q -period 2.5
# generated clock from u_CLOCK_200_u_CKI/A - master clock clk200  (edges { 1 2 3} ???)
netlist clock u_CLOCK_200_u_CKI.Z -period 5

## since it's clkP i assume it's period is 2.5
netlist clock u_PR_FIFO_A.u_CLK.u_CKMUX2.D0 -period 2.5
netlist clock u_PR_FIFO_B.u_CLK.u_CKMUX2.D0 -period 2.5
netlist clock u_PR_FIFO_C.u_CLK.u_CKMUX2.D0 -period 2.5


#pin omains

netlist port domain hard_resetn -clock  clk300_virt ; #unfound
netlist port domain prog_resetn -clock  clk300_virt ; #unfound
netlist port domain fast_write_mode -clock  clk300_virt ; #unfound
netlist port domain clk200_en -clock  clk300_virt ; #unfound
netlist port domain clk300_en -clock  clk300_virt ; #unfound
netlist port domain vclk_en -clock  clk300_virt ; #unfound
netlist port domain vclk_cnt_en -clock  clk300_virt ; #unfound
netlist port domain vclk_cnt_uclk_sel -clock  clk300_virt ; #unfound
netlist port domain vclk_cnt -clock  clk300_virt ; #unfound
netlist port domain vclk_div -clock  clk300_virt ; #unfound
netlist port domain usri -clock clk300_virt
netlist port domain dll_lock -clock  clk300_virt ; #unfound
netlist port domain dll_ctl_o -clock  clk300_virt ; #unfound
netlist port domain dll_ctl_min_o -clock  clk300_virt ; #unfound
netlist port domain dll_ctl_max_o -clock  clk300_virt ; #unfound
netlist port domain dll_underflow_o -clock  clk300_virt ; #unfound
netlist port domain dll_overflow_o -clock  clk300_virt ; #unfound
netlist port domain dll_sync_phase_o -clock  clk300_virt ; #unfound
netlist port domain dll_sync_lock -clock  clk300_virt ; #unfound
netlist port domain dll_bist_current_value -clock  clk300_virt ; #unfound
netlist port domain dll_bist_first_result -clock  clk300_virt ; #unfound
netlist port domain dll_bist_last_result -clock  clk300_virt ; #unfound
netlist port domain dll_bist_monotony -clock  clk300_virt ; #unfound
netlist port domain dll_bist_done -clock  clk300_virt ; #unfound
netlist port domain dll_bist_timeout -clock  clk300_virt ; #unfound
netlist port domain en1200_align_done -clock  clk300_virt ; #unfound
netlist port domain en1200_edges_status -clock  clk300_virt ; #unfound
netlist port domain snapshot_i -clock clk100_virt
netlist port domain full_trace -clock  clk300_virt ; #unfound
netlist port domain corner_id -clock  clk300_virt ; #unfound
netlist port domain uclk -clock clk100_virt
netlist port domain freeze -clock  clk300_virt ; #unfound
netlist port domain switch_mode -clock  clk300_virt ; #unfound
netlist port domain leg_macro_0_sel -clock  clk300_virt ; #unfound
netlist port domain leg_macro_1_sel -clock  clk300_virt ; #unfound
netlist port domain leg_macro_2_sel -clock  clk300_virt ; #unfound
netlist port domain tb_md_sel -clock  clk300_virt ; #unfound
netlist port domain hop_uclk_sel -clock  clk300_virt ; #unfound
netlist port domain hop_training_en -clock  clk300_virt ; #unfound
netlist port domain error_a_ri -clock  clk300_virt ; #unfound
netlist port domain error_Id_a_ri -clock  clk300_virt ; #unfound
netlist port domain error_b_ri -clock  clk300_virt ; #unfound
netlist port domain error_Id_b_ri -clock  clk300_virt ; #unfound
netlist port domain error_c_ri -clock  clk300_virt ; #unfound
netlist port domain error_Id_c_ri -clock  clk300_virt ; #unfound
netlist port domain vw_hop_a_in -clock clk300_virt
netlist port domain vw_hop_b_in -clock clk300_virt
netlist port domain vw_hop_c_in -clock clk300_virt
netlist port domain vw_hop_d_in -clock clk300_virt
netlist port domain hop_sync_a_i -clock clk300_virt
netlist port domain hop_sync_b_i -clock clk300_virt
netlist port domain macro_vw_i -clock u_CORNER0/clk100_MA_virt
netlist port domain macro_cmem_i -clock u_CORNER0/clk100_MA_virt
netlist port domain prog_master_i -clock  clk300_virt ; #unfound
netlist port domain data_a_i -clock LOADER_clkP_virt
netlist port domain dv_a_i -clock LOADER_clkP_virt
netlist port domain data_b_i -clock u_CORNER1/clkP_virt
netlist port domain dv_b_i -clock u_CORNER1/clkP_virt
netlist port domain data_c_i -clock u_FUMEM_0/clkP_virt
netlist port domain dv_c_i -clock u_FUMEM_0/clkP_virt
##netlist port domain clk_c_i -clock  clk300_virt ; #unfound
netlist port domain la_state_i -clock clk100_virt
netlist port domain faulty_cluster_i -clock  clk300_virt ; #unfound
netlist port domain trixs0_scanin -clock clkM300_virt
netlist port domain trixs1_scanin -clock clkM300_virt
netlist port domain trixs2_scanin -clock clkM300_virt
netlist port domain trixs3_scanin -clock clkM300_virt
netlist port domain trixs4_scanin -clock clkM300_virt
netlist port domain trixs0_scanin_valid -clock clkM300_virt
netlist port domain trixs1_scanin_valid -clock clkM300_virt
netlist port domain trixs2_scanin_valid -clock clkM300_virt
netlist port domain trixs3_scanin_valid -clock clkM300_virt
netlist port domain trixs4_scanin_valid -clock clkM300_virt
netlist port domain vw_trace_a_i -clock clk200_virt
netlist port domain vw_trace_valid_a_i -clock clk200_virt
netlist port domain vw_trace_domain_a_i -clock clk200_virt
netlist port domain vw_trace_shadow_a_i -clock clk200_virt
netlist port domain vw_trace_id_a_i -clock clk200_virt
netlist port domain vw_trace_rdy_a_i -clock clk200_virt
netlist port domain cmem_quarter_trace_a_i -clock clk200_virt
netlist port domain cmem_quarter_trace_valid_a_i -clock clk200_virt
netlist port domain cmem_send_a_i -clock clk200_virt
netlist port domain cmem_send_b_i -clock clk200_virt
netlist port domain slice_accu_a_i -clock clk200_virt
netlist port domain slice_accu_b_i -clock clk200_virt
netlist port domain slice_accu_c_i -clock clk200_virt
netlist port domain slice_accu_d_i -clock clk200_virt
netlist port domain xmem_send_b_i -clock u_CRY0/u_CORNER0/clk200_to_trace_virt
netlist port domain xmem_send_a_i -clock clk200_virt
netlist port domain ff_send_a_i -clock clk200_virt
netlist port domain ff_send_b_i -clock  clk300_virt ; #unfound
netlist port domain xmem_trace_a_i -clock clk200_virt
netlist port domain xmem_trace_valid_a_i -clock clk200_virt
netlist port domain ff_trace_a_i -clock clk200_virt
netlist port domain ff_trace_valid_a_i -clock clk200_virt
netlist port domain ff_trace_clear_a_i -clock clk200_virt
netlist port domain op_perfmon -clock u_CORNER0/clk100_MA_virt
netlist port domain bist_rst_n -clock  clk300_virt ; #unfound
netlist port domain bist_ctl_shift_en -clock  clk300_virt ; #unfound
netlist port domain bist_ctl_serial_i -clock clk25_virt
netlist port domain bist_ctl_mem_type_sel -clock  clk300_virt ; #unfound
netlist port domain bist_ctl_mode_sel -clock  clk300_virt ; #unfound
netlist port domain bist_ctl_mode -clock  clk300_virt ; #unfound
netlist port domain bist_ctl_sif_load_en -clock  clk300_virt ; #unfound
netlist port domain bist_ctl_sif_reg_en -clock  clk300_virt ; #unfound
netlist port domain bist_bypass -clock  clk300_virt ; #unfound
netlist port domain bist_bypass_r -clock  clk300_virt ; #unfound
netlist port domain mrepair_rst_n -clock  clk300_virt ; #unfound
netlist port domain mrepair_shift_en -clock clk25_virt
netlist port domain mrepair_serial_i -clock clk25_virt
netlist port domain rddc2fuse_a_i -clock  clk300_virt ; #unfound
netlist port domain rddc2fuse_b_i -clock  clk300_virt ; #unfound
netlist port domain lvds_rdout -clock  clk300_virt ; #unfound
netlist port domain lvds_rdrdy -clock  clk300_virt ; #unfound
netlist port domain lvds_comzc_core -clock  clk300_virt ; #unfound
netlist port domain lvds_comzcrdy -clock  clk300_virt ; #unfound
netlist port domain edt_update -clock  clk300_virt ; #unfound
netlist port domain edt_bypass -clock  clk300_virt ; #unfound
netlist port domain edt_low_power_shift_en -clock  clk300_virt ; #unfound
netlist port domain edt_channels_in -clock  clk300_virt ; #unfound
netlist port domain atpg_te -clock  clk300_virt ; #unfound
netlist port domain atpg_at_speed -clock  clk300_virt ; #unfound
netlist port domain atpg_se -clock  clk300_virt ; #unfound
netlist port domain PLL_feedback -clock  clk300_virt ; #unfound
netlist port domain clk200_o -clock  clk200_virt 
netlist port domain clk300_co_0 -clock  clk300_i ; #unfound
netlist port domain clk300_co_1 -clock  clk300_i ; #unfound
netlist port domain clk300_co_2 -clock  clk300_i ; #unfound
netlist port domain clk300_co_3 -clock  clk300_i ; #unfound
netlist port domain clk300_co_4 -clock  clk300_i ; #unfound
netlist port domain clk300_co_5 -clock  clk300_i ; #unfound
netlist port domain clk300_co_6 -clock  clk300_i ; #unfound
netlist port domain usro -clock clk300_virt
netlist port domain is_resetn -clock  clk300_virt ; #unfound
netlist port domain dll_en -clock  clk300_virt ; #unfound
netlist port domain dll_freeze_control -clock  clk300_virt ; #unfound
netlist port domain dll_force_control -clock  clk300_virt ; #unfound
netlist port domain dll_madj -clock  clk300_virt ; #unfound
netlist port domain dll_max_adj -clock  clk300_virt ; #unfound
netlist port domain dll_tracking_speed -clock  clk300_virt ; #unfound
netlist port domain dll_ctl_i -clock  clk300_virt ; #unfound
netlist port domain dll_status_freeze -clock  clk300_virt ; #unfound
netlist port domain dll_status_reset -clock  clk300_virt ; #unfound
netlist port domain dll_lock_level -clock  clk300_virt ; #unfound
netlist port domain dll_sync_manual -clock  clk300_virt ; #unfound
netlist port domain dll_sync_phase_i -clock  clk300_virt ; #unfound
netlist port domain dll_sync_lock_resetn -clock  clk300_virt ; #unfound
netlist port domain dll_sync_lock_level -clock  clk300_virt ; #unfound
netlist port domain dll_bist_enable -clock  clk300_virt ; #unfound
netlist port domain dll_bist_start -clock  clk300_virt ; #unfound
netlist port domain dll_bist_start_value -clock  clk300_virt ; #unfound
netlist port domain dll_bist_end_value -clock  clk300_virt ; #unfound
netlist port domain dll_bist_constant_value -clock  clk300_virt ; #unfound
netlist port domain dll_bist_DLL_Id -clock  clk300_virt ; #unfound
netlist port domain tx_loopback_en -clock  clk300_virt ; #unfound
netlist port domain tx_speed -clock  clk300_virt ; #unfound
netlist port domain rx_speed -clock  clk300_virt ; #unfound
netlist port domain en1200_resetn -clock  clk300_virt ; #unfound
netlist port domain en1200_timer_value -clock  clk300_virt ; #unfound
netlist port domain en1200_align_start -clock  clk300_virt ; #unfound
netlist port domain tx_IO_enable -clock  clk300_virt ; #unfound
netlist port domain tx_DE -clock  clk300_virt ; #unfound
netlist port domain tx_gain -clock  clk300_virt ; #unfound
netlist port domain rx_IO_enable -clock  clk300_virt ; #unfound
netlist port domain rx_PE -clock  clk300_virt ; #unfound
netlist port domain rx_hyst -clock  clk300_virt ; #unfound
netlist port domain leg_macro_a_o -clock u_CORNER0/clk100_MA_virt
netlist port domain leg_xmem_rd_a_o -clock u_CORNER0/clk100_MA_virt
netlist port domain leg_xmem_rd_b_o -clock u_CORNER0/clk100_MA_virt
netlist port domain leg_xmem_wr_a_o -clock u_CORNER0/clk100_MA_virt
netlist port domain leg_xmem_wr_b_o -clock u_CORNER0/clk100_MA_virt
netlist port domain scan_capture_a -clock u_CORNER0/clk100_MA_virt
netlist port domain scan_enable_a -clock clk300_virt
netlist port domain scan_enable_b -clock clk300_virt
netlist port domain error_ro -clock  clk300_virt ; #unfound
netlist port domain error_Id_ro -clock  clk300_virt ; #unfound
netlist port domain vw_hop_a_out -clock clk300_virt
netlist port domain vw_hop_b_out -clock clk300_virt
netlist port domain vw_hop_c_out -clock clk300_virt
netlist port domain vw_hop_d_out -clock clk300_virt
netlist port domain sync_a_o -clock clk300_virt
netlist port domain sync_b_o -clock clk300_virt
netlist port domain vw_macro_o -clock u_CORNER0/clk100_MA_virt
netlist port domain cmem_macro_o -clock u_CORNER0/clk100_MA_virt
netlist port domain data_a_o -clock u_LOADER_0/u_PR_FIFO_RI/fifo/clkP_virt
netlist port domain dv_a_o -clock u_LOADER_0/u_PR_FIFO_RI/fifo/clkP_virt
netlist port domain clk_a_o -clock  clk_a_i 
netlist port domain data_b_o -clock u_CORNER1/u_PR_FIFO_B/fifo/clkP_virt
netlist port domain dv_b_o -clock u_CORNER1/u_PR_FIFO_B/fifo/clkP_virt
netlist port domain clk_b_o -clock  clk_b_i ; #unfound
netlist port domain data_c_o -clock u_FUMEM_0/u_PR_FIFO/fifo/clkP_virt
netlist port domain dv_c_o -clock u_FUMEM_0/u_PR_FIFO/fifo/clkP_virt
##netlist port domain clk_c_o -clock clk_c_i 
netlist port domain vw_trace_rdy_a_o -clock clk200_virt
netlist port domain vw_trace_b_o -clock u_CRY0/u_CORNER0/clk200_to_trace_virt
netlist port domain vw_trace_valid_b_o -clock u_CRY0/u_CORNER0/clk200_to_trace_virt
netlist port domain vw_trace_domain_b_o -clock u_CRY0/u_CORNER0/clk200_to_trace_virt
netlist port domain vw_trace_shadow_b_o -clock u_CRY0/u_CORNER0/clk200_to_trace_virt
netlist port domain vw_trace_id_b_o -clock u_CRY0/u_CORNER0/clk200_to_trace_virt
netlist port domain vw_trace_a_o -clock clk200_virt
netlist port domain vw_trace_valid_a_o -clock clk200_virt
netlist port domain vw_trace_domain_a_o -clock clk200_virt
netlist port domain vw_trace_shadow_a_o -clock clk200_virt
netlist port domain vw_trace_id_a_o -clock clk200_virt
netlist port domain cmem_quarter_trace_a_o -clock clk200_virt
netlist port domain cmem_quarter_trace_b_o -clock u_CRY0/u_CORNER0/clk200_to_trace_virt
netlist port domain cmem_quarter_trace_valid_a_o -clock clk200_virt
netlist port domain cmem_quarter_trace_valid_b_o -clock u_CRY0/u_CORNER0/clk200_to_trace_virt
netlist port domain cmem_send_a_o -clock clk200_virt
netlist port domain slice_accu_b_o -clock clk200_virt
netlist port domain slice_accu_a_o -clock clk200_virt
netlist port domain slice_accu_c_o -clock clk200_virt
netlist port domain slice_accu_d_o -clock clk200_virt
netlist port domain xmem_send_a_o -clock clk200_virt
netlist port domain ff_send_a_o -clock clk200_virt
netlist port domain xmem_trace_a_o -clock clk200_virt
netlist port domain xmem_trace_b_o -clock u_CRY0/u_CORNER0/clk200_to_trace_virt
netlist port domain xmem_trace_valid_a_o -clock clk200_virt
netlist port domain xmem_trace_valid_b_o -clock u_CRY0/u_CORNER0/clk200_to_trace_virt
netlist port domain ff_trace_a_o -clock clk200_virt
netlist port domain ff_trace_b_o -clock u_CRY0/u_CORNER0/clk200_to_trace_virt
netlist port domain ff_trace_valid_a_o -clock clk200_virt
netlist port domain ff_trace_valid_b_o -clock u_CRY0/u_CORNER0/clk200_to_trace_virt
netlist port domain ff_trace_clear_a_o -clock clk200_virt
netlist port domain ff_trace_clear_b_o -clock  clk300_virt ; #unfound
netlist port domain ip_perfmon -clock u_CORNER0/clk100_MA_virt
##netlist port domain vclk_a_o -clock  clk300_virt ; #unfound
##netlist port domain clk300_a0_o -clock  clk300_virt ; #unfound
##netlist port domain clk300_a1_o -clock  clk300_virt ; #unfound
##netlist port domain clk300_b0_o -clock  clk300_virt ; #unfound
##netlist port domain clk300_b1_o -clock  clk300_virt ; #unfound
##netlist port domain clk300_b2_o -clock  clk300_virt ; #unfound
netlist port domain bist_ctl_serial_o -clock clk25_virt
netlist port domain bist_ctl_bend -clock clk25_virt
netlist port domain bist_ctl_global_bbad -clock clk25_virt
netlist port domain bist_ctl_global_repairable -clock clk25_virt
netlist port domain mrepair_serial_o -clock clk25_virt
netlist port domain rddc2fuse_d_o -clock  clk300_virt ; #unfound
netlist port domain rddc2fuse_b_o -clock  clk300_virt ; #unfound
netlist port domain lvds_enableb -clock  clk300_virt ; #unfound
netlist port domain lvds_updaterd -clock  clk300_virt ; #unfound
netlist port domain lvds_updatezc -clock  clk300_virt ; #unfound
netlist port domain lvds_clksel -clock  clk300_virt ; #unfound
netlist port domain lvds_enbcomzcin -clock  clk300_virt ; #unfound
netlist port domain lvds_comzcin -clock  clk300_virt ; #unfound
netlist port domain lvds_avg_cycle -clock  clk300_virt ; #unfound
netlist port domain edt_channels_out -clock  clk300_virt ; #unfound
#
# Define constants

# Add CDC constraints
cdc preference reconvergence -depth 1 -divergence_depth 1 
cdc preference -fifo_scheme -handshake_scheme

#read exception sdc
sdc load data/CORNER_func_except.sdc
