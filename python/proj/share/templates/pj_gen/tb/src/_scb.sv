

`ifndef {{module_name}}_SCB__SV
`define {{module_name}}_SCB__SV


class {{module_name}}_scb extends uvm_scoreboard;
{%-for a_name in agt_name_lst%}
    {{module_name}}_{{a_name}}_otrans get_{{a_name}}_exp, get_{{a_name}}_act,trans_{{a_name}}_exp,trans_{{a_name}}_act;
{% endfor %}
    bit result;
{%-for a_name in agt_name_lst%}
    {{module_name}}_{{a_name}}_otrans  exp_{{a_name}}_queue[$]; 
    {{module_name}}_{{a_name}}_otrans  act_{{a_name}}_queue[$]; 
{% endfor %}
{%-for a_name in agt_name_lst%}
    uvm_blocking_get_port #({{module_name}}_{{a_name}}_otrans) exp_{{a_name}}_port;
    uvm_blocking_get_port #({{module_name}}_{{a_name}}_otrans) act_{{a_name}}_port;
{% endfor %}

    //string golden_result;
    //integer file;
    //int scanf;
    //bit [???:0] all_bytes;

    `uvm_component_utils({{module_name}}_scb)
	extern function new(string name = "{{module_name}}_scb",uvm_component parent = null); 
	extern virtual function void  build_phase (uvm_phase phase);
	extern virtual task  run_phase(uvm_phase phase);
	extern virtual function void  report_phase(uvm_phase phase);
endclass: {{module_name}}_scb


function {{module_name}}_scb::new(string name = "{{module_name}}_scb",uvm_component parent);
    super.new(name,parent);
endfunction: new


function void {{module_name}}_scb::build_phase(uvm_phase phase);
    super.build_phase(phase);
{%-for a_name in agt_name_lst%}
    exp_{{a_name}}_port = new("exp_{{a_name}}_port", this);
    act_{{a_name}}_port = new("act_{{a_name}}_port", this);
{% endfor %}

    //uvm_config_db #(string)::get(this,"","golden_result",golden_result);
endfunction:build_phase


task {{module_name}}_scb::run_phase(uvm_phase phase);
    super.run_phase(phase);
    /*
    //ToDo: processing golden file to pkt
    //if c modle or golden reference could be got
    begin: length_file
        file = $fopen(golden_result,"r"); 
        if(file == 0) begin
            disable length_file;
            $display("Open result file failure!");
            $finish;
        end else begin 
            $display("Open result file succeed: %s", golden_result);
        end 

        while(!$feof(file)) begin
            get_{{a_name}}_exp = new();
            scanf = $fscanf(file,"%h", all_bytes); 
//ToDo: get expected pkt here
            //get_{{a_name}}_exp.xx = all_bytes[319:300]; 

            exp_{{a_name}}_queue.push_back(get_{{a_name}}_exp);
        end
    end
    */
    fork
{%-for a_name in agt_name_lst%}
        forever begin
            exp_{{a_name}}_port.get(get_{{a_name}}_exp);
            exp_{{a_name}}_queue.push_back(get_{{a_name}}_exp);
        end
{% endfor %}
        
{%-for a_name in agt_name_lst%}
        forever begin
            act_{{a_name}}_port.get(get_{{a_name}}_act);
            act_{{a_name}}_queue.push_back(get_{{a_name}}_act);
          `uvm_info("{{module_name}}_SCB","Scoreboard get mon Transaction",UVM_HIGH)
          `uvm_info("{{module_name}}_SCB", get_{{a_name}}_act.sprint(),UVM_HIGH)
         end 
{% endfor %}
        

{%-for a_name in agt_name_lst%}
         forever begin
            wait(exp_{{a_name}}_queue.size() > 0 && act_{{a_name}}_queue.size() > 0) begin
                trans_{{a_name}}_exp = exp_{{a_name}}_queue.pop_front();
                trans_{{a_name}}_act = act_{{a_name}}_queue.pop_front();
                result = trans_{{a_name}}_act.compare(trans_{{a_name}}_exp);
                if (result) begin
                    //ToDo: Deal if packet match
                    `uvm_info("{{module_name}}_SCB","\n{{a_name}} Transaction Compare match ^_^",UVM_HIGH);
                end
                else begin
                    //ToDo: Deal if packet mismatch
                    `uvm_error("{{module_name}}_SCB","\n{{a_name}} Transaction Compare Mismatch !!!");
                    `uvm_info("{{module_name}}_SCB", $sformatf("\n{{a_name}} model\n%s", trans_{{a_name}}_exp.sprint()),UVM_LOW)
                    `uvm_info("{{module_name}}_SCB", $sformatf("\n{{a_name}} DUT\n%s", trans_{{a_name}}_act.sprint()),UVM_LOW)
                 end
            end
         end
{% endfor %}
    join
endtask: run_phase

function void {{module_name}}_scb::report_phase(uvm_phase phase);
    super.report_phase(phase);
    //ToDo: Add result report here

endfunction:report_phase


`endif // {{module_name}}_SCB__SV
