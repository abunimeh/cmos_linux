1. declare clock interface in the testbench top
	clock_if clk_if();

2. include "clock_if.sv" and set virtual interface in techbench mode
	`include "clock_if.sv"
  	uvm_config_db #(virtual clock_if)::set(null,"","clk_if",test_top.clk_if);

3. instantiate clock agent and set virtual interface in environment

4. specific your clock configuration in "clock_config.sv"

5. include the file "clock_pkg.incl" in your project package
