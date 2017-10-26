

#set_fp_pin_constraints -corner_keepout_percent_side 30 -block

create_floorplan \
        -control_type aspect_ratio \
        -core_utilization 0.8 \
        -row_core_ratio 1 \
        -left_io2core 10 \
        -bottom_io2core 10 \
        -right_io2core 10 \
        -top_io2core 10 \
        -flip_first_row \
        -start_first_row


