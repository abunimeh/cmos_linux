`ifndef CLOCK_TRANSACTION__SV 
`define CLOCK_TRANSACTION__SV 
class clock_transaction extends uvm_sequence_item; 

   rand int half_clk;
   rand int clk_skew;
   rand bit clk_init;
   rand int clk_jitter;

   constraint default_config{
      half_clk   == HALF_CLK;
      clk_skew   == CLK_SKEW;
      clk_init   == CLK_INIT;
      clk_jitter == CLK_JITTER;
   }

   `uvm_object_utils_begin(clock_transaction)
     `uvm_field_int(half_clk, UVM_ALL_ON)
     `uvm_field_int(clk_skew, UVM_ALL_ON)
     `uvm_field_int(clk_init, UVM_ALL_ON)
     `uvm_field_int(clk_jitter, UVM_ALL_ON)
   `uvm_object_utils_end 

   function new(string name = "clock_transaction");
      super.new(name);
   endfunction: new

endclass: clock_transaction 

`endif 
