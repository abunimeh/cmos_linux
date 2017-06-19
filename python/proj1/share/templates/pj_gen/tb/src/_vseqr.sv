`ifndef {{module_name}}_Vseqr__SV
`define {{module_name}}_Vseqr__SV

//-----------------------------------------------------------------------------
//
// CLASS: {{module_name}}_vseqr
//
// A virtual sequence in verification environment.
//-----------------------------------------------------------------------------


class {{module_name}}_vseqr extends uvm_sequencer;
{%-for a_name in agt_name%}
    {{module_name}}_{{a_name}}_seqr {{a_name}}_seqr;
{% endfor %}

   `uvm_component_utils({{module_name}}_vseqr)

   function new (string name,uvm_component parent);
   super.new(name,parent);
   endfunction:new 

   task reset_phase(uvm_phase phase);
      super.reset_phase(phase);
      this.stop_sequences();
   endtask: reset_phase

endclass:{{module_name}}_vseqr

`endif // {{module_name}}_Vseqr__SV
