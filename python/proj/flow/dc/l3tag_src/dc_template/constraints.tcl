#general synthesize constraints tcl, by gub.
#specify below parameters, according to target library.
set_operating_conditions -max tt 
#set_operating_conditions -max {{dc_dic.constraints__tcl.set_operating_conditions}}
#set auto_wire_load_selection {{dc_dic.constraints__tcl.auto_wire_load_selection}}
set auto_wire_load_selection false
#set_wire_load_model -name {{dc_dic.constraints__tcl.set_wire_load_model}}
set_wire_load_mode {{dc_dic.constraints__tcl.set_wire_load_mode}}
#set_wire_load_mode {{set_wire_load_mode}}

#group_paths
#clock_gating_excludes

