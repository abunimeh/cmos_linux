#!/:usr/bin/tclsh

{%-for base_key, base_value in base_arg_dic|dictsort%}
set {{base_key}} {{base_value}}
{%-endfor%}

{%-for set_key, set_value in set_arg_dic|dictsort%}
{%-if set_key=='rtl_files' %}
set {{set_key}} {\ 
{{set_value}} 
}
{%-else%}
set {{set_key}} "{{set_value}}"
{%-endif%}
{%-endfor%}
