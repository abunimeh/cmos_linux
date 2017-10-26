




############ voltage area DEFAULT_VA ######################
set_fp_rail_voltage_area_constraints \
                -voltage_area DEFAULT_VA \
                -voltage_supply 1.08 \
                -nets {VDD GND} \
                -target_voltage_drop 100 \
                -power_budget 25

set_fp_rail_voltage_area_constraints \
                -voltage_area DEFAULT_VA \
                -layer T4M2 \
                -max_width 3 -min_width 3 \
                -max_strap 5 -min_strap 5 \
                -offset -5 \
                -direction vertical


set_fp_rail_voltage_area_constraints \
                -voltage_area DEFAULT_VA \
                -layer RDL \
                -max_width 3 -min_width 3 \
                -max_strap 5 -min_strap 5 \
                -offset -5 \
                -direction horizontal

set_fp_rail_voltage_area_constraints \
                -voltage_area DEFAULT_VA \
                -ring_nets  {VDD GND} \
                -ring_width 1.26 \
                -ring_spacing 1 \
                -ring_offset 1 \
                -horizontal_ring_layer M6 \
                -vertical_ring_layer T4M2 \
                -extend_strap core_ring

set_fp_rail_voltage_area_constraints \
                -voltage_area DEFAULT_VA \
                -global -allow_routing_over_voltage_area




