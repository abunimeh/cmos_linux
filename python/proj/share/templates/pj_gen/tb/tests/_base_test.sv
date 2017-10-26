`ifndef {{module_name}}__base_test__SV
`define {{module_name}}__base_test__SV

//import uvm_pkg::*;
//import {{module_name}}_pkg::*;
typedef class {{module_name}}_env;

class {{module_name}}__base_test extends uvm_test;

  `uvm_component_utils({{module_name}}__base_test)

  {{module_name}}_env env;

  function new(string name, uvm_component parent);
    super.new(name, parent);
  endfunction

  virtual function void build_phase(uvm_phase phase);
    super.build_phase(phase);
    env = {{module_name}}_env::type_id::create("env", this);
    //ToDo: set default sequence in inherited test cases
    uvm_config_db #(uvm_object_wrapper)::set(this, "env.clk_agt.clk_seqr.run_phase", "default_sequence", clock_base_sequence::get_type());
  endfunction

  task main_phase(uvm_phase phase);
    phase.phase_done.set_drain_time(this, 100ns);
  endtask: main_phase
endclass : {{module_name}}__base_test


class {{module_name}}__smoke_test extends {{module_name}}__base_test;

  `uvm_component_utils({{module_name}}__smoke_test)

  function new(string name, uvm_component parent);
    super.new(name, parent);
  endfunction

  virtual function void build_phase(uvm_phase phase);
    super.build_phase(phase);
    //ToDo: set default sequence in inherited test cases
{%-if with_vseq%}
    uvm_config_db #(uvm_object_wrapper)::set(this, "env.vseqr.main_phase", "default_sequence", {{module_name}}_vseq_smoke::get_type());
{%-else%}
  {%-for a_name in agt_name_lst%}
    uvm_config_db #(uvm_object_wrapper)::set(this, "env.{{a_name}}_agt.{{a_name}}_seqr.main_phase", "default_sequence", sequence_{{a_name}}_smoke::get_type());
  {%-endfor%}
{%-endif%}    
  endfunction

endclass : {{module_name}}__smoke_test
`endif //{{module_name}}__base_test__SV


