class reset_transaction extends uvm_sequence_item; 
   rand int reset_pending_cycle;
   rand int reset_pending_time;
   rand int reset_hold_cycle;

   rand bit reset_enable;
   rand bit reset_gen_init_value;
   
   //   rand bit ctl_disable_init;
   //   rand bit ctl_disable_seq;
   //   rand bit ctl_set_enable;

   constraint default_config{
      reset_pending_cycle  == RESET_PENDING_CYCLE;
      reset_pending_time   == RESET_PENDING_TIME;
      reset_hold_cycle     == RESET_HOLD_CYCLE;
      reset_enable         == RESET_ENABLE;
      reset_gen_init_value == RESET_GEN_INIT_VALUE;
   }

   `uvm_object_utils_begin(reset_transaction) 
   `uvm_object_utils_end 

   function new(string name = "reset_transaction");
      super.new(name);
   endfunction: new

endclass: reset_transaction 
