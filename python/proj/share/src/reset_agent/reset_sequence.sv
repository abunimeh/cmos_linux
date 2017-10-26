class reset_sequence extends uvm_sequence # (reset_transaction); 

   `uvm_object_utils(reset_sequence) 

   function new(string name = "reset_sequence");
      super.new(name);
   endfunction: new 

   virtual task pre_body(); 
      if (starting_phase != null)
         starting_phase.raise_objection(this); 
         `uvm_do(req);
   endtask: pre_body 
   
   virtual task body(); 
   endtask:body 

   virtual task post_body(); 
      if (starting_phase != null) 
         starting_phase.drop_objection(this); 
   endtask: post_body
endclass: reset_sequence
