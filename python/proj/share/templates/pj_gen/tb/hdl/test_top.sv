`ifndef TEST_TOP__SV
`define TEST_TOP__SV


module test_top();

import global_cfg::*; // define 'sim_cycle'

   clock_if clk_if();
   wire clk = clk_if.clk;

   reset_if  rst_if(clk_if.clk);
   {%-for a_name in agt_name_lst%}
   {{module_name}}_{{a_name}}_if {{a_name}}_if(clk,rst_if.rst_n);
   {% endfor %}

   
   {{module_name}}_tb_mod test(); 
   
   // ToDo: Include Dut instance here
   //top dut (
   //        .i_shiz (clk_if.clk),
   //        .i_fuw_d (rst_if.rst_n)
   //    );

endmodule: test_top

`endif // TEST_TOP__SV
