##########################################################################################
# Lynx Metrics for IC Compiler Reference Methodology
# Script: metric_reports_icc.tcl
# Version: E-2010.12 (January 10, 2011)
# Copyright (C) 2011 Synopsys, Inc. All rights reserved.
##########################################################################################

redirect -file $SEV(rpt_dir)/icc.report_units {
  report_units
}

redirect -file $SEV(rpt_dir)/icc.report_qor {
  report_qor
}

redirect -file $SEV(rpt_dir)/icc.report_threshold_voltage_group {
  report_threshold_voltage_group
}

redirect -file $SEV(rpt_dir)/icc.report_power {
  if { [llength [all_active_scenarios]] > 0 } {
    report_power -scenario [all_active_scenarios]
  } else {
    report_power -nosplit
  }
}

redirect -file $SEV(rpt_dir)/icc.report_design_physical {
  report_design_physical -all -verbose
}

## -----------------------------------------------------------------------------
## End of File
## -----------------------------------------------------------------------------
