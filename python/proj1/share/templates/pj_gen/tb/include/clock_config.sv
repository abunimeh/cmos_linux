//------------------------------------
// Set the default clock parameters 
//------------------------------------
`ifndef CLOCK_CONFIG__SV 
`define CLOCK_CONFIG__SV 
package clock_config; 
   `timescale 1ns/100ps 
   
   parameter HALF_CLK = 5;     // half clock period
   parameter CLK_SKEW = 0 ;    // clock activated delay at the beginning
   parameter CLK_INIT = 1'b0 ; // clock initial value
   parameter CLK_JITTER = 0 ;  // delay = HALF_CLK +/-(CLK_JITTER). 

endpackage: clock_config

`endif
