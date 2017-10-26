#################################################################################
# Create bounds for AO ISO in shutdown area					#
#################################################################################

create_bounds -name iso1 \
              -type hard \
              -exclusive \
              -coordinate {{63.245 47.685} {68.230 86.915}} \
              -cycle_color \
           [get_cells {snps_PD_ADD__iso1_snps_add_out*}]             
#MM change the region from 1008.68 to 1005.68 to get power on the top row empty

# we still need an iso region which has AO power to hold the level shifters 
# needed on  power switch control
#
# his will be added in the leon3mp.pns.tcl script 
#create_bounds -name p2_iso_region \
#              -type hard \
#              -exclusive \
#              -coordinate {{4632.100 2084.800} {5728.330 2096.320} \
#                           {4632.100 2096.320} {4643.620 2787.520} \
#                           {3151.665 2787.520} {4643.620 2799.040} \
#                           {3151.665 2799.040} {3163.185 3740.800}} \
#              -cycle_color \
#              [get_cells {u0_2/pd_switchable/iso_UPF_LS}]
	      
#create_bounds -name p3_iso_region \
              -type hard \
              -exclusive \
              -coordinate {{4632.100 1701.760} {5728.330 1713.280} \
                           {4632.100 1004.800} {4643.620 1701.760} \
                           {3151.665 993.280} {4643.620 1004.800} \
                           {3151.665 57.280} {3163.185 996.160}} \
              -cycle_color \
              [get_cells u0_3/pd_switchable/*_ISO]
#MM change the region from 1008.68 to 1005.68 to get power to the top row empty

#create_bounds -name misc_iso_region \
              -type hard \
              -exclusive \
              -coordinate {{1751.255 1419.520} {4032.075 1431.040} \
                           {1751.255 1431.040} {1762.775 2364.160} \
                           {1751.255 2364.160} {4032.075 2375.680} \
                           {4020.555 1431.040} {4032.075 2364.160}} \
              -cycle_color \
              [get_cells u_m/u_m_pd/*_ISO]

