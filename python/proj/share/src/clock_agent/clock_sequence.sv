`ifndef CLOCK_SEQUENCE__SV
`define CLOCK_SEQUENCE__SV
class clock_default_sequence extends uvm_sequence # (clock_transaction); 

   `uvm_object_utils(clock_default_sequence) 

   function new(string name = "clock_default_sequence");
      super.new(name);
   endfunction: new 

   virtual task pre_body(); 
      if (starting_phase != null)
         starting_phase.raise_objection(this); 
   endtask: pre_body 
   
   virtual task body(); 
      `uvm_do(req)
   endtask:body 

   virtual task post_body(); 
      if (starting_phase != null) 
         starting_phase.drop_objection(this); 
   endtask: post_body
endclass: clock_default_sequence

class clock_specific_example extends clock_default_sequence;

   clock_transaction clk_example;
   `uvm_object_utils(clock_specific_example) 

   function new(string name = "clock_specific_example");
      super.new(name);
   endfunction: new 

   virtual task body(); 
      clk_example = new();
      clk_example.constraint_mode(0);
      `uvm_rand_send_with(clk_example, {half_clk   == 10;
                                        clk_skew   == 5;
                                        clk_init   == 1'b0;
                                        clk_jitter == 1;})
   endtask:body 
endclass: clock_specific_example

`endif 
