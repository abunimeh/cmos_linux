#################################################################################
# Create Power Switch Array and Ring                                            #
#################################################################################

#report_power_domain -all

##LAB: complete to create map_power_switch for power switches in each power domain
############### map power switch for LEON3_p0 ################
map_power_switch sw1 -domain PD_ADD -lib_cell HEADER2X4LP18T 
############### map power switch for LEON3_p1 ################
#map_power_switch leon3_p1_sw -domain LEON3_p1 -lib_cell HEAD2X16_HVT
############### map power switch for LEON3_p2 ################
#map_power_switch leon3_p2_sw -domain LEON3_p2 -lib_cell HEAD2X16_HVT
############### map power switch for LEON3_p3 ################
#map_power_switch leon3_p3_sw -domain LEON3_p3 -lib_cell HEAD2X16_HVT
############### map power switch for LEON3_misc ################
#map_power_switch leon3_misc_sw -domain LEON3_misc -lib_cell HEAD2X16_HVT

############### create power switch array for LEON3_p0 ################
create_power_switch_array -voltage_area PD_ADD \
                          -lib_cell sw1 \
                          -design I_ADD \
                          -bounding_box {30 47.72 52.415 88.040} \
                          -x_incr 0 -y_incr 0 \
                          -snap_to_row_and_tile \
                          -prefix sw1_header

############### power switch synthesis will be run for u0_2/pd_switchable/LEON3_p2 in PNS later ################
############### power switch synthesis will be run for u0_3/pd_switchable/LEON3_p3 in PNS later ################

############### create power switch ring for LEON3_misc ################
#create_power_switch_ring -area_obj PD_ADD \
                         -switch_lib_cell sw1 \
                         -start_point {11.135 8.440} \
                         -prefix sw1_header

connect_power_switch \
        -source I_PWR_CTRL/sw_ctrl \
        -port_name EPIN \
        -mode daisy \
        -verbose \
        -voltage_area PD_ADD \
        -direction vertical

