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

   `uvm_object_utils(clock_transaction) 

   function new(string name = "clock_transaction");
      super.new(name);
   endfunction: new

endclass: clock_transaction 

`endif 
