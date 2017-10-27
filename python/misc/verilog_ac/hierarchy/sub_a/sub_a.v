module sub_a (/*AUTOARG*/);
   output sub_a__sub_b__s1;
   output ssub_b__sub_b__s1;
   input  top__sub_a__ss1;
   input  top__sub_a__s1;
   input [1:0] top__sub_a__s2;
   input  top__ssub_a__s2;
   input  top__ssub_b__s3;
   
   /*AUTOREG*/
   /*AUTOWIRE*/

   ssub_a ss1 (/*AUTOINST*/);
   ssub_b ss2 (/*AUTOINST*/);
endmodule
// Local Variables:
// verilog-library-directories:("." "ssub_a" "ssub_b")
// End:
