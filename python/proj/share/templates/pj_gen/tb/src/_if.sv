//
// Template for UVM-compliant interface
//

`ifndef {{module_name}}_{{agt_name}}_IF__SV
`define {{module_name}}_{{agt_name}}_IF__SV

interface {{module_name}}_{{agt_name}}_if 
#(
    //ToDo: add parameter here
                            parameter a = 1       
                         )
      (input bit clk, input bit rst_n);
  //ToDo: Add interface siginals here
    //logic  [2:0]                  xx;

  clocking down_clk @(posedge clk);
    //ToDo: Add driver siginals here
    input  rst_n;
  endclocking:down_clk

  clocking down_mon_clk @(posedge clk);
    //ToDo: Add input siginals here
    input   rst_n;
    //input   xx;

  endclocking:down_mon_clk

endinterface: {{module_name}}_{{agt_name}}_if

`endif // {{module_name}}_{{agt_name}}_IF__SV
