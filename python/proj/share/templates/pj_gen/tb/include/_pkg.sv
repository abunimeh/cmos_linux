
package {{module_name}}_pkg;
import uvm_pkg::*;
`include "clock_pkg.incl"
`include "reset_pkg.incl"
{%-for a_name in agt_name_lst%}
`include "{{module_name}}_{{a_name}}_itrans.sv"
`include "{{module_name}}_{{a_name}}_otrans.sv"
`include "{{module_name}}_{{a_name}}_seqr.sv"
`include "{{module_name}}_{{a_name}}_drv.sv"
`include "{{module_name}}_{{a_name}}_mon.sv"
`include "{{module_name}}_{{a_name}}_agt.sv"
{% endfor %}
`include "{{module_name}}_sequence_library.sv"
{%-if with_vseq%}
`include "{{module_name}}_vseqr.sv"
{% endif %}
`include "{{module_name}}_reset_sequence_library.sv"
`include "{{module_name}}_clock_sequence_library.sv"
`include "{{module_name}}_cfg.sv"
`include "{{module_name}}_cov.sv"
`include "{{module_name}}_ref_model.sv"
`include "{{module_name}}_scb.sv"
`include "{{module_name}}_env.sv"


//`include "{{module_name}}_base_test.sv"

//Sequences
`include "{{module_name}}_seqs.svh"
//Test_cases
`include "{{module_name}}_tc.svh"

endpackage
