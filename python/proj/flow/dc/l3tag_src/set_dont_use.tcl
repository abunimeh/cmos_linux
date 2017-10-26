set_dont_use [get_lib_cells {*/CLK*}]
set_dont_use [get_lib_cells {*/G*}]
set_dont_use [get_lib_cells {*/DLY*}]


set_clock_gating_check -setup 0.3 [current_design]

