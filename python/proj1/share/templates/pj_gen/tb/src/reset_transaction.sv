class reset_transaction extends uvm_sequence_item; 
   rand int reset_pending_cycle;
   rand int reset_pending_time;
   rand int reset_hold_cycle;
   rand int sync_clk;
   rand bit reset_enable;
   rand bit reset_gen_init_value;
   
   //   rand bit ctl_disable_init;
   //   rand bit ctl_disable_seq;
   //   rand bit ctl_set_enable;
/*
   constraint reset_sync_clk{
       sync_clk == 0;
   }

   constraint default_config{
      reset_pending_cycle  == RESET_PENDING_CYCLE;
      reset_pending_time   == RESET_PENDING_TIME;
      reset_hold_cycle     == RESET_HOLD_CYCLE;
      reset_enable         == RESET_ENABLE;
      reset_gen_init_value == RESET_GEN_INIT_VALUE;
   }
*/
   `uvm_object_utils_begin(reset_transaction) 
     `uvm_field_int(reset_pending_cycle, UVM_ALL_ON)
     `uvm_field_int(reset_pending_time, UVM_ALL_ON)
     `uvm_field_int(reset_hold_cycle, UVM_ALL_ON)
     `uvm_field_int(sync_clk, UVM_ALL_ON)
     `uvm_field_int(reset_enable, UVM_ALL_ON)
     `uvm_field_int(reset_gen_init_value, UVM_ALL_ON)
   `uvm_object_utils_end 

   function new(string name = "reset_transaction");
      super.new(name);
   endfunction: new

endclass: reset_transaction 
