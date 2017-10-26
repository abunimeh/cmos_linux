package reset_config; 
   `timescale 1ns/100ps 
   
   parameter RESET_PENDING_CYCLE  = 0;
   parameter RESET_PENDING_TIME   = 50;
   parameter RESET_HOLD_CYCLE     = 10;
   parameter SYNC_CLK             = 0;
   parameter RESET_ENABLE         = 0;
   parameter RESET_GEN_INIT_VALUE = 1;
endpackage: reset_config

