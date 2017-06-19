`ifndef {{module_name}}_TB_MOD__SV
`define {{module_name}}_TB_MOD__SV

`include "{{module_name}}_intfs.inc"

program {{module_name}}_tb_mod;

import uvm_pkg::*;
import {{module_name}}_pkg::*;
// ToDo: Include all other test list here
{%-for a_name in agt_name_lst%}
   typedef virtual {{module_name}}_{{a_name}}_if {{a_name}}_if;
{% endfor %}
   typedef virtual clock_if clk_interface;

   string case_name;
   string output_dir;
   string golden_result;

   initial begin 
      if($test$plusargs("TEMPDIR")) begin
          $value$plusargs("TEMPDIR=%s", output_dir);
      end else begin 
         $display("ERROR: Get output directory failed!");
         $exit();
      end 

      if($test$plusargs("UVM_TESTNAME")) begin 
         $value$plusargs("UVM_TESTNAME=%s", case_name);
         golden_result = $sformatf("%s/%s_result.txt", output_dir, case_name);
         uvm_config_db #(string)::set(null,"uvm_test_top.env.sb","golden_result",golden_result);
      end else begin 
         `uvm_fatal("tb_mod", "Get output testcase name failed!")
      end 
{%-for a_name in agt_name_lst%}
      uvm_config_db #({{a_name}}_if)::set(null,"uvm_test_top.env.{{a_name}}_agent.{{a_name}}_drv","{{a_name}}_drv_if",test_top.{{a_name}}_if); 
      uvm_config_db #({{a_name}}_if)::set(null,"uvm_test_top.env.{{a_name}}_agent.mon","{{a_name}}_mon_if",test_top.{{a_name}}_if); 
{% endfor %}
      uvm_config_db #(virtual reset_if)::set(null,"uvm_test_top.env","rst_if",test_top.rst_if); 
      uvm_config_db #(clk_interface)::set(null,"uvm_test_top.env","clk_if",test_top.clk_if); 
      run_test();
   end

endprogram: {{module_name}}_tb_mod

`endif // {{module_name}}_TB_MOD__SV

