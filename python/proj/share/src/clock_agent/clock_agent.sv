`ifndef CLOCK_AGENT__SV 
`define CLOCK_AGENT__SV 
class clock_agent extends uvm_agent; 

   clock_driver clk_drv;
   clock_sequencer clk_seqr;
   typedef virtual clock_if vif;
   vif clk_if;

   `uvm_component_utils(clock_agent)

   function new(string name, uvm_component parent);
      super.new(name, parent);
   endfunction: new 

   virtual function void build_phase(uvm_phase phase); 
      super.build_phase(phase); 
      clk_drv = clock_driver::type_id::create("clk_drv", this); 
      clk_seqr = clock_sequencer::type_id::create("clk_seqr", this); 
      if(!uvm_config_db#(vif)::get(this, "", "clk_if", clk_if)) 
         `uvm_fatal("NOVIF", "No virtual interface for clock agent")
      uvm_config_db# (vif)::set(this, "clk_drv", "clk_if", clk_if);
   endfunction: build_phase


   virtual function void connect_phase(uvm_phase phase); 
      super.connect_phase(phase); 
      clk_drv.seq_item_port.connect(clk_seqr.seq_item_export);
   endfunction: connect_phase 

endclass: clock_agent

`endif
