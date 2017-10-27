module top (/*AUTOARG*/);
   input  top__sub_a__s1;
   input  top__ssub_a__s2;
   input  top__ssub_b__s3;
   input [3:0] top__sub_a__s2;
   input [1:0] top__sub_a__ss1ss1ss1;
   output sub_b__top__s1;

   /*AUTOREG*/
   /*AUTOWIRE*/
   
   always @ (/*AUTOSENSE*/) begin
      o1 = i1 | i2 | inter1;
   end

   /* sub_a AUTO_TEMPLATE (
    .top__sub_a__s2 (top__sub_a__s2[@"(+ (* (- @ 1) 2) 1)":@"(* (- @ 1) 2)"]),
    );*/
   
   sub_a #(/*AUTOINSTPARAM*/) sa1 (// Custom Connections
                                   .top__sub_a__ss1 (top__sub_a__ss1ss1ss1),
                                   /*AUTOINST*/);
   sub_b #(/*AUTOINSTPARAM*/) sb1 (// Custom Connections
                                   .ssub_b__sub_b__s1_temp (ssub_b__sub_b__s1),
                                   /*AUTOINST*/);
endmodule
// Local Variables:
// verilog-library-directories:("." "sub_a" "sub_b")
// End:
