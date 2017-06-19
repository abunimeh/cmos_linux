`ifndef {{module_name}}_{{agt_name}}_OTRANS__SV
`define {{module_name}}_{{agt_name}}_OTRANS__SV


class {{module_name}}_{{agt_name}}_otrans extends uvm_sequence_item;
   // ToDo: Add relevant class properties to define all transactions
   //rand bit [x:0] x;
   constraint {{module_name}}_{{agt_name}}_otrans_cons {
      // ToDo: Define constraint to make descriptor valid
   }

   `uvm_object_utils_begin({{module_name}}_{{agt_name}}_otrans) 
      //  ToDo: Add properties using macros here
     //`uvm_field_int(x, UVM_ALL_ON)
   `uvm_object_utils_end
 
   extern function new(string name = "{{module_name}}_{{agt_name}}_otrans");
endclass: {{module_name}}_{{agt_name}}_otrans

function {{module_name}}_{{agt_name}}_otrans::new(string name = "{{module_name}}_{{agt_name}}_otrans");
   super.new(name);
endfunction: new

`endif // {{module_name}}_{{agt_name}}_OTRANS__SV
