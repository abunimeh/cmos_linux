class reset_driver extends uvm_driver # (reset_transaction); 

   typedef virtual reset_if vif; 
   vif drv_if; 
   `uvm_component_utils(reset_driver) 

   extern function new(string name = "driver", uvm_component parent = null); 

   extern virtual function void build_phase(uvm_phase phase); 
   extern virtual function void end_of_elaboration_phase(uvm_phase phase); 
   extern virtual function void connect_phase(uvm_phase phase); 
   extern virtual task run_phase(uvm_phase phase); 
   extern protected virtual task drive_rst(); 

endclass: reset_driver 

function reset_driver::new(string name, uvm_component parent); 
   super.new(name, parent); 
endfunction: new

function void reset_driver::build_phase(uvm_phase phase); 
   super.build_phase(phase); 
endfunction: build_phase 

function void reset_driver::connect_phase(uvm_phase phase); 
   super.connect_phase(phase); 
   uvm_config_db#(vif)::get(this, "", "rst_if", drv_if);
endfunction: connect_phase 

function void reset_driver::end_of_elaboration_phase(uvm_phase phase); 
   super.end_of_elaboration_phase(phase); 
   if(drv_if == null)
      `uvm_fatal("NO_CONN", "Virtual port not connected to the reset interface instance"); 
endfunction: end_of_elaboration_phase 

task reset_driver::run_phase(uvm_phase phase); 
   super.run_phase(phase); 
   phase.raise_objection(this, "");
   fork 
      drive_rst();
   join 
   phase.drop_objection(this);
endtask: run_phase

task reset_driver::drive_rst(); 
   reset_transaction tr;
   seq_item_port.get_next_item(tr);
   drv_if.rst_n <= tr.reset_gen_init_value; 
   if (tr.reset_gen_init_value == 0); begin 
      @(posedge drv_if.clk)
      drv_if.rst_n <= 1;
   end 

   forever begin 
      if(tr.reset_enable) begin  
         repeat(tr.reset_pending_cycle) @(posedge drv_if.clk);
         #(tr.reset_pending_time); drv_if.rst_n <= 0;
         repeat(tr.reset_hold_cycle) @(posedge drv_if.clk); 
         drv_if.rst_n <= 1; 
      end 
      else begin 
         drv_if.rst_n <= 1;
      end 
      seq_item_port.item_done();

      tr = new();
      seq_item_port.get_next_item(tr);
   end 
endtask: drive_rst

