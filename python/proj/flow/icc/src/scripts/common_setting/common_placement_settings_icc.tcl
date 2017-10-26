puts "RM-Info: Running script [info script]\n"

##########################################################################################
# Version: E-2010.12 (January 10, 2011)
# Copyright (C) 2007-2011 Synopsys, Inc. All rights reserved.
##########################################################################################

# Placement Common Session Options - set in all sessions

## Set Min/Max Routing Layers
if { $MAX_ROUTING_LAYER != ""} {set_ignored_layers -max_routing_layer $MAX_ROUTING_LAYER}
if { $MIN_ROUTING_LAYER != ""} {set_ignored_layers -min_routing_layer $MIN_ROUTING_LAYER}



## Set PNET Options to control cel placement around P/G straps 
#if {$PNET_METAL_LIST != "" || $PNET_METAL_LIST_COMPLETE != "" } {
#	remove_pnet_options

#	if {$PNET_METAL_LIST_COMPLETE != "" } {
#		set_pnet_options -complete $PNET_METAL_LIST_COMPLETE -see_object {all_types#}
#	}

#	if {$PNET_METAL_LIST != "" } {
#		set_pnet_options -partial $PNET_METAL_LIST -see_object {all_types} 
#	}
	
#	report_pnet_options
#}

#set_dont_use [get_lib_cells */CLK*]
#set_dont_use [get_lib_cells */G*]
 

## it is recommended to use the default of the tool
## in case it needs to change ( e.g. for low utlization designs), use the command below :
 # set_congestion_options -max_util 0.85

set_app_var enable_recovery_removal_arcs true

puts "RM-Info: Completed script [info script]\n"
