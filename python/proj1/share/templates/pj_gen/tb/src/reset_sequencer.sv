
`ifndef RESET_SEQR__SV
`define RESET_SEQR__SV
class reset_sequencer extends uvm_sequencer # (reset_transaction); 

   `uvm_component_utils(reset_sequencer) 
   function new (string name, uvm_component parent); 
      super.new(name, parent); 
   endfunction: new 
endclass: reset_sequencer
`endif // RESET_SEQR__SV
