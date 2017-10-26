`ifndef {{module_name}}_{{agt_name}}_SEQR__SV
`define {{module_name}}_{{agt_name}}_SEQR__SV

typedef class {{module_name}}_{{agt_name}}_itrans;

class {{module_name}}_{{agt_name}}_seqr extends uvm_sequencer # ({{module_name}}_{{agt_name}}_itrans);

   `uvm_component_utils({{module_name}}_{{agt_name}}_seqr)

   function new (string name,uvm_component parent);
   super.new(name,parent);
   endfunction:new 

   task reset_phase(uvm_phase phase);
      super.reset_phase(phase);
      this.stop_sequences();
   endtask: reset_phase

endclass:{{module_name}}_{{agt_name}}_seqr

`endif // {{module_name}}_{{agt_name}}_SEQR__SV
