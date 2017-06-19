

`ifndef {{module_name}}_RESET_SEQUENCE_LIBRARY__SV
`define {{module_name}}_RESET_SEQUENCE_LIBRARY__SV


class {{module_name}}_reset_sequence_library extends uvm_sequence_library # (reset_transaction);
  
  `uvm_object_utils({{module_name}}_reset_sequence_library)
  `uvm_sequence_library_utils({{module_name}}_reset_sequence_library)

  function new(string name = "{{module_name}}_reset_sequence_library");
    super.new(name);
    init_sequence_library();
  endfunction

endclass  

class reset_sequence extends uvm_sequence # (reset_transaction); 

   `uvm_object_utils(reset_sequence) 

   function new(string name = "reset_sequence");
      super.new(name);
   endfunction: new 

   virtual task pre_body(); 
      if (starting_phase != null)
         starting_phase.raise_objection(this); 
         //`uvm_do(req);
        `uvm_do_with(req, {
                               reset_enable ==1 ;
                               sync_clk == 0;
                               reset_hold_cycle ==2000;
                               reset_pending_time == 100;
                              }); 
   endtask: pre_body 
   
   virtual task post_body(); 
      if (starting_phase != null) 
         starting_phase.drop_objection(this); 
   endtask: post_body
endclass: reset_sequence

class sequence_rst_base extends reset_sequence;
    
    reset_transaction req;
    
    `uvm_object_utils(sequence_rst_base)
    `uvm_add_to_seq_lib(sequence_rst_base,{{module_name}}_reset_sequence_library)

    function new(string name = "sequence_rst_base");
        super.new(name);
    endfunction:new

    virtual task body();
    /*
     rand int reset_pending_cycle;
   rand int reset_pending_time;
   rand int reset_hold_cycle;
   rand int sync_clk;
   rand bit reset_enable;
   rand bit reset_gen_init_value;
   */
        repeat(1) begin
            `uvm_do_with(req, {
                               reset_enable ==1 ;
                               sync_clk == 0;
                               reset_hold_cycle ==5000;
                               reset_pending_time == 10000;
                              });
        end
    endtask
endclass: sequence_rst_base

`endif // {{module_name}}_RESET_SEQUENCE_LIBRARY__SV
