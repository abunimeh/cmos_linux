`ifndef CLOCK_SEQUENCER__SV
`define CLOCK_SEQUENCER__SV
class clock_sequencer extends uvm_sequencer # (clock_transaction); 

   `uvm_component_utils(clock_sequencer) 
   function new (string name, uvm_component parent); 
      super.new(name, parent); 
   endfunction: new 

   task reset_phase(uvm_phase phase);
      super.reset_phase(phase);
      this.stop_sequences();
   endtask: reset_phase


endclass: clock_sequencer

`endif 
