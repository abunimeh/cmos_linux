/*********************************************************************
 * SYNOPSYS CONFIDENTIAL                                             *
 *                                                                   *
 * This is an unpublished, proprietary work of Synopsys, Inc., and   *
 * is fully protected under copyright and trade secret laws. You may *
 * not view, use, disclose, copy, or distribute this file or any     *
 * information contained herein except pursuant to a valid written   *
 * license from Synopsys.                                            *
 *********************************************************************/

`timescale 1 ns / 10 ps
`define CLK_PERIOD 2


module tb;
  reg clock;

  reg ion, gon, mon;
  reg iiso, giso, miso;
  reg reset;
  reg[31:0] ADDRESS = 32'h00000000;

  wire OUTMWV;
  wire[31:0] DATA;

  reg gprs_save,inst_save,gprs_nrestore,inst_nrestore;

`ifdef UPF
import UPF::*;
`endif
  //instantiation of dut
  ChipTop dut (.MemWriteBus(DATA), .MemWriteValid(OUTMWV), .MemReadBus(ADDRESS), .clock(clock),
               .reset(reset), .inst_on(ion), .inst_iso_in(iiso), .inst_iso_out(~iiso), 
	       .inst_save(inst_save),.inst_nrestore(inst_nrestore),
               .gprs_on(gon), .gprs_iso_in(giso), .gprs_iso_out(~giso), 
	       .gprs_save(gprs_save),.gprs_nrestore(gprs_nrestore),
               .mult_on(mon), .mult_iso_in(miso), .mult_iso_out(~miso) 
              );

`ifdef VPD
  initial
  begin
	$vcdpluspowerenableon;
	$vcdpluspowerstateon;
	$vcdpluson;
  end
`endif

`ifdef UPF
  initial
  begin
	 	supply_on ("VDD", 1.08);
     	supply_on ("VDDI", 1.08);
     	supply_on ("VDDG", 1.08);
     	supply_on ("VDDM", 1.08);
     	supply_on ("VSS", 0.0); 
  end
`endif

  initial
    begin
      inst_save = 0;
      gprs_save = 0;
      inst_nrestore = 1;
      gprs_nrestore = 1;
    end

  // STIM
  initial begin

  // Simulation started with all blocks on
    ion   = 1'b0;
    mon   = 1'b0;
    gon   = 1'b0;
    iiso  = 1'b0;
    giso  = 1'b0;
    miso  = 1'b1;

  // Assert reset to all blocks
    #1  reset = 1'b1;
    #10 reset = 1'b0;

  // Command ref
  // NOOP: 	ADDRESS[31:24] = 8'h30 
  // LOAD: 	ADDRESS[31:24] = 8'h31
  // STORE:	ADDRESS[31:24] = 8'h32,
  // MULT:	ADDRESS[31:24] = 8'h33,
  // ADD:	ADDRESS[31:24] = 8'h34, 
  // MULTX:	ADDRESS[31:24] = 8'h35;

  // Simple test case that loads 6 of the GPRS registers, 
  // retains their values, powers down the GPRS blocks,
  // powers it back up and restores the register values

  // Load data into 6 GPRS registers
    #40 ADDRESS = 32'h3000_0000; //NOOP  H30

    // Load into GPRS_reg0
    #20 ADDRESS = 32'h3100_0000; 	// LOAD CMD
    #4  ADDRESS = 32'h0000_abcd; 	// Data to load
    #8  ADDRESS = 32'h3200_0000;	// Read the reg

    // Load into GPRS_reg1
    #4  ADDRESS = 32'h3110_0000;
    #4  ADDRESS = 32'h0011_1111;
    #8  ADDRESS = 32'h3201_0000; 

    // Load into GPRS_reg2
    #4  ADDRESS = 32'h3120_0000;
    #4  ADDRESS = 32'h0022_2222;
    #8  ADDRESS = 32'h3202_0000;

    // Load into GPRS_reg3
    #4  ADDRESS = 32'h3130_0000;
    #4  ADDRESS = 32'h0033_3333;
    #8  ADDRESS = 32'h3203_0000; 

    // Load into GPRS_reg4
    #4  ADDRESS = 32'h3140_0000;
    #4  ADDRESS = 32'h0044_4444;
    #8  ADDRESS = 32'h3204_0000;

    // Load into GPRS_reg5
    #4  ADDRESS = 32'h3150_0000;
    #4  ADDRESS = 32'h0055_5555;
    #8  ADDRESS = 32'h3205_0000;

    // End of Loads
    #4 ADDRESS = 32'h3000_0000; // NOOP

    // Turn off GPRS block
    #40  giso     = 1'b1; 

    // deassert save signal here
    #40  gprs_save = 1'b1;
    #4   gprs_save = 1'b0;

    #4   gon      = 1'b1;
    #100 gon      = 1'b0;

    #50

   // Assert restore signal here
    #100  gprs_nrestore = 1'b0;
    #10  gprs_nrestore = 1'b1;

    #20 giso = 1'b0;

    // Verify GPRS register values are restored

    $display("\nVerifying restored values\n");

    #4  ADDRESS = 32'h3200_0000;
    #4  ADDRESS = 32'h3201_0000;
    #4  ADDRESS = 32'h3202_0000;
    #4  ADDRESS = 32'h3203_0000;
    #4  ADDRESS = 32'h3204_0000;
    #4  ADDRESS = 32'h3205_0000;

    // End of Loads
    #4 ADDRESS = 32'h3000_0000; // NOOP

    #50
`ifdef UPF
    // Voltage ramp on VDDG to show LS corruption on a protected crossover
    #4 supply_on ("VDDG", 1.0);
    #4 supply_on ("VDDG", 0.9);
    #4 supply_on ("VDDG", 0.8);
    #4 supply_on ("VDDG", 0.7);
    #4 supply_on ("VDDG", 0.6);
    #4 supply_on ("VDDG", 0.7);
    #4 supply_on ("VDDG", 0.8);
    #4 supply_on ("VDDG", 0.9);
    #4 supply_on ("VDDG", 1.0);
    #4 supply_on ("VDDG", 1.08);
`endif 
    // Reset all blocks
    #200   reset   = 1'b1;
    #2   reset   = 1'b0;

    #50

`ifdef UPF
    // Voltage ramp on VDDM to show 30-70 on an unprotected crossover
    #4 supply_on ("VDDM", 1.0);
    #4 supply_on ("VDDM", 0.8);
    #4 supply_on ("VDDM", 0.6);
    #4 supply_on ("VDDM", 0.4);
    #4 supply_on ("VDDM", 0.2);
    #4 supply_on ("VDDM", 0.4);
    #4 supply_on ("VDDM", 0.6);
    #4 supply_on ("VDDM", 0.8);
    #4 supply_on ("VDDM", 1.0);
    #4 supply_on ("VDDM", 1.08);
`endif 
    // Reset all blocks
    #200   reset   = 1'b1;
    #2   reset   = 1'b0;
   
     $display("cpuxos case passed!");
  end

   initial begin                                         
            //$dumpfile("testbench.vcd");                        
            //$dumpvars;                                        
        end      
 

  // CLOCK 
  initial begin
    clock=0;
    forever #(`CLK_PERIOD) clock=~clock;
  end

  // FINISH SIMULATION
  initial begin
    #5000 $finish;
  end

   always @(posedge clock) begin
     if (OUTMWV == 1'b1)
        $display("%t Reading %h from GPRS reg %h", $time, DATA, DATA[23:20]);
    end

endmodule
