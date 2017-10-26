#general synthesize sdc file, by gub.
#basic parameter definitions need to config, duplicate below lines if there are two or more clocks.
#clk_freq unit is MHz
#please keep the 000 after ".", otherwise clk_period will be an integer(w/o decimal).
#clk_period unit is ns

source -echo -verbose {{dc_dic.dc__tcl.DcTcl_DIR}}/set_args.tcl


set clk_name ${clk_name}
set clk_port ${clk_port}


set clk_freq ${clk_freq}
set clk_period [expr 1000/$clk_freq]

#clock definition
create_clock -name $clk_name -period $clk_period [get_ports $clk_port]
#create_clock [get_ports clk]  -period 1 -waveform {0 0.5}

set_clock_uncertainty [expr {{dc_dic.common__sdc.set_clock_uncertainty}}*$clk_period] [get_clocks $clk_name]
set_clock_transition  [expr {{dc_dic.common__sdc.set_clock_transition}}*$clk_period] [get_clocks $clk_name]

set_input_delay  -max [expr {{dc_dic.common__sdc.set_input_delay}}*$clk_period] -clock $clk_name [all_inputs]
set_output_delay -max [expr {{dc_dic.common__sdc.set_output_delay}}*$clk_period] -clock $clk_name [all_outputs]

##specify below lib_cell name and pin, according to target library.
#set_driving_cell -lib_cell AND2X2LP18T -pin Y [all_inputs]
#set_driving_cell -lib_cell AND2X1 -pin Y [all_inputs]
set_load 0.080  [all_outputs]

#timing exceptions
#set_false_path -from [get_clocks Asynch_CLKA] -to [get_clocks Asynch_CLKB]
#set_multicycle_path -setup 4 -from -from A_reg -through U_Mult/Out -to B_reg
#set_multicycle_path -hold 3 -from -from A_reg -through U_Mult/Out -to B_reg
set_ideal_network [get_ports $clk_port]

 #set_clock_gating_check -setup 0.3 [current_design]

#temp timing exceptions sdc for timing trial
#source /workspace/cpu1/wuwj/houduan/syn/common_syn_flow_nofanout/source/fdzx_1
#source /workspace/cpu1/wuwj/houduan/syn/common_syn_flow_nofanout/source/fdzx_2
