//`ifndef reset_agent 
//`define reset_agent
class reset_agent extends uvm_agent; 

   reset_sequencer rst_seqr;
   reset_driver rst_drv;
   typedef virtual reset_if vif;
   vif rst_if;

   `uvm_component_utils(reset_agent)

   function new(string name, uvm_component parent);
      super.new(name, parent);
   endfunction: new 

   virtual function void build_phase(uvm_phase phase); 
      super.build_phase(phase); 
      rst_seqr = reset_sequencer::type_id::create("rst_seqr", this); 
      rst_drv = reset_driver::type_id::create("rst_drv", this); 
      if(!uvm_config_db#(vif)::get(this, "", "rst_if", rst_if)) 
         `uvm_fatal("NOVIF", "No virtual interface for reset agent")
      uvm_config_db# (vif)::set(this, "drv", "rst_if", rst_if);
   endfunction: build_phase

   virtual function void connect_phase(uvm_phase phase); 
      super.connect_phase(phase); 
      rst_drv.seq_item_port.connect(rst_seqr.seq_item_export);
   endfunction: connect_phase 

endclass: reset_agent

//`endif
