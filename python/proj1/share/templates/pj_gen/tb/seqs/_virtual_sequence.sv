`ifndef {{module_name}}_VIRTUAL_SEQUENCE__SV
`define {{module_name}}_VIRTUAL_SEQUENCE__SV

class {{module_name}}_vseq_base extends uvm_sequence #(uvm_sequence_item);
  `uvm_object_utils({{module_name}}_vseq_base)
  {{module_name}}_vseqr vseqr;
{%-for a_name in agt_name_lst%}
    {{module_name}}_{{a_name}}_seqr {{a_name}}_seqr;
{% endfor %}

  function new(string name = "{{module_name}}_vseq_base");
    super.new(name);
  endfunction:new

  virtual task pre_body();
    if (starting_phase != null)
      starting_phase.raise_objection(this);
  endtask:pre_body

  virtual task body();
    //if (uvm_config_db#({{module_name}}_cfg)::get(null, get_full_name(), "{{module_name}}_cfg", cfg))
    //    `uvm_info(get_type_name(), $sformatf("get config.xx value=%d via config", cfg.xx), UVM_MEDIUM)
    //else
    //    `uvm_error(get_type_name(), "cannot get xx value!")
  endtask: body

  virtual task post_body();
    if (starting_phase != null)
      starting_phase.drop_objection(this);
  endtask:post_body

endclass: {{module_name}}_vseq_base

//--------------------------------------------------------------
// vseq smoke
//--------------------------------------------------------------
class {{module_name}}_vseq_smoke extends {{module_name}}_vseq_base;

  `uvm_object_utils({{module_name}}_vseq_smoke)
  `uvm_declare_p_sequencer({{module_name}}_vseqr)

  function new(string name = "{{module_name}}_vseq_smoke");
    super.new(name);
  endfunction:new
  
  virtual task body();
{%-for a_name in agt_name_lst%}
    sequence_{{a_name}}_smoke {{a_name}}_smoke;
{% endfor %}

    fork
{%-for a_name in agt_name_lst%}
    `uvm_do_on({{a_name}}_smoke, p_sequencer.{{a_name}}_seqr)
{% endfor %}
    join_any
  endtask: body

endclass:{{module_name}}_vseq_smoke
`endif

