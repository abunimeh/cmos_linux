//import uvm_pkg::*;
//import {{module_name}}_pkg::*;

`ifndef {{case_name}}__SV
`define {{case_name}}__SV

//-----------------------------------------------------------------------------
//
// CLASS: {{case_name}}
//
// Priority: 
// Engg.:
// Suite: {{module_name}}
//
// Description: 
//             source file directory:{{src_dir}}
//             seed:{{seed}} 
//-----------------------------------------------------------------------------
 
class {{case_name}} extends {{module_name}}__base_test;
  
    `uvm_component_utils({{case_name}})
 
     function new(string name,uvm_component parent);
         super.new(name,parent);
     endfunction: new
     
     {%-if module_name=='slbs' %}
     virtual function void build_phase(uvm_phase phase);
         super.build_phase(phase);
          uvm_config_db #(uvm_object_wrapper)::set(this, "env.iagent.sqr.main_phase", "default_sequence", {{seq_name}}::get_type());
          uvm_config_db #(uvm_object_wrapper)::set(this, "env.oagent.rotator_sqr.main_phase", "default_sequence", SEQ_slbs_rotater_req1::get_type());
          uvm_config_db #(uvm_object_wrapper)::set(this, "env.clk_agt.clk_seqr.run_phase", "default_sequence", clock_base_sequence::get_type());
     endfunction: build_phase
     {%-elif module_name=='yjm' %} 
     virtual function void build_phase(uvm_phase phase);
        super.build_phase(phase);
          uvm_config_db #(uvm_object_wrapper)::set(this, "env.fetch_agt.sqr.main_phase", "default_sequence", {{seq_name}}::get_type());
          uvm_config_db #(uvm_object_wrapper)::set(this, "env.clk_agt.clk_seqr.run_phase", "default_sequence", clock_base_sequence::get_type());
          uvm_config_db #(string)::set(this,"env.sb","_filename", "inst_str_{{case_name}}_result.txt"); 
     endfunction: build_phase
     {%-elif module_name=='cdym' %}
     virtual function void build_phase(uvm_phase phase);
         super.build_phase(phase);
          uvm_config_db #(uvm_object_wrapper)::set(this, "env.zllhc_agent.zllhc_sqr.main_phase", "default_sequence",{{seq_name}}::get_type());
          uvm_config_db #(uvm_object_wrapper)::set(this, "env.slbs_agent.slbs_sqr.main_phase", "default_sequence", sequence_slbs_smoke::get_type());
     endfunction: build_phase
     {%-elif module_name=='gsq' %}
     virtual function void build_phase(uvm_phase phase);
         super.build_phase(phase);
          uvm_config_db #(uvm_object_wrapper)::set(this, "env.slbs_agt.sqr.main_phase", "default_sequence",{{seq_name}}::get_type());
          uvm_config_db #(uvm_object_wrapper)::set(this, "env.iq_agt.sqr.main_phase", "default_sequence", seq_iq_req::get_type());
          uvm_config_db #(uvm_object_wrapper)::set(this, "env.decoder_agt.sqr.main_phase", "default_sequence", SEQ_decoder_smoke::get_type());
          uvm_config_db #(uvm_object_wrapper)::set(this, "env.clk_agt.clk_seqr.run_phase", "default_sequence", clock_base_sequence::get_type());
     endfunction: build_phase
     {%-elif module_name=='rotator' %}
     virtual function void build_phase(uvm_phase phase);
         super.build_phase(phase);
          uvm_config_db #(uvm_object_wrapper)::set(this, "env.X_agent.X_sqr.main_phase", "default_sequence",{{seq_name}}::get_type());
          uvm_config_db #(uvm_object_wrapper)::set(this, "env.clk_agt.clk_seqr.run_phase", "default_sequence", clock_base_sequence::get_type());
          uvm_config_db #(uvm_object_wrapper)::set(this, "env.rst_agt.rst_seqr.run_phase", "default_sequence", sequence_rst_base::get_type());
     endfunction: build_phase
     {%-elif module_name=='split' %}
     virtual function void build_phase(uvm_phase phase);
         super.build_phase(phase);
          uvm_config_db #(uvm_object_wrapper)::set(this, "env.split_agt.sqr.main_phase", "default_sequence",{{seq_name}}::get_type());
          uvm_config_db #(uvm_object_wrapper)::set(this, "env.clk_agt.clk_seqr.run_phase", "default_sequence", clock_base_sequence::get_type());
          uvm_config_db #(uvm_object_wrapper)::set(this, "env.rst_agt.rst_seqr.run_phase", "default_sequence", sequence_rst_base::get_type());
     endfunction: build_phase
     {%-endif%}
endclass: {{case_name}}
`endif //{{case_name}}__SV

