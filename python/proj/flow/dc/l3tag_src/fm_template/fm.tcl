
set design_name {{DESIGN_NAME}}

set hdlin_dwroot "/tools/synopsys/syn/syn_K-2015.06"

set_svf {{set_svf}}

set ADDITIONAL_SEARCH_PATH "{{ADDITIONAL_SEARCH_PATH}}"
set_app_var search_path ". ${ADDITIONAL_SEARCH_PATH} $search_path"

read_db { 
{{read_db}}
}

set_mismatch_message_filter -warn FMR_ELAB-117

#--------------------------------------------------------------------------------------
# FM variable
#--------------------------------------------------------------------------------------
set sh_new_variable_message                       "{{sh_new_variable_message}}"         ; # default = "true"
set hdlin_auto_top                                "{{hdlin_auto_top}}"         ; # default = "false"
set hdlin_unresolved_modules                      "{{hdlin_unresolved_modules}}"     ; # default = "error"
set verification_failing_point_limit              {{verification_failing_point_limit}}             ; # default = 20
set verification_assume_reg_init                  "{{verification_assume_reg_init}}"          ; # default = "Auto"
set verification_blackbox_match_mode              "{{verification_blackbox_match_mode}}"      ; # default = "Any"
set hdlin_verilog_wired_net_interpretation        "{{hdlin_verilog_wired_net_interpretation}}"
set verification_clock_gate_hold_mode             "{{verification_clock_gate_hold_mode}}"
set verification_set_undriven_signals             "{{verification_set_undriven_signals}}"

#--------------------------------------------------------------------------------------
# read design
#--------------------------------------------------------------------------------------
{%-if ref_netlist_flag=='True' %} 
read_verilog -netlist -r {
{{ref_filelist}}
}
{%-else%}
read_verilog -r {
{{ref_filelist}}
}
{%-endif%}
set_top ${design_name}

{%-if imp_netlist_flag=='True'%} 
read_verilog -netlist -i {
{{imp_filelist}}
} 
{%-else%}
read_verilog -i {
{{imp_filelist}}
}
{%-endif%}
set_top ${design_name}

#--------------------------------------------------------------------------------------
# mode setting
#--------------------------------------------------------------------------------------
{{mode_setting}}
#set_constant i:/WORK/chip/test_mode_0_ {{test_mode_0_}} -type port
#set_constant r:/WORK/chip/test_mode_0_ {{test_mode_0_}} -type port
#set_constant i:/WORK/chip/test_mode_1_ {{test_mode_1_}} -type port
#set_constant r:/WORK/chip/test_mode_1_ {{test_mode_1_}} -type port
#set_constant i:/WORK/chip/test_mode_2_ {{test_mode_2_}} -type port
#set_constant r:/WORK/chip/test_mode_2_ {{test_mode_2_}} -type port
#set_constant i:/WORK/chip/scan_en {{scan_en}} -type port
#set_constant r:/WORK/chip/scan_en {{scan_en}} -type port
#set_constant i:/WORK/chip/serial_rx_ready 1 -type port
#set_constant r:/WORK/chip/serial_rx_ready 1 -type port
#set_constant i:/WORK/chip/tms_pad_i 1 -type port
#set_constant r:/WORK/chip/tms_pad_i 1 -type port
#set_constant i:/WORK/chip/trst_pad_i 0 -type port
#set_constant r:/WORK/chip/trst_pad_i 0 -type port
#--------------------------------------------------------------------------------------
# match
#--------------------------------------------------------------------------------------

match

report_unmatched_points > {{fm_time_dir}}/report_unmatched_points.rpt
report_matched_points   > {{fm_time_dir}}/report_matched_points.rpt

set result [ verify r:/WORK/${design_name} i:/WORK/${design_name} ]

report_failing > {{fm_time_dir}}/report_failing.rpt
report_passing > {{fm_time_dir}}/report_passing.rpt
report_aborted > {{fm_time_dir}}/report_aborted.rpt
printvar       > {{fm_time_dir}}/printvar.log

exec touch {{fm_time_dir}}/early_complete
if { $result == 0 } {
  exec touch {{fm_time_dir}}/failed
  save_session {{fm_time_dir}}/fail.session -replace
  start_gui
} else {
  exec touch {{fm_time_dir}}/pass
}

exit

