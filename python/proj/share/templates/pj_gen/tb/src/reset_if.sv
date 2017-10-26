interface reset_if(input logic clk);
   logic rst;     // active high reset 
   logic rst_n;   // active low reset 
   assign rst = !rst_n; 
endinterface
