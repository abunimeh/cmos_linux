`include "clock_if.sv"
`include "reset_if.sv"
{%-for a_name in agt_name_lst%}
`include "{{module_name}}_{{a_name}}_if.sv"
{% endfor %}
