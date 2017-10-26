`include "{{module_name}}_sequence_library.sv"
{%-if with_vseq%}
`include "{{module_name}}_virtual_sequence.sv"
{% endif %}
