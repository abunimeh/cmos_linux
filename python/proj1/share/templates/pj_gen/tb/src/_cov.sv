//
// Template for UVM-compliant Coverage Class
//

`ifndef {{module_name}}_COV__SV
`define {{module_name}}_COV__SV

{%-for a_name in agt_name_lst%}
`uvm_analysis_imp_decl(_{{a_name}}_out)
`uvm_analysis_imp_decl(_{{a_name}}_in)
{% endfor %}

//-----------------------------------------------------------------------------
//
// CLASS: {{module_name}}_cov
//
// 
//-----------------------------------------------------------------------------

class {{module_name}}_cov extends uvm_component;
   event event_in;
   event event_out;
{%-for a_name in agt_name_lst%}
   {{module_name}}_{{a_name}}_itrans {{a_name}}_tr_in;
   {{module_name}}_{{a_name}}_otrans {{a_name}}_tr_out;
{% endfor %}
{%-for a_name in agt_name_lst%}
   uvm_analysis_imp_{{a_name}}_out#({{module_name}}_{{a_name}}_otrans, {{module_name}}_cov) {{a_name}}_out_imp;
   uvm_analysis_imp_{{a_name}}_in# ({{module_name}}_{{a_name}}_itrans, {{module_name}}_cov) {{a_name}}_in_imp;
{% endfor %}

   `uvm_component_utils({{module_name}}_cov)
 


   covergroup cg_itrans @(event_in);
   //ToDo: Add input coverage here

   endgroup: cg_itrans


/*
  event: cg_otrans
  
  Discription: To cover output siginals of dut
*/

   covergroup cg_otrans @(event_out);
   //ToDo: Add output coverage here

   endgroup: cg_otrans

   function new(string name, uvm_component parent);
      super.new(name,parent);
      cg_itrans = new();
      cg_otrans = new();
   endfunction: new

   function void build_phase(uvm_phase phase);
      super.build_phase(phase);
{%-for a_name in agt_name_lst%}
      {{a_name}}_in_imp = new("{{a_name}}_in_imp",this);
      {{a_name}}_out_imp = new("{{a_name}}_out_imp",this);
{% endfor %}
   endfunction: build_phase

{%-for a_name in agt_name_lst%}
   virtual function write_{{a_name}}_in({{module_name}}_{{a_name}}_itrans tr);
      this.{{a_name}}_tr_in = tr;
      -> event_in;
   endfunction: write_{{a_name}}_in

   virtual function write_{{a_name}}_out({{module_name}}_{{a_name}}_otrans tr);
      this.{{a_name}}_tr_out = tr;
      -> event_out;
   endfunction: write_{{a_name}}_out
{% endfor %}

endclass: {{module_name}}_cov

`endif // {{module_name}}_COV__SV

