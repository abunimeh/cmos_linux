#report_power_domain -all
#report_voltage_area -all


############ block M6 for future strap for ISO AO power #######################
#create_route_guide -name iso1  -coordinate {1.005 13.005 25.995 13.505} -no_preroute_layers M6
#create_route_guide -name iso1  -coordinate {25.495 13.505 25.995 45.995} -no_preroute_layers M6

synthesize_fp_rail -synthesize_voltage_areas \
                   -voltage_area { DEFAULT_VA } \
                   -use_strap_ends_as_pads



commit_fp_rail



