##########################################################################################
# Lynx Metrics for Design Compiler Reference Methodology
# Script: metric_reports_dc.tcl
# Version: E-2010.12 (January 10, 2011)
# Copyright (C) 2011 Synopsys, Inc. All rights reserved.
##########################################################################################

redirect $SEV(rpt_dir)/dc.report_units {
  report_units
}

redirect $SEV(rpt_dir)/dc.report_qor {
  report_qor
}

redirect $SEV(rpt_dir)/dc.report_threshold_voltage_group {
  report_threshold_voltage_group
}

redirect $SEV(rpt_dir)/dc.report_power {
  report_power -nosplit
}

if { [shell_is_in_topographical_mode] } {
  redirect $SEV(rpt_dir)/dc.report_congestion {
    report_congestion
  }
}

## -----------------------------------------------------------------------------
## End of File
## -----------------------------------------------------------------------------
