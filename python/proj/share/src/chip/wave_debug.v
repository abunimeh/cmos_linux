
// Generate VCD+ waveform with WAVE= option
`timescale 1ns/10ps
`ifdef WAVE
module wave_debug;
  initial begin
    `ifdef USE_WAVE_ON_TIME
       # `WAVE_ON_TIME ;
    `endif
    $vcdpluson();
	$vcdplusdeltacycleon();
	//$vcdplusmemon(test_top.dut.....);
    `ifdef USE_WAVE_OFF_TIME
       # `WAVE_OFF_TIME ;
       $vcdplusoff;
    `endif
  end
endmodule
`endif


`ifdef DUMP 
`ifdef SAIF_ON
module saif_wave;
initial begin
    `ifdef USE_WAVE_ON_TIME
    #`WAVE_ON_TIME
    `endif
    $display("%m:start dump vcd file at %0t",$time);
    //$dumpvars(1,test_top.DUT....);
    $dumpvars();
    $set_gate_level_monitoring("rtl_on");
    $set_toggle_region("test_top.DUT");
    $toggle_start;
    `ifdef USE_WAVE_OFF_TIME
    #`WAVE_OFF_TIME
    `endif
    $dumpoff;
    $toggle_stop;
    $toggle_report("test.saif",1.0e-9,"test_top.DUT");
    $display("%m:end dump vcd file at %0t",$time);
    $finish;
end
endmodule

`else
module wave_debug;
initial begin
    `ifdef USE_WAVE_ON_TIME
    #`WAVE_ON_TIME
    `endif
    $display("%m:start dump vcd file at %0t",$time);
    //$dumpvars(1,test_top.DUT...,test_top.DUT...);
    //$dumpvars(1,test_top.DUT...);
    $dumpvars();
    `ifdef USE_WAVE_OFF_TIME
    #`WAVE_OFF_TIME
    `endif
    $display("%m:end dump vcd file at %0t",$time);
    $dumpoff;
end
endmodule
`endif
`endif

// Generate Novas waveform 
// NOTE-- This is not controlled via the WAVES= option.  Instead use the VCS_COMP_ARGS
`ifdef NOVAS

`ifdef SAIF_ON
module saif_wave;
    initial begin


    `ifdef USE_WAVE_ON_TIME
       # `WAVE_ON_TIME ;
    `endif
     $display("-----------dump saif and fsdb wave begin------------%t",$time);
           //$dumpvars;
          // $set_toggle_region("test_top.DUT.synthesis_unit....");
           $set_gate_level_monitoring("rtl_on");
           $set_toggle_region("test_top.DUT");

           $toggle_start;

	`ifdef wavesplit
		$fsdbAutoSwitchDumpfile(500,"./waves/cpu_split.fsdb", 10);
        	$fsdbDumpvars;
	`else
		`ifdef MODULELIST
		    $fsdbDumpvarsToFile("./module.list");
		`else
            $fsdbDumpvars;
			//$fsdbDumpvars(1,test_top.DUT...);
		`endif
	 `endif
	`ifdef ASSERT_ON
	  $fsdbDumpSVA(0,test_top);
    `endif



      //#900000;
      //
      //
    `ifdef USE_WAVE_OFF_TIME
       # `WAVE_OFF_TIME ;
    `endif
           $fsdbDumpoff;       
           $toggle_stop;
           $toggle_report("test.saif",1.0e-9,"test_top.DUT");

     $display("-----------dump saif and fsdb wave end------------%t",$time);
	 $finish;
     end
 endmodule  

`else
module novas_wave_debug;
  initial begin
    `ifdef USE_WAVE_ON_TIME
       # `WAVE_ON_TIME ;
    `endif

     $display("-----------dump fsdb wave begin------------%t",$time);

	`ifdef wavesplit
		$fsdbAutoSwitchDumpfile(500,"./waves/cpu_split.fsdb", 10);
        	$fsdbDumpvars;
	`else
		`ifdef SILOTI
		$fsdbDumpvarsToFile("./fullchip.list");
		`else
		    `ifdef MODULELIST
				$display("dump fsdb as module.list");
		        $fsdbDumpvarsToFile("./module.list");
		    `else
    	    	$fsdbDumpvars;
	        `endif
		`endif
	 `endif
	 `ifdef DUMPEEPROM
	//$fsdbDumpMem(test_top.DUT.u_dualcard_logic_and_mem.trom1_unit.mem);
      $fsdbDumpMem(`EE_MEM, , ,1000);
      $fsdbDumpMem(`EEOTP_MEM, , ,1000);
	`endif
	`ifdef ASSERT_ON
	  $fsdbDumpSVA(0,test_top);
    `endif
    `ifdef USE_WAVE_OFF_TIME
       # `WAVE_OFF_TIME ;
       $fsdbDumpoff;
    `endif

     $display("-----------dump fsdb wave end------------%t",$time);

  end
endmodule
`endif
`endif

//################################################################################
//# End of file
//################################################################################
