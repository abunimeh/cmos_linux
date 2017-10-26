#!/:usr/bin/tclsh

source -echo -verbose {{dc_dic.dc__tcl.DcTcl_DIR}}/set_args.tcl

#################################################################################
# Design Compiler Top-Down Reference Methodology Setup
# Script: dc_setup.tcl
# Version: D-2010.03 (March 29, 2010)
# Copyright (C) 2007-2010 Synopsys, Inc. All rights reserved.
#################################################################################

if {$synopsys_program_name == "dc_shell"}  {

  set_app_var alib_library_analysis_path .

  # Add any additional DC variables needed here
}

set RTL_SOURCE_FILES { }
foreach rtl_file $rtl_files {
set full_file_path $rtl_file
set RTL_SOURCE_FILES [concat $RTL_SOURCE_FILES $full_file_path ]
}


# The following variables are used by scripts in dc_scripts to direct the location
# of the output files

#set REPORTS_DIR "reports"
#set RESULTS_DIR "results"
#file mkdir ${REPORTS_DIR}
#file mkdir ${RESULTS_DIR}

set report_default_significant_digits 4

# Milkyway variable settings
# Make sure to define the following Milkyway library variables
# mw_logic1_net, mw_logic0_net and mw_design_library are needed by write_milkyway

set_app_var mw_logic1_net ${MW_POWER_NET}
set_app_var mw_logic0_net ${MW_GROUND_NET}

set mw_reference_library ${MW_REFERENCE_LIB_DIRS}
set mw_design_library ${DCRM_MW_LIBRARY_NAME}

set mw_site_name_mapping [list CORE unit Core unit core unit]
if {$synopsys_program_name == "dc_shell"}  {


#  set_app_var target_library "gtech.db and_or.db class.db class_fpga.db lsi_10k.db lsi_7k.db lsi_9k.db lsi_lsc15.db nonlinear.db power2_sample.db power_sample.db tc6a_cbacore.db tc6a_cbamc.db vhdlmacro.db"
set_app_var search_path ". ${ADDITIONAL_SEARCH_PATH} $search_path"
set_app_var target_library "{{dc_dic.dc_setup__tcl.target_library}}"
set_app_var synthetic_library "{{dc_dic.dc_setup__tcl.synthetic_library}}"
set_app_var link_library "* $target_library $synthetic_library {{dc_dic.dc_setup__tcl.link_library}}"
  
  foreach {max_library min_library} $MIN_LIBRARY_FILES {
    set_min_library $max_library -min_version $min_library
  }

  if {[shell_is_in_topographical_mode]} {

    # Only create new Milkyway design library if it doesn't already exist
    if {![file isdirectory $mw_design_library ]} {
      create_mw_lib   -technology $TECH_FILE \
                      -mw_reference_library $mw_reference_library \
                      $mw_design_library
    } else {
      # If Milkyway design library already exists, ensure that it is consistent with specified Milkyway reference libraries
      set_mw_lib_reference $mw_design_library -mw_reference_library $mw_reference_library
    }

    open_mw_lib     $mw_design_library

    check_library

    set_tlu_plus_files -max_tluplus $TLUPLUS_MAX_FILE \
                       -min_tluplus $TLUPLUS_MIN_FILE \
                       -tech2itf_map $MAP_FILE

    check_tlu_plus_files

  }

  #################################################################################
  # Library Modifications
  #
  # Apply library modifications here after the libraries are loaded.
  #################################################################################

  if {[file exists [which ${LIBRARY_DONT_USE_FILE}]]} {
    source -echo -verbose ${LIBRARY_DONT_USE_FILE}
  }
}
