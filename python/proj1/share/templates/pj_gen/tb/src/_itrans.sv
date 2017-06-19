`ifndef {{module_name}}_{{agt_name}}_ITRANS__SV
`define {{module_name}}_{{agt_name}}_ITRANS__SV


class {{module_name}}_{{agt_name}}_itrans extends uvm_sequence_item;
   // ToDo: Add relevant class properties to define all transactions
   //rand bit xx;


   constraint {{module_name}}_zllhc__itrans_cons {
      // ToDo: Define constraint to make descriptor valid

   }

   `uvm_object_utils_begin({{module_name}}_{{agt_name}}_itrans) 
      // ToDo: Add properties using macros here
     //`uvm_field_int(xx, UVM_ALL_ON)
   `uvm_object_utils_end
 
   extern function new(string name = "{{module_name}}_{{agt_name}}_itrans");
endclass: {{module_name}}_{{agt_name}}_itrans


function {{module_name}}_{{agt_name}}_itrans::new(string name = "{{module_name}}_{{agt_name}}_itrans");
   super.new(name);
endfunction: new


`endif // {{module_name}}_{{agt_name}}_ITRANS__SV
