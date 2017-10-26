##########################################################################################
# Lynx Metrics for PrimeTime Reference Methodology
# Script: metric_reports_pt.tcl
# Version: E-2010.12 (January 10, 2011)
# Copyright (C) 2011 Synopsys, Inc. All rights reserved.
##########################################################################################

redirect $RPT(basename).report_constraint {
  echo "case_analysis_sequential_propagation = $case_analysis_sequential_propagation"
  report_constraint \
    -all_violators \
    -nosplit
}

if { $TEV(vx_enable) } {

  redirect $RPT(basename).report_clock_timing.latency {
    report_clock_timing -type latency -nosplit -variation
  }
  redirect $RPT(basename).report_clock_timing.skew {
    report_clock_timing -type skew -nosplit -variation
  }

} else {

  redirect $RPT(basename).report_clock_timing.latency {
    report_clock_timing -type latency -nosplit
  }
  redirect $RPT(basename).report_clock_timing.skew {
    report_clock_timing -type skew -nosplit
  }

}


## -----------------------------------------------------------------------------
## End of File
## -----------------------------------------------------------------------------
