`ifndef CLOCK_SEQUENCER__SV
`define CLOCK_SEQUENCER__SV
class clock_sequencer extends uvm_sequencer # (clock_transaction); 

   `uvm_component_utils(clock_sequencer) 
   function new (string name, uvm_component parent); 
      super.new(name, parent); 
   endfunction: new 

endclass: clock_sequencer

`endif 
