`ifndef {{seq_name}}__SV
`define {{seq_name}}__SV

//-----------------------------------------------------------------------------
//
// CLASS:{{seq_name}} 
//
// Priority: 
// Engg.: 
// Suite: {{module_name}}
//
// Description:
//-----------------------------------------------------------------------------


class {{seq_name}} extends {{module_name}}_base_sequence ;
    
    {{module_name}}_fetch_trans  req;
    
    `uvm_object_utils({{seq_name}})
    `uvm_add_to_seq_lib({{seq_name}},{{module_name}}_sequence_library)

    function new(string name = "{{seq_name}}");
        super.new(name);
    endfunction:new

    virtual task body();
        repeat(1) begin
                    {{seq}}
                  end 
    endtask             
endclass:{{seq_name}}
`endif //{{seq_name}}
