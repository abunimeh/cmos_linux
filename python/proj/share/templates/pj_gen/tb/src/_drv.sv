//
// Template for UVM-compliant physical-level transactor
//

`ifndef {{module_name}}_{{agt_name}}_DRV__SV
`define {{module_name}}_{{agt_name}}_DRV__SV

typedef class {{module_name}}_{{agt_name}}_itrans;



class {{module_name}}_{{agt_name}}_drv extends uvm_driver # ({{module_name}}_{{agt_name}}_itrans);

   typedef virtual {{module_name}}_{{agt_name}}_if v_if; 
   v_if drv_if;
 
   `uvm_component_utils_begin({{module_name}}_{{agt_name}}_drv)
   // ToDo: Add uvm driver member
   `uvm_component_utils_end


   extern function new(string name = "{{module_name}}_{{agt_name}}_drv",uvm_component parent = null); 
   extern virtual function void build_phase(uvm_phase phase);
   extern virtual task reset_phase(uvm_phase phase);
   extern virtual task configure_phase(uvm_phase phase);
   extern virtual task main_phase(uvm_phase phase);
   extern protected virtual task send({{module_name}}_{{agt_name}}_itrans tr); 
   extern protected virtual task send_idle();
   extern protected virtual task tx_driver();

endclass: {{module_name}}_{{agt_name}}_drv


function {{module_name}}_{{agt_name}}_drv::new(string name = "{{module_name}}_{{agt_name}}_drv",uvm_component parent = null);
   super.new(name, parent);
endfunction: new


function void {{module_name}}_{{agt_name}}_drv::build_phase(uvm_phase phase);
   super.build_phase(phase);
   //ToDo : Implement this phase here
   if(!uvm_config_db#(v_if)::get(this, "", "{{agt_name}}_drv_if", drv_if)) begin
      `uvm_fatal("{{module_name}}_{{agt_name}}_DRV", "No virtual interface specified for this instance")          
   end
endfunction: build_phase


task {{module_name}}_{{agt_name}}_drv::reset_phase(uvm_phase phase);
   super.reset_phase(phase);
   phase.raise_objection(this,"");
   `uvm_info("{{module_name}}_{{agt_name}}_DRV", "Reset phase start...",UVM_HIGH)
   // ToDo: Reset output signals
   //drv_if.mark_rdy <= 0;
   @(posedge drv_if.rst_n);
   phase.drop_objection(this);
endtask: reset_phase

task {{module_name}}_{{agt_name}}_drv::configure_phase(uvm_phase phase);
   super.configure_phase(phase);
   phase.raise_objection(this,"");
   //ToDo: Configure your component here
   phase.drop_objection(this);
endtask:configure_phase


task {{module_name}}_{{agt_name}}_drv::main_phase(uvm_phase phase);
   super.main_phase(phase);
   fork 
      tx_driver();
      begin
        @(negedge drv_if.rst_n);
        phase.jump(uvm_reset_phase::get());
        //ToDo: Add clear operations here
        if(req != null) seq_item_port.item_done();
      end
   join
endtask: main_phase


task {{module_name}}_{{agt_name}}_drv::tx_driver();
   forever
   begin

      `uvm_info("{{module_name}}_{{agt_name}}_DRV", "Starting transaction...",UVM_HIGH)
      seq_item_port.try_next_item(req);
      if (req == null) begin
        send_idle();
      end
      else begin       
        send(req);   
        `uvm_info("{{module_name}}_{{agt_name}}_DRV", req.sprint(),UVM_MEDIUM)
        seq_item_port.item_done();
      end
      `uvm_info("{{module_name}}_{{agt_name}}_DRV", "Completed transaction...",UVM_HIGH)

   end
endtask : tx_driver


task {{module_name}}_{{agt_name}}_drv::send({{module_name}}_{{agt_name}}_itrans tr);
   // ToDo: Drive signals on interface
   @(posedge drv_if.clk);
endtask: send


task {{module_name}}_{{agt_name}}_drv::send_idle();
   //ToDo: Drive idle state
   @(posedge drv_if.clk);
endtask

`endif // {{module_name}}_{{agt_name}}_DRV__SV


