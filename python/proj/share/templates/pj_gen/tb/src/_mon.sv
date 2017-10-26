
`ifndef {{module_name}}_{{agt_name}}_MON__SV
`define {{module_name}}_{{agt_name}}_MON__SV

typedef class {{module_name}}_{{agt_name}}_otrans;
typedef class {{module_name}}_{{agt_name}}_itrans;

class {{module_name}}_{{agt_name}}_mon extends uvm_monitor;

   uvm_analysis_port #({{module_name}}_{{agt_name}}_otrans) {{agt_name}}_omon_analysis_port;   
   uvm_analysis_port #({{module_name}}_{{agt_name}}_itrans) {{agt_name}}_imon_analysis_port;   
   typedef virtual {{module_name}}_{{agt_name}}_if v_if;
   v_if mon_if;

   `uvm_component_utils_begin({{module_name}}_{{agt_name}}_mon)
     // ToDo: Add uvm monitor member if any class property added later through field macros
   `uvm_component_utils_end

   extern function new(string name = "{{module_name}}_{{agt_name}}_mon",uvm_component parent);
   extern virtual function void build_phase(uvm_phase phase);
   extern virtual task run_phase(uvm_phase phase);
   extern protected virtual task tx_monitor();
   extern protected virtual task rx_monitor();

endclass: {{module_name}}_{{agt_name}}_mon


function {{module_name}}_{{agt_name}}_mon::new(string name = "{{module_name}}_{{agt_name}}_mon",uvm_component parent);
   super.new(name, parent);
endfunction: new


function void {{module_name}}_{{agt_name}}_mon::build_phase(uvm_phase phase);
   super.build_phase(phase);
   {{agt_name}}_omon_analysis_port = new ("{{agt_name}}_omon_analysis_port",this);
   {{agt_name}}_imon_analysis_port = new ("{{agt_name}}_imon_analysis_port",this);
   if (!uvm_config_db#(v_if)::get(this, "", "{{agt_name}}_mon_if", mon_if)) begin
       `uvm_fatal("{{module_name}}_{{agt_name}}_MON", "No virtual interface specified for this instance")
   end
 endfunction: build_phase


task {{module_name}}_{{agt_name}}_mon::run_phase(uvm_phase phase);
   super.run_phase(phase);
   fork
      tx_monitor();
      rx_monitor();
   join

endtask: run_phase


task {{module_name}}_{{agt_name}}_mon::tx_monitor();
   forever begin
      {{module_name}}_{{agt_name}}_otrans otr;
      otr = new("otr");
      `uvm_info("{{module_name}}_{{agt_name}}_OMON", "Starting transaction...",UVM_HIGH)
      @(posedge mon_if.clk);
      //ToDo: Add siginal sample here
      //otr.xx       =mon_if.down_mon_clk.xx       ;

      `uvm_info("{{module_name}}_{{agt_name}}_OMON", "Completed transaction...",UVM_HIGH)
      `uvm_info("{{module_name}}_{{agt_name}}_OMON", otr.sprint(),UVM_HIGH)
      {{agt_name}}_omon_analysis_port.write(otr);
   end
endtask: tx_monitor

task {{module_name}}_{{agt_name}}_mon::rx_monitor();
   forever begin
      {{module_name}}_{{agt_name}}_itrans itr;
      itr = new("itr");
      `uvm_info("{{module_name}}_{{agt_name}}_IMON", "Starting transaction...",UVM_HIGH)
      @(posedge mon_if.clk);
      //ToDo: Add siginal sample here
      //itr.xx = mon_if.xx;
      `uvm_info("{{module_name}}_{{agt_name}}_IMON", "Completed transaction...",UVM_HIGH)
      `uvm_info("{{module_name}}_{{agt_name}}_IMON", itr.sprint(),UVM_HIGH)
      {{agt_name}}_imon_analysis_port.write(itr);
   end
endtask: rx_monitor

`endif // {{module_name}}_{{agt_name}}_MON__SV
