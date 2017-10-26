remove_placement -object_type standard_cell
#source -e -v ../../DATA_SAED/ICC_DATA/fp/insert_mv_filler_cells.tcl

################### Avoid preroute changing layer ###############################


################### preroute AO power for iso1 ###############################

#
################### preroute all shutdown power for VDD1_ADD ###############################

################### preroute shutdown power and AO power for top ###############################
set_parameter  -name  layerSwitching -value 1

preroute_standard_cells  -nets {VDD GND} -voltage_area_filter_mode select -voltage_area_filter DEFAULT_VA -fill_empty_rows

################### preroute secondary supplies ###############################
remove_stdcell_filler -stdcell
preroute_standard_cells -mode net  -nets  {VDD}  -connect horizontal  -remove_floating_pieces  -route_type {Signal Route}
#save_mw_cel -as flat_dp_groute_with_filler

verify_pg_nets
#check_mv_design -verbose
