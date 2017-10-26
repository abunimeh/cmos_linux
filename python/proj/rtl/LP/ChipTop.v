/*********************************************************************
 * SYNOPSYS CONFIDENTIAL                                             *
 *                                                                   *
 * This is an unpublished, proprietary work of Synopsys, Inc., and   *
 * is fully protected under copyright and trade secret laws. You may *
 * not view, use, disclose, copy, or distribute this file or any     *
 * information contained herein except pursuant to a valid written   *
 * license from Synopsys.                                            *
 *********************************************************************/

module ChipTop (MemWriteBus, MemWriteValid, MemReadBus, clock, reset,
                inst_on, inst_iso_in, inst_iso_out,
                gprs_on, gprs_iso_in, gprs_iso_out,
                mult_on, mult_iso_in, mult_iso_out,
                inst_save, inst_nrestore, gprs_save, gprs_nrestore
               );

   input  [31:0]     MemReadBus;             // Memory Read Bus
   output [31:0]     MemWriteBus;            // Memory Write Bus
   output 	     MemWriteValid;          // Memory Write Bus Contains Data
   input             clock;                  // System Clock
   input 	     reset;

   input 	     inst_on;                // switch 
   input 	     inst_iso_in;            // iso
   input 	     inst_iso_out;           // iso
   input 	     inst_save;
   input 	     inst_nrestore;
   wire              inst_ack;

   input 	     gprs_on;                // switch 
   input 	     gprs_iso_in;            // iso
   input 	     gprs_iso_out;           // iso
   input 	     gprs_save;
   input 	     gprs_nrestore;
   wire              gprs_ack;
  
   input 	     mult_iso_in;            // iso
   input 	     mult_iso_out;           // iso
   input 	     mult_on;                // switch 
   wire              mult_ack;

   wire genpp_on;
   wire genpp_ack;

   wire   [31:0]     MemReadBus;             // Memory Read Bus
   wire   [31:0]     MemWriteBus;            // Memory Write Bus
   wire 	     MemWriteValid;          // Memory Write Bus Contains Data
   wire   [31:0]     A, B, C;                // Data Buses
   wire   [3:0]      RdAdrA, RdAdrB, RdAdrC; // Read Addresses
   wire   [3:0]      WrtAdrX, WrtAdrY;       // Write Address
   wire              WrtEnbX, WrtEnbY;       // Write Enables
   wire   [31:0]     Product;                // Multiplier output
   wire   [31:0]     iso_Product;            // Multiplier output
   wire 	     Ovfl;                   // Multiplier Overflow

   
   wire [31:0] iso_MemReadBus_to_inst;
   wire        iso_clock_to_inst;
   wire [31:0] iso_MemReadBus_to_gprs;
   wire        iso_clock_to_gprs;
   wire [3:0]  iso_RdAdrA_to_gprs;
   wire [3:0]  iso_RdAdrB_to_gprs;
   wire [3:0]  iso_RdAdrC_to_gprs;
   wire [3:0]  iso_WrtAdrX_to_gprs;
   wire [3:0]  iso_WrtAdrY_to_gprs;
   wire        iso_WrtEnbX_to_gprs;
   wire        iso_WrtEnbY_to_gprs;
   wire [31:0] iso_Product_to_gprs;

             
   assign  MemWriteBus = A;               // Drive A to Write Bus
   wire    GENPP_ao = 1'b1;

//- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
// Instruction Decoder 
//- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
InstructionDecoder InstDecode(MemReadBus,RdAdrA,RdAdrB,RdAdrC,
                              WrtAdrX,WrtEnbX,
                              WrtAdrY,WrtEnbY,
                              MemWriteValid, clock, reset);
   
//- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
// 16 General Purpose Registers
//- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
GeneralPurposeRegisters  GPRs(A,B,C,RdAdrA,RdAdrB,RdAdrC,
			      WrtAdrX,WrtEnbX,WrtAdrY,WrtEnbY,
                              MemReadBus,Product,
                              clock, reset);
   

//- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
// 32 x 32 Signed Multiplier
//- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Mult_32x32 Multiplier(Ovfl,Product,A,B,C,clock,mult_iso_in, reset);

endmodule
