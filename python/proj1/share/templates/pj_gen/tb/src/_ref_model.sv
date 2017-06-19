`ifndef {{module_name}}_REF_MODEL__SV
`define {{module_name}}_REF_MODEL__SV

//-----------------------------------------------------------------------------
//
// CLASS: {{module_name}}_ref_model
//
//
//-----------------------------------------------------------------------------
class {{module_name}}_ref_model extends uvm_component;
    
    //ToDo: Change the input and output transaction names below.
{%-for a_name in agt_name_lst%}
    typedef {{module_name}}_{{a_name}}_itrans {{a_name}}_itrans;
    typedef {{module_name}}_{{a_name}}_otrans {{a_name}}_otrans;
    uvm_nonblocking_get_port #({{a_name}}_itrans) {{a_name}}_input_port;
    uvm_analysis_port #({{a_name}}_otrans) {{a_name}}_output_port;
{% endfor %}
    `uvm_component_utils({{module_name}}_ref_model)
{%-for a_name in agt_name_lst%}
    {{a_name}}_itrans {{a_name}}_itr;
    {{a_name}}_otrans {{a_name}}_otr;
{% endfor %}
    // ***Opetion for integration***
    // ToDo: Instantiate sub-models here. 
    // Example: 
    // sub_model submdl;

    bit integration = 0;
    bit clock;
    bit flag_reset;

    // ToDo: Put internal variables here.
    // Example:
    // int counter;

    extern function new(string name = "{{module_name}}_ref_model", uvm_component parent = null);
    extern virtual function void build_phase(uvm_phase phase);
    extern virtual task reset_phase(uvm_phase phase);
    extern virtual task post_reset_phase(uvm_phase phase);
    extern virtual task run_phase(uvm_phase phase);

    extern virtual task automatic clk_gen();
    extern virtual function automatic void get_itr();
    extern virtual function automatic void write_otr();
    extern virtual function automatic void run_comb(byte equal_times = 2);
    extern virtual function automatic void run_seq();
    extern virtual function automatic void make_itr();
    extern virtual function automatic void make_otr();
endclass:{{module_name}}_ref_model

// Function: new
//
// Create the internal components.
function {{module_name}}_ref_model::new(string name = "{{module_name}}_ref_model", uvm_component parent);
    super.new(name,parent);
{%-for a_name in agt_name_lst%}
    {{a_name}}_itr = new();
    {{a_name}}_otr = new();
{% endfor %}
    // ***Opetion for integration***
    // submdl = new("submdl", this);
endfunction: new

// Function: build_phase
//
// Create and configure testbench structure.
function void {{module_name}}_ref_model::build_phase(uvm_phase phase);
    super.build_phase(phase);
    if(!integration)begin
{%-for a_name in agt_name_lst%}
        {{a_name}}_input_port  = new("{{a_name}}_input_port" , this);
        {{a_name}}_output_port = new("{{a_name}}_output_port", this);
{% endfor %}
    end
    // ***Opetion for integration***
    // submdl.integration  = 1;
endfunction: build_phase

// Task: reset_phase
//
// Reset the intermediate variables and set the flag_reset to 1. 
task automatic {{module_name}}_ref_model::reset_phase(uvm_phase phase);
    super.reset_phase(phase);
    flag_reset = 1; // assert the reset flag
    // ToDo: Reset internal variables here.
    // Example:
    // counter = 0;
endtask: reset_phase

// Task: post_reset_phase
//
// Set the flag_reset to 0. 
task automatic {{module_name}}_ref_model::post_reset_phase(uvm_phase phase);
    super.post_reset_phase(phase);
    phase.raise_objection(this);
    flag_reset = 0; // deassert the reset flag after reset_phase
    phase.drop_objection(this);
endtask: post_reset_phase

// Task: run_phase
//
// Receive input packet from imonitor & send output packet to scoreboard.
task automatic {{module_name}}_ref_model::run_phase(uvm_phase phase);
    super.run_phase(phase);
    if(!integration)begin
        fork
            clk_gen(); // Pseudo clock generation. 
            forever begin
                @(posedge clock);   // Wait the positive edge of pseudo clock.
                get_itr();          // Get the input transaction.
                run_comb();         // Running the combinational logics.
                if (!flag_reset)    // At reset_phase, the sequential logics will not be executed.
                run_seq();          // Running the sequential logics.
                write_otr();        // Send the output transaction.
            end
        join
    end
endtask: run_phase

// Task :clk_gen
//
// Pseudo clock generation, period is transfered from testbench top. 
task automatic {{module_name}}_ref_model::clk_gen();
    clock = 0;
    //forever #(sim_cycle/2) clock = ~clock;
endtask // clk_gen

// Function: get_itr
//
// Get input transaction from input port. 
function automatic void {{module_name}}_ref_model::get_itr();
{%-for a_name in agt_name_lst%}
    if(!{{a_name}}_input_port.try_get({{a_name}}_itr)) begin // try getting the input transaction from imonitor, return 1 if got.
        // ToDo: If couldn't get the input transaction, disable the valid signals in itrans.
        // Example: 
        // itr.valid = 0;
    end
    else begin
       `uvm_info("{{module_name}}_ref_model", "Model received a transaction from {{a_name}} imon.", UVM_HIGH) //print the successful information
   end
{% endfor %}
endfunction: get_itr

// Function: write_otr
//
// Export the output transaction to output port.
function automatic void {{module_name}}_ref_model::write_otr();
    // ToDo: Use the same export condition as oMonitor.
    // Example: 
    // if(otr.valid) 
    begin
{%-for a_name in agt_name_lst%}
        {{a_name}}_output_port.write({{a_name}}_otr);
{% endfor %}
    end
endfunction: write_otr

// Function: run_comb
//
// Execute all of the combinational logics.
// Repeat for multiple cycles until the logics become stable.
// Argument: equal_times - required equal times of sub-model inputs to make sure it become stable.
function automatic void {{module_name}}_ref_model::run_comb(byte equal_times = 2); // ToDo: change the equal_times as needed.
    // ToDo: Put the combinational logic here.
    // Example: 
    // otr.valid = (counter<10) ? 1 : 0;


    // ***Option for integration***
    // ToDo: Put the sub-models combinational function here with proper parameters.
    // Template: 
    // (start code)
    // parameter model_num = 1; // ToDo: Change the number as the amount of sub-models.
    // byte flag_stable[1:model_num]; // flags for each sub-model to store the accumulated equal times
    // mdl_itrans mdl_itr_old; // instantiate the input transaction to store its last value.
    // // use comparer policy to disable printing information when compare mismatch
    // uvm_comparer cmp_policy;
    // cmp_policy = new;
    // cmp_policy.show_max = 0;
    // // start running sub-models combinational logic, 
    // // and make comparison to judge whether inputs become stable.
    // do begin
    //     make_itr(); // see detail in function
    //     if(flag_stable[1]!=(equal_times)) begin // if the stable requirement not meet, run comparison
    //         if(submdl.itr.compare(mdl_itr_old, cmp_policy)) begin // if current inputs is the same as last one, flag added. 
    //             flag_stable[1] = (flag_stable[1] < equal_times) ? flag_stable[1] + 1 : flag_stable[1];
    //         end else begin // if current inputs is different to last one, clear flag and run comb logic
    //             flag_stable[1] = 0; 
    //             submdl.run_comb(); 
    //             mdl_itr_old = new("mdl_itr_old"); 
    //             mdl_itr_old.copy(submdl.itr); 
    //         end 
    //     end
    // end
    // while(flag_stable.sum() != (equal_times)*model_num); // jump out the loop, if all sub-models inputs stable
    // (end)
endfunction: run_comb

// Function: run_seq
//
// Execute all of the sequential logics.
function automatic void {{module_name}}_ref_model::run_seq();
    // ToDo: Put the sequential logic here.
    // Example:
    // if(itr.valid) 
    // counter = counter + 1;

    // ***Opetion for integration***
    // ToDo: Put the sub-models sequential function here with proper execute condition.
    // Example: 
    // submdl.run_seq();
    // make_otr(); // see detail in function
endfunction:run_seq

// ***Option for integration***
// Function: make_itr
//
// Generate the intermediate input transactions in sub-models
function automatic void {{module_name}}_ref_model::make_itr();
    // ToDo: Connect the super-model input transaction to sub-model input transaction.
    // Example:
    // submdl.itr.valid = itr.valid;
endfunction: make_itr

// ***Option for integration***
// Function: make_otr
//
// Generate the output transactions in this model.
function automatic void {{module_name}}_ref_model::make_otr(); 
    // ToDo: Connect the sub-models internal transaction to super-model output transaction.
    // Example:
    // otr.valid = submdl.otr.valid;
endfunction: make_otr

`endif // {{module_name}}_REF_MODEL__SV
