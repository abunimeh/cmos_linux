`ifndef {{module_name}}_SEQUENCE_LIBRARY__SV
`define {{module_name}}_SEQUENCE_LIBRARY__SV

{%-for a_name in agt_name_lst%}
class {{module_name}}_{{a_name}}_sequence_library extends uvm_sequence_library # ({{module_name}}_{{a_name}}_itrans);
  
  `uvm_object_utils({{module_name}}_{{a_name}}_sequence_library)
  `uvm_sequence_library_utils({{module_name}}_{{a_name}}_sequence_library)

  function new(string name = "{{module_name}}_{{a_name}}_sequence_library");
    super.new(name);
    init_sequence_library();
  endfunction

endclass  

class {{module_name}}_{{a_name}}_base_sequence extends uvm_sequence #({{module_name}}_{{a_name}}_itrans);
  `uvm_object_utils({{module_name}}_{{a_name}}_base_sequence)

  function new(string name = "{{module_name}}_{{a_name}}_base_sequence");
    super.new(name);
  endfunction:new

  virtual task pre_body();
    if (starting_phase != null)
      starting_phase.raise_objection(this);
  
  endtask:pre_body
  virtual task post_body();
    if (starting_phase != null)
      starting_phase.drop_objection(this);

  endtask:post_body
endclass

class sequence_{{a_name}}_smoke extends {{module_name}}_{{a_name}}_base_sequence;
    
    {{module_name}}_{{a_name}}_itrans req;
    bit [15:0] packet_num;
    
    `uvm_object_utils(sequence_{{a_name}}_smoke)
    `uvm_add_to_seq_lib(sequence_{{a_name}}_smoke,{{module_name}}_{{a_name}}_sequence_library)

    function new(string name = "sequence_{{a_name}}_smoke");
        super.new(name);
    endfunction:new

    virtual task body();
        repeat(1) begin
            `uvm_do_with(req,{
              //mark_rdy=='h1;
            });
        end
    endtask
endclass: sequence_{{a_name}}_smoke
{% endfor %}

`endif // {{module_name}}_SEQUENCE_LIBRARY__SV
