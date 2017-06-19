class reset_driver extends uvm_driver # (reset_transaction); 

   typedef virtual reset_if vif; 
   vif drv_if; 
   extern function new(string name = "reset_driver",
                       uvm_component parent = null); 
 
      `uvm_component_utils_begin(reset_driver)
      // ToDo: Add uvm driver member
       `uvm_component_utils_end
   // ToDo: Add required short hand override method

 //  extern function new(string name = "reset_driver", uvm_component parent = null); 
  // `uvm_component_utils(reset_driver)
   //`uvm_component_utils_end

   extern virtual function void build_phase(uvm_phase phase); 
   extern virtual function void end_of_elaboration_phase(uvm_phase phase); 
   extern virtual function void connect_phase(uvm_phase phase); 
   extern virtual task run_phase(uvm_phase phase); 
   extern protected virtual task drive_rst(); 
   extern protected virtual task send(reset_transaction tr); 
   extern protected virtual task send_idle(); 
endclass: reset_driver 

function reset_driver::new(string name = "reset_driver",
                   uvm_component parent = null);
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
   //phase.raise_objection(this, "");
   fork 
      drive_rst();
   join 
   //phase.drop_objection(this);
endtask: run_phase
/*
   rand int reset_pending_cycle;
   rand int reset_pending_time;
   rand int reset_hold_cycle;

   rand bit reset_enable;
   rand bit reset_gen_init_value;
*/

task reset_driver::drive_rst(); 
   /*
   drv_if.rst_n <= tr.reset_gen_init_value; 
   if (tr.sync_clk == 1) begin 
      @(posedge drv_if.clk)
      drv_if.rst_n <= 1;
   end
   else begin
      drv_if.rst_n <= 0;
      #50;
      drv_if.rst_n <= 1;
   end 
*/ 
  drv_if.rst_n <= 1;
   #1;
   drv_if.rst_n <= 0;
   #50;   
   drv_if.rst_n <= 1;

   forever begin
      //`uvm_info(get_name(), "Start Reset...", UVM_LOW)
      reset_transaction tr;
      seq_item_port.get_next_item(tr);
      if (tr == null) begin
          send_idle();
      end
      else begin
          `uvm_info("rst_DRIVER", tr.sprint(),UVM_MEDIUM)
          if(tr.reset_enable) begin
            `uvm_info("rst_DRIVER", "Starting transaction...",UVM_LOW)
            send(tr);   
            `uvm_info("rst_DRIVER", "Completed transaction...",UVM_LOW)
          end
          else begin 
            `uvm_info(get_name(), "Start Reset with reset_enable low...", UVM_LOW)
            #(tr.reset_hold_cycle);
          end
          seq_item_port.item_done();
      end 
   end 
endtask: drive_rst

task reset_driver::send(reset_transaction tr);
    `uvm_info(get_name(), "Start Reset...", UVM_LOW)
    if (tr.sync_clk == 1) begin 
      repeat(tr.reset_pending_cycle) @(posedge drv_if.clk);
      #(tr.reset_pending_time); drv_if.rst_n <= 0;
      repeat(tr.reset_hold_cycle) @(posedge drv_if.clk); 
      drv_if.rst_n <= 1; 
      end
      else begin
        #(tr.reset_pending_time); 
        drv_if.rst_n <= 0;
        #(tr.reset_hold_cycle);
        drv_if.rst_n <= 1; 
      end
    //rst_cov.sample();
endtask: send

task reset_driver::send_idle();
  begin
      //@(negedge drv_if.clk);
      # 1000;
      drv_if.rst_n <= 1;
  end
endtask

