# THIS FILE CONTAINS DIRECTIVES FOR CRYSTAL3S
# Define clocks
### directives taken from func mode
# /vols/mentor/crystal3s_dev/working_main/Damien.Pesme/IRDrop150522/src/sdc/CORNER/func/CORNER_func_clock.sdc
#

# Splitted by Mentor   on Wed Feb 12 08:17:26 CET 2014
#set_units -time ns -capacitance pF -current mA -voltage V -resistance kOhm -power mW
netlist clock u_CENTRAL_IO.core_refclk_0 -period 9.999
netlist clock u_CENTRAL_IO.core_refclk_1 -period 9.999
netlist clock u_CENTRAL_IO.core_refclk_2 -period 9.999
netlist clock u_CENTRAL_IO.core_refclk_3 -period 9.999
netlist clock u_CENTRAL_IO.core_refclk_4 -period 9.999
netlist clock u_CENTRAL_IO.core_refclk_5 -period 9.999
netlist clock u_CENTRAL_IO.core_refclk_6 -period 9.999
netlist clock u_CENTRAL_IO.core_refclk_7 -period 9.999
netlist clock u_CENTRAL_IO.core_refclk_8 -period 9.999

netlist clock u_CLOCK_center.clk1200_o .PHI -period 0.833
netlist clock u_CLOCK_top_center.clk1200_o -period 0.833
netlist clock u_CLOCK_top_left.clk1200_o -period 0.833
netlist clock u_CLOCK_top_right.clk1200_o -period 0.833
netlist clock u_CLOCK_center_right.clk1200_o -period 0.833
netlist clock u_CLOCK_center_left.clk1200_o -period 0.833
netlist clock u_CLOCK_bot_center.clk1200_o -period 0.833
netlist clock u_CLOCK_bot_left.clk1200_o -period 0.833
netlist clock u_CLOCK_bot_right.clk1200_o -period 0.833

netlist clock u_CLOCK_center.clk300_o .PHI -period 2.65
netlist clock u_CLOCK_top_center.clk300_o -period 2.65
netlist clock u_CLOCK_top_left.clk300_o -period 2.65
netlist clock u_CLOCK_top_right.clk300_o -period 2.65
netlist clock u_CLOCK_center_right.clk300_o -period 2.65
netlist clock u_CLOCK_center_left.clk300_o -period 2.65
netlist clock u_CLOCK_bot_center.clk300_o -period 2.65
netlist clock u_CLOCK_bot_left.clk300_o -period 2.65
netlist clock u_CLOCK_bot_right.clk300_o -period 2.65

netlist clock u_CLOCK_center.clk100_o .PHI -period 10
netlist clock u_CLOCK_top_center.clk100_o -period 10
netlist clock u_CLOCK_top_left.clk100_o -period  10
netlist clock u_CLOCK_top_right.clk100_o -period 10
netlist clock u_CLOCK_center_right.clk100_o -period 10
netlist clock u_CLOCK_center_left.clk100_o -period 10
netlist clock u_CLOCK_bot_center.clk100_o -period 10
netlist clock u_CLOCK_bot_left.clk100_o -period  10
netlist clock u_CLOCK_bot_right.clk100_o -period 10

##--## netlist clock clk25_virt -period 39.9984 
##--## netlist clock clk1200 -period 0.8333 
##--## netlist clock clk400 -period 2.499
##--## netlist clock clk300 -period 3.333
##--## netlist clock clk200 -period 4.9998 
##--## netlist clock clk100 -period 9.9996 
##--## netlist clock clk_edt -period 39.9984 
##--## netlist clock clkP -period 2.4999 
##--## netlist clock LOADER/clkP -period 2.4999 
##--## netlist clock CORNER/clkP -period 2.499
##--## netlist clock FUMEM/clkP -period 2.4999 
##--## netlist clock clk_shift -period 25 
##--## netlist clock clk_shift_prog -period 25 
##--## netlist clock clk_shift_bist -period 25 
##--## netlist clock clk_bist -period 39.9984 
##--## netlist clock u_TRIXS0/clkM300 -period 3.3332 
##--## netlist clock u_TRIXS1/clkM300 -period 3.3332 
##--## netlist clock u_TRIXS2/clkM300 -period 3.3332 
##--## netlist clock u_TRIXS3/clkM300 -period 3.3332 
##--## netlist clock u_TRIXS4/clkM300 -period 3.3332 
##--## netlist clock LOADER_clkP_virt -period 2.4999 
##--## netlist clock clk100_virt -period 9.9996 
##--## netlist clock clk200_virt -period 4.9998 
##--## netlist clock clk300_virt -period 3.3332 
##--## netlist clock u_CORNER0/clk100_MA_virt -period 9.9996 
##--## netlist clock u_CORNER0/clkP_virt -period 2.4999 
##--## netlist clock u_CORNER0/u_PR_FIFO_B/fifo/clkP_virt -period 2.4999 
##--## netlist clock u_CORNER1/clk100_MA_virt -period 9.9996 
##--## netlist clock u_CORNER1/clkP_virt -period 2.4999 
##--## netlist clock u_CORNER1/u_PR_FIFO_B/fifo/clkP_virt -period 2.4999 
##--## netlist clock u_CORNER2/clk100_MA_virt -period 9.9996 
##--## netlist clock u_CORNER3/clkP_virt -period 2.4999 
##--## netlist clock u_CORNER3/u_PR_FIFO_B/fifo/clkP_virt -period 2.4999 
##--## netlist clock u_CRY0/u_CORNER0/clk200_to_trace_virt -period 4.9998 
##--## netlist clock u_CRY0/u_CORNER1/clk200_to_trace_virt -period 4.9998 
##--## netlist clock u_FUMEM_0/clkP_virt -period 2.4999 
##--## netlist clock u_FUMEM_0/u_PR_FIFO/fifo/clkP_virt -period 2.4999 
##--## netlist clock u_LOADER_0/u_PR_FIFO_RI/fifo/clkP_virt -period 2.4999 
##--## netlist clock u_TRACE_0/clkP_virt -period 2.4999 
##--## netlist clock u_TRACE_0/u_PR_FIFO/fifo/clkP_virt -period 2.4999 
##--## netlist clock clk_default_virt -period 10 
##--## netlist clock clkM300_virt -period 3.3332 
##--## netlist clock u_LEG_CORNER_A/u_LEG_PMB/LR_speed_n_clk -period 4 
##--## netlist clock u_LEG_CORNER_A/u_LEG_PMB/LR_speed_p_clk -period 4 
##--## netlist clock u_LEG_CORNER_A/u_LEG_PMB/LR_leak_clk -period 4 
##--## netlist clock u_LEG_CORNER_A/u_LEG_PMB/LL_speed_n_clk -period 4 
##--## netlist clock u_LEG_CORNER_A/u_LEG_PMB/LL_speed_p_clk -period 4 
##--## netlist clock  u_LEG_CORNER_A/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lplvt_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_u_logic_lplvt/LEAK_OUT -period 4
##--## netlist clock u_LEG_CORNER_A/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lprvt_p4_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_p4_u_logic_lprvt_p4/SPEEDOUT_NMOS -period 4
##--## netlist clock u_LEG_CORNER_A/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lprvt_p4_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_p4_u_logic_lprvt_p4/SPEEDOUT_PMOS -period 4
##--## ##--## netlist clock u_LEG_CORNER_A/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lprvt_p4_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_p4_u_logic_lprvt_p4/LEAK_OUT -period 4
##--## netlist clock u_LEG_CORNER_A/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lplvt_p4_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_p4_u_logic_lplvt_p4/SPEEDOUT_NMOS -period 4
##--## netlist clock u_LEG_CORNER_A/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lplvt_p4_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_p4_u_logic_lplvt_p4/SPEEDOUT_PMOS -period 4
##--## netlist clock u_LEG_CORNER_A/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lplvt_p4_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_p4_u_logic_lplvt_p4/LEAK_OUT -period 4
##--## netlist clock u_LEG_CORNER_A/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lprvt_p10_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_p10_u_logic_lprvt_p10/SPEEDOUT_NMOS -period 4
##--## netlist clock u_LEG_CORNER_A/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lprvt_p10_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_p10_u_logic_lprvt_p10/SPEEDOUT_PMOS -period 4
##--## netlist clock u_LEG_CORNER_A/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lprvt_p10_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_p10_u_logic_lprvt_p10/LEAK_OUT -period 4
##--## netlist clock u_LEG_CORNER_A/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lplvt_p10_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_p10_u_logic_lplvt_p10/SPEEDOUT_NMOS -period 4
##--## netlist clock u_LEG_CORNER_A/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lplvt_p10_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_p10_u_logic_lplvt_p10/SPEEDOUT_PMOS -period 4
##--## netlist clock u_LEG_CORNER_A/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lplvt_p10_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_p10_u_logic_lplvt_p10/LEAK_OUT -period 4
##--## netlist clock u_LEG_CORNER_A/u_LEG_PMB/u_C32_PM_CONTROL/gen_sram_lprvt_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_sram_lprvt_u_sram_lprvt/SPEEDOUT_NMOS -period 4
##--## netlist clock u_LEG_CORNER_A/u_LEG_PMB/u_C32_PM_CONTROL/gen_sram_lprvt_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_sram_lprvt_u_sram_lprvt/SPEEDOUT_PMOS -period 4
##--## netlist clock u_LEG_CORNER_A/u_LEG_PMB/u_C32_PM_CONTROL/gen_sram_lprvt_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_sram_lprvt_u_sram_lprvt/LEAK_OUT -period 4
##--## netlist clock u_LEG_CORNER_B/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lprvt_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_u_logic_lprvt/SPEEDOUT_NMOS -period 4
##--## netlist clock u_LEG_CORNER_B/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lprvt_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_u_logic_lprvt/SPEEDOUT_PMOS -period 4
##--## netlist clock u_LEG_CORNER_B/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lprvt_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_u_logic_lprvt/LEAK_OUT -period 4
##--## netlist clock u_LEG_CORNER_B/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lplvt_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_u_logic_lplvt/SPEEDOUT_NMOS -period 4
##--## netlist clock u_LEG_CORNER_B/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lplvt_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_u_logic_lplvt/SPEEDOUT_PMOS -period 4
##--## netlist clock u_LEG_CORNER_B/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lplvt_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_u_logic_lplvt/LEAK_OUT -period 4
##--## netlist clock u_LEG_CORNER_B/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lprvt_p4_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_p4_u_logic_lprvt_p4/SPEEDOUT_NMOS -period 4
##--## netlist clock u_LEG_CORNER_B/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lprvt_p4_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_p4_u_logic_lprvt_p4/SPEEDOUT_PMOS -period 4
##--## netlist clock u_LEG_CORNER_B/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lprvt_p4_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_p4_u_logic_lprvt_p4/LEAK_OUT -period 4
##--## netlist clock u_LEG_CORNER_B/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lplvt_p4_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_p4_u_logic_lplvt_p4/SPEEDOUT_NMOS -period 4
##--## netlist clock u_LEG_CORNER_B/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lplvt_p4_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_p4_u_logic_lplvt_p4/SPEEDOUT_PMOS -period 4
##--## netlist clock u_LEG_CORNER_B/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lplvt_p4_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_p4_u_logic_lplvt_p4/LEAK_OUT -period 4
##--## netlist clock u_LEG_CORNER_B/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lprvt_p10_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_p10_u_logic_lprvt_p10/SPEEDOUT_NMOS -period 4
##--## netlist clock u_LEG_CORNER_B/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lprvt_p10_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_p10_u_logic_lprvt_p10/SPEEDOUT_PMOS -period 4
##--## netlist clock u_LEG_CORNER_B/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lprvt_p10_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lprvt_p10_u_logic_lprvt_p10/LEAK_OUT -period 4
##--## netlist clock u_LEG_CORNER_B/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lplvt_p10_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_p10_u_logic_lplvt_p10/SPEEDOUT_NMOS -period 4
##--## netlist clock u_LEG_CORNER_B/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lplvt_p10_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_p10_u_logic_lplvt_p10/SPEEDOUT_PMOS -period 4
##--## netlist clock u_LEG_CORNER_B/u_LEG_PMB/u_C32_PM_CONTROL/gen_logic_lplvt_p10_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_logic_lplvt_p10_u_logic_lplvt_p10/LEAK_OUT -period 4
##--## netlist clock u_LEG_CORNER_B/u_LEG_PMB/u_C32_PM_CONTROL/gen_sram_lprvt_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_sram_lprvt_u_sram_lprvt/SPEEDOUT_NMOS -period 4
##--## netlist clock u_LEG_CORNER_B/u_LEG_PMB/u_C32_PM_CONTROL/gen_sram_lprvt_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_sram_lprvt_u_sram_lprvt/SPEEDOUT_PMOS -period 4
##--## netlist clock u_LEG_CORNER_B/u_LEG_PMB/u_C32_PM_CONTROL/gen_sram_lprvt_pmb_wrapper_1_u_C32_PM_CONTROL_pmb_wrapper_gen_pmb_sram_lprvt_u_sram_lprvt/LEAK_OUT -period 4
##--## 
##--## ## generated clocks - should they define as clocks for CDC - ### leave if for now
##--## ##netlist clock u_LEG_CORNER_B/u_LEG_PMB/clkP_div_8 -source [get_pins {u_LEG_CORNER_B/u_LEG_PMB/u_CLK_div_0_u_REGN/CP}]  -divide_by 8  -add -master_clock [get_clocks {clkP}] [get_pins {u_LEG_CORNER_B/u_LEG_PMB/u_CLK_MUX_2_u_CKMUX2/D0}] 
##--## ##netlist clock u_LEG_CORNER_B/u_LEG_PMB/clkP_div_2 -source [get_pins {u_LEG_CORNER_B/u_LEG_PMB/u_CLK_div_0_u_REGN/CP}]  -divide_by 2  -add -master_clock [get_clocks {clkP}] [get_pins {u_LEG_CORNER_B/u_LEG_PMB/u_CLK_MUX_0_u_CKMUX2/D0}] 
##--## ##netlist clock u_LEG_CORNER_B/u_LEG_PMB/clkP_div_16 -source [get_pins {u_LEG_CORNER_B/u_LEG_PMB/u_CLK_div_0_u_REGN/CP}]  -divide_by 16  -add -master_clock [get_clocks {clkP}] [get_pins {u_LEG_CORNER_B/u_LEG_PMB/u_CLK_MUX_3_u_CKMUX2/D0}] 
##netlist clock u_LEG_CORNER_A/u_LEG_PMB/clkP_div_8 -source [get_pins {u_LEG_CORNER_A/u_LEG_PMB/u_CLK_div_0_u_REGN/CP}]  -divide_by 8  -add -master_clock [get_clocks {clkP}] [get_pins {u_LEG_CORNER_A/u_LEG_PMB/u_CLK_MUX_2_u_CKMUX2/D0}] 
##netlist clock clk100_MA -source [get_pins {u_vclk_gate_u_CKGATE/CP}] -edges { 1 2 3}  -add -master_clock [get_clocks {clk100}] [get_pins {u_vclk_gate_u_CKGATE/Q}] 
##netlist clock u_VW/clk400_bist -source [get_pins {u_VW/u_CG_400B_u_CKGATE/CP}] -edges { 1 2 3}  -add -master_clock [get_clocks {clk400}] [get_pins {u_VW/u_CG_400B_u_CKGATE/Q}] 
##netlist clock u_LEG_CORNER_A/u_LEG_PMB/clkP_div_16 -source [get_pins {u_LEG_CORNER_A/u_LEG_PMB/u_CLK_div_0_u_REGN/CP}]  -divide_by 16  -add -master_clock [get_clocks {clkP}] [get_pins {u_LEG_CORNER_A/u_LEG_PMB/u_CLK_MUX_3_u_CKMUX2/D0}] 
##netlist clock u_LEG_CORNER_A/u_LEG_PMB/clkP_div_32 -source [get_pins {u_LEG_CORNER_A/u_LEG_PMB/u_CLK_div_0_u_REGN/CP}]  -divide_by 32  -add -master_clock [get_clocks {clkP}] [get_pins {u_LEG_CORNER_A/u_LEG_PMB/u_CLK_MUX_4_u_CKMUX2/D0}] 
##netlist clock u_LEG_CORNER_A/u_LEG_PMB/clkP_div_4 -source [get_pins {u_LEG_CORNER_A/u_LEG_PMB/u_CLK_div_0_u_REGN/CP}]  -divide_by 4  -add -master_clock [get_clocks {clkP}] [get_pins {u_LEG_CORNER_A/u_LEG_PMB/u_CLK_MUX_1_u_CKMUX2/D0}] 
##netlist clock u_LEG_CORNER_A/u_LEG_PMB/clkP_div_2 -source [get_pins {u_LEG_CORNER_A/u_LEG_PMB/u_CLK_div_0_u_REGN/CP}]  -divide_by 2  -add -master_clock [get_clocks {clkP}] [get_pins {u_LEG_CORNER_A/u_LEG_PMB/u_CLK_MUX_0_u_CKMUX2/D0}] 
##netlist clock u_LEG_CORNER_B/u_LEG_PMB/clkP_div_4 -source [get_pins {u_LEG_CORNER_B/u_LEG_PMB/u_CLK_div_0_u_REGN/CP}]  -divide_by 4  -add -master_clock [get_clocks {clkP}] [get_pins {u_LEG_CORNER_B/u_LEG_PMB/u_CLK_MUX_1_u_CKMUX2/D0}] 
##netlist clock clk200_to_trace -source [get_pins {u_CLOCK_200_u_CKI/A}] -edges { 1 2 3} -invert  -add -master_clock [get_clocks {clk200}] [get_pins {u_CLOCK_200_u_CKI/Z}] 
##netlist clock u_LEG_CORNER_B/u_LEG_PMB/clkP_div_32 -source [get_pins {u_LEG_CORNER_B/u_LEG_PMB/u_CLK_div_0_u_REGN/CP}]  -divide_by 32  -add -master_clock [get_clocks {clkP}] [get_pins {u_LEG_CORNER_B/u_LEG_PMB/u_CLK_MUX_4_u_CKMUX2/D0}] 
##
### I don't know how to treat clocks that are define only on certain edges and define only on two pins so I leave it for now
##create_generated_clock [get_pins u_PR_FIFO_A/u_CLK/u_CKMUX2/Z] -name u_PR_FIFO_A/fifo/clkP -source [get_pins u_PR_FIFO_A/u_CLK/u_CKMUX2/D0] -edges {1 2 3}
##create_generated_clock [get_pins u_PR_FIFO_B/u_CLK/u_CKMUX2/Z] -name u_PR_FIFO_B/fifo/clkP -source [get_pins u_PR_FIFO_B/u_CLK/u_CKMUX2/D0] -edges {1 2 3}
##create_generated_clock [get_pins u_PR_FIFO_C/u_CLK/u_CKMUX2/Z] -name u_PR_FIFO_C/fifo/clkP -source [get_pins u_PR_FIFO_C/u_CLK/u_CKMUX2/D0] -edges {1 2 3}
##

## original definition
#netlist clock cpu_clk_in -period 50
#netlist clock core_clk_in -period 60 
#netlist clock mac_clk_in -period 50 

# Define constants
netlist constant scan_mode 1'b0

# Add CDC constraints
cdc preference reconvergence -depth 1 -divergence_depth 1 
cdc preference -fifo_scheme -handshake_scheme
