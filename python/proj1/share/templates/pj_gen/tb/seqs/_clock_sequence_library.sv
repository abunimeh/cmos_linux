`ifndef {{module_name}}_CLOCK_SEQUENCE_LIBRARY__SV
`define {{module_name}}_CLOCK_SEQUENCE_LIBRARY__SV

class {{module_name}}_clock_sequence_library extends uvm_sequence_library # (clock_transaction);
  
  `uvm_object_utils({{module_name}}_clock_sequence_library)
  `uvm_sequence_library_utils({{module_name}}_clock_sequence_library)

  function new(string name = "{{module_name}}_clock_sequence_library");
    super.new(name);
    init_sequence_library();
  endfunction

endclass  


class clock_base_sequence extends uvm_sequence # (clock_transaction); 

   `uvm_object_utils(clock_base_sequence) 

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
endclass: clock_base_sequence

class clock_specific_example extends clock_base_sequence;

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
