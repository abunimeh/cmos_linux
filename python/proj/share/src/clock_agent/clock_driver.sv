`ifndef CLOCK_DRIVER__SV
`define CLOCK_DRIVER__SV
class clock_driver extends uvm_driver # (clock_transaction); 

   typedef virtual clock_if vif; 
   vif clk_if; 
   `uvm_component_utils(clock_driver) 

   int half_clk;
   int clk_skew;
   int jitter;
   bit clk_init;
   int clk_jitter;

   extern function new(string name, uvm_component parent); 
   extern virtual function void connect_phase(uvm_phase phase); 
   extern virtual function void end_of_elaboration_phase(uvm_phase phase); 
   extern virtual task run_phase(uvm_phase phase); 
   extern protected virtual task drive(); 

endclass: clock_driver 

function clock_driver::new(string name, uvm_component parent); 
   super.new(name, parent); 
endfunction: new

function void clock_driver::connect_phase(uvm_phase phase); 
   super.connect_phase(phase); 
   uvm_config_db#(vif)::get(this, "", "clk_if", clk_if);
endfunction: connect_phase 

function void clock_driver::end_of_elaboration_phase(uvm_phase phase); 
   super.end_of_elaboration_phase(phase); 
   if(clk_if == null)
      `uvm_fatal(get_name(), "Virtual port not connected to the clock interface instance"); 
endfunction: end_of_elaboration_phase 

task clock_driver::run_phase(uvm_phase phase); 
   super.run_phase(phase); 
      drive();
endtask: run_phase

task clock_driver::drive(); 
   seq_item_port.get_next_item(req);
   `uvm_info("clk_drv", "Get clock configuration.", UVM_FULL)
   half_clk   = req.half_clk;
   clk_skew   = req.clk_skew;   
   clk_init   = req.clk_init;
   clk_jitter = req.clk_jitter;
   seq_item_port.item_done();

   `uvm_info(get_name(), "Start driving clock signal.", UVM_FULL)
   clk_if.clk <= clk_init;
   #(clk_skew); 
   forever begin 
      if(clk_jitter) begin 
         jitter = $urandom_range(0 , (clk_jitter*2));
         jitter = clk_jitter - jitter;
      end else begin 
         jitter = 0;
      end  
      #(half_clk + jitter); 
      clk_if.clk <= !clk_if.clk;
   end 
endtask: drive

`endif
