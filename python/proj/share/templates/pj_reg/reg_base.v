///////////////////////////////////////////////////////// 
//文件名称：{{module_name}}模块     
//模块名称：{{module_name}}
//禁止修改，该文件由pj reg自动生成
////////////////////////////////////////////////////////////

module {{module_name}} 
(
//======全局=========
 input  wire shiz
,input  wire fuw_d
//======中间结点============
,input  wire [15:0] zjjd__yjd__shuj
,output reg  [15:0] yjd__zjjd__shuj 
{% set mod_to_mod = module_name.split("_")[0] + "__" + module_name -%}
{% set mod_to_mod_reverse = module_name + "__" + module_name.split("_")[0] -%}
//======所在单元==========
{% block io_def -%}
{% for reg, parameters in data.items() -%}
{% for bits, items in parameters.fields.items() -%}
{% set definition = "_"+ items.definition if items.definition -%}
//-----{{reg}}{{definition}}-----
{% if parameters["ST/MT"] == "MT" -%}
{% for i in range(2) -%}
{% if 'hrw' not in items or items.hrw == 'NA' or items.hrw == 'rw' -%}
,input  wire  {{mod_to_mod}}__{{reg}}{{definition}}{{i}}_xsn   //{{reg}}{{definition}}线程{{i}},写使能
,input  wire {{items.interval}} {{mod_to_mod}}__{{reg}}{{definition}}{{i}}_sj    //{{reg}}{{definition}}线程{{i}},所在单元要写的值
,output wire {{items.interval}} {{mod_to_mod_reverse}}__{{reg}}{{definition}}{{i}}_sj    //{{reg}}{{definition}}线程{{i}},CR当前的值
{% elif items.hrw == "r" -%}
,output wire {{items.interval}} {{mod_to_mod_reverse}}__{{reg}}{{definition}}{{i}}_sj    //{{reg}}{{definition}}线程{{i}},CR当前的值
{% elif items.hrw == "w" -%}
,input  wire  {{mod_to_mod}}__{{reg}}{{definition}}{{i}}_xsn   //{{reg}}{{definition}}线程{{i}},写使能
,input  wire {{items.interval}} {{mod_to_mod}}__{{reg}}{{definition}}{{i}}_sj    //{{reg}}{{definition}}线程{{i}},所在单元要写的值
{% endif -%}
{% endfor %}{% else -%}
{% if 'hrw' not in items or items.hrw == 'NA' or items.hrw == 'rw' -%}
,input  wire  {{mod_to_mod}}__{{reg}}{{definition}}_xsn    //{{reg}}{{definition}},写使能  
,input  wire {{items.interval}} {{mod_to_mod}}__{{reg}}{{definition}}_sj     //{{reg}}{{definition}},所在单元要写的值 
,output wire {{items.interval}} {{mod_to_mod_reverse}}__{{reg}}{{definition}}_sj     //{{reg}}{{definition}},CR当前的值
{% elif items.hrw == "r" -%}
,output wire {{items.interval}} {{mod_to_mod_reverse}}__{{reg}}{{definition}}_sj     //{{reg}}{{definition}},CR当前的值
{% elif items.hrw == "w" -%}
,input  wire  {{mod_to_mod}}__{{reg}}{{definition}}_xsn    //{{reg}}{{definition}},写使能  
,input  wire {{items.interval}} {{mod_to_mod}}__{{reg}}{{definition}}_sj     //{{reg}}{{definition}},所在单元要写的值 
{% endif -%}
{% endif -%}
{% endfor -%}
{% endfor -%}
{% endblock io_def -%}
);


{% set prefix = ["yjdkz", "kzjcq"] %}
reg  [15:0] zjjd_xie_shuj;
wire [15:0] zjjd_du_sj;
{% block wire_def %}
{% for reg, parameters in data.items() -%}
{% for bits, items in parameters.fields.items() -%}
{% set definition = "_"+ items.definition if items.definition -%}
wire [15:0] {{reg}}{{definition}}_du_shuj;
{% if parameters["ST/MT"] == "MT" -%}
{% for i in range(2) -%}
wire  {{prefix[0]}}__{{prefix[1]}}__{{reg}}{{definition}}{{i}}_xsn;   
wire {{items.interval}} {{prefix[0]}}__{{prefix[1]}}__{{reg}}{{definition}}{{i}}_sj;
wire {{items.interval}} {{prefix[1]}}__{{prefix[0]}}__{{reg}}{{definition}}{{i}}_sj;
{% endfor %}
{% else -%}
wire  {{prefix[0]}}__{{prefix[1]}}__{{reg}}{{definition}}_xsn;
wire {{items.interval}} {{prefix[0]}}__{{prefix[1]}}__{{reg}}{{definition}}_sj;
wire {{items.interval}} {{prefix[1]}}__{{prefix[0]}}__{{reg}}{{definition}}_sj;
{% endif -%}
{% endfor -%}
{% endfor -%}
{% endblock wire_def -%}

always@(posedge shiz or negedge fuw_d)
begin
    if(~fuw_d)
        zjjd_xie_shuj <= 16'b0;
    else
        zjjd_xie_shuj <= zjjd__yjd__shuj;
end

{% block instances -%}
{% for reg, parameters in data.items() -%}
{% for bits, items in parameters.fields.items() -%}
{% set definition = "_"+ items.definition if items.definition -%}
{% set reg_def = reg + definition if definition else reg -%}
{% set ds = "s" if parameters["ST/MT"] == "MT" else "d" -%}
{% set bits = parameters["32bit/64bit"].replace("bit", "") if items.interval_type == "kbwk" else "" -%}
//========={{reg_def}}=================
{{prefix[0]}}_{{ds}}{{bits}}{{items.interval_type}}#(
 {% if parameters["32bit/64bit"] == "64bit" -%}
 .G_GDZ ({{parameters.hglobal_address}}),
 .G_DDZ ({{parameters.global_address}}),
 .L_GDZ ({{parameters.hlocal_address}}),
 .L_DDZ ({{parameters.local_address}})
 {%- else -%}
 .G_DIZ ({{parameters.global_address}}),
 .L_DIZ ({{parameters.local_address}})
 {%- endif -%}
 {% if items.interval_type == "kbwk"-%}
 ,
 .KAISW({{items.st_ed[1]}}),
 .JIESW({{items.st_ed[0]}}),
 .SZ({{items.st_ed[0]-items.st_ed[1] +1 }})
 {% endif -%}
)u_{{prefix[0]}}_{{reg_def}}(
    .shiz               (shiz                       ),  
    .fuw_d              (fuw_d                      ), 
    .zjjd__{{prefix[0]}}__shuj  (zjjd_xie_shuj              ), //根结点来的数据
    .{{prefix[0]}}__zjjd__shuj  ({{reg_def}}_du_shuj             ), //输出到根结点的数据
    {% if ds == "s" -%}
    {% for i in range(2) -%}
    .{{prefix[0]}}__{{prefix[1]}}{{i}}__xsn  ({{prefix[0]}}__{{prefix[1]}}__{{reg}}{{definition}}{{i}}_xsn   ), //写使能
    .{{prefix[0]}}__{{prefix[1]}}{{i}}__sj   ({{prefix[0]}}__{{prefix[1]}}__{{reg}}{{definition}}{{i}}_sj    ), //CRU要写的值
    .{{prefix[1]}}{{i}}__{{prefix[0]}}__sj   ({{prefix[1]}}__{{prefix[0]}}__{{reg}}{{definition}}{{i}}_sj    ){%- if i==0  -%},{%- endif -%}  //CR当前的值
    {% endfor %}{% else -%}
    .{{prefix[0]}}__{{prefix[1]}}__xsn  ({{prefix[0]}}__{{prefix[1]}}__{{reg_def}}_xsn   ), //写使能             
    .{{prefix[0]}}__{{prefix[1]}}__sj   ({{prefix[0]}}__{{prefix[1]}}__{{reg_def}}_sj    ), //CRU要写的值
    .{{prefix[1]}}__{{prefix[0]}}__sj   ({{prefix[1]}}__{{prefix[0]}}__{{reg_def}}_sj    )  //CR当前的值
    {% endif -%}
);
{% if ds == "s" -%}
{% for i in range(2) -%}
{{prefix[1]}}_{{items.interval_type}} #(
 {% if items.interval_type == "kbwk" -%}
 .SZ({{items.st_ed[0]-items.st_ed[1] +1 }}),
 {% endif -%}
 .MRZ ({{items.reset_value}})
)u_{{reg}}{{definition}}{{i}}(
    .shiz                (shiz                       ),
    .fuw_d               (fuw_d                      ),
    .{{prefix[0]}}__{{prefix[1]}}__xsn   ({{prefix[0]}}__{{prefix[1]}}__{{reg}}{{definition}}{{i}}_xsn   ),    //写使能//
    .{{prefix[0]}}__{{prefix[1]}}__sj    ({{prefix[0]}}__{{prefix[1]}}__{{reg}}{{definition}}{{i}}_sj    ),    //CRU要写的值// 
    .{{prefix[1]}}__{{prefix[0]}}__sj    ({{prefix[1]}}__{{prefix[0]}}__{{reg}}{{definition}}{{i}}_sj    ),    //CR当前的值//
    {% if 'hrw' not in items or items.hrw == 'NA' or items.hrw == 'rw' -%}
    .szdy__{{prefix[1]}}__xsn    ({{mod_to_mod}}__{{reg}}{{definition}}{{i}}_xsn      ),    //写使能//
    .szdy__{{prefix[1]}}__sj     ({{mod_to_mod}}__{{reg}}{{definition}}{{i}}_sj       ),    //所在单元要写的值//
    .{{prefix[1]}}__szdy__sj     ({{mod_to_mod_reverse}}__{{reg}}{{definition}}{{i}}_sj       )     //CR当前的值//
    {% elif items.hrw == "r" -%}
    .szdy__{{prefix[1]}}__xsn    (0),    //写使能//
    .szdy__{{prefix[1]}}__sj     (0),    //所在单元要写的值//
    .{{prefix[1]}}__szdy__sj     ({{mod_to_mod_reverse}}__{{reg}}{{definition}}{{i}}_sj       )     //CR当前的值//    
    {% elif items.hrw == "w" -%}
    .szdy__{{prefix[1]}}__xsn    ({{mod_to_mod}}__{{reg}}{{definition}}{{i}}_xsn      ),    //写使能//
    .szdy__{{prefix[1]}}__sj     ({{mod_to_mod}}__{{reg}}{{definition}}{{i}}_sj       ),    //所在单元要写的值//
    .{{prefix[1]}}__szdy__sj     ()     //CR当前的值//    
    {% endif -%}
);
{% endfor %}{% else -%}
{{prefix[1]}}_{{items.interval_type}} #(
 {% if items.interval_type == "kbwk" -%}
 .SZ({{items.st_ed[0]-items.st_ed[1] +1 }}),
 {% endif -%}
 .MRZ ({{items.reset_value}}) 
)u_{{reg_def}}(
    .shiz                (shiz                       ),
    .fuw_d               (fuw_d                      ),
    .{{prefix[0]}}__{{prefix[1]}}__xsn   ({{prefix[0]}}__{{prefix[1]}}__{{reg_def}}_xsn   ),    //写使能//
    .{{prefix[0]}}__{{prefix[1]}}__sj    ({{prefix[0]}}__{{prefix[1]}}__{{reg_def}}_sj    ),    //CRU要写的值//
    .{{prefix[1]}}__{{prefix[0]}}__sj    ({{prefix[1]}}__{{prefix[0]}}__{{reg_def}}_sj    ),    //CR当前的值//
    {% if 'hrw' not in items or items.hrw == 'NA' or items.hrw == 'rw' -%}
    .szdy__{{prefix[1]}}__xsn    ({{mod_to_mod}}__{{reg_def}}_xsn      ),    //写使能//
    .szdy__{{prefix[1]}}__sj     ({{mod_to_mod}}__{{reg_def}}_sj       ),    //所在单元要写的值//
    .{{prefix[1]}}__szdy__sj     ({{mod_to_mod_reverse}}__{{reg_def}}_sj       )     //CR当前的值//
    {% elif items.hrw == "r" -%}
    .szdy__{{prefix[1]}}__xsn    (0),    //写使能//
    .szdy__{{prefix[1]}}__sj     (0),    //所在单元要写的值//
    .{{prefix[1]}}__szdy__sj     ({{mod_to_mod_reverse}}__{{reg_def}}_sj       )     //CR当前的值//
    {% elif items.hrw == "w" -%}
    .szdy__{{prefix[1]}}__xsn    ({{mod_to_mod}}__{{reg_def}}_xsn      ),    //写使能//
    .szdy__{{prefix[1]}}__sj     ({{mod_to_mod}}__{{reg_def}}_sj       ),    //所在单元要写的值//
    .{{prefix[1]}}__szdy__sj     ()     //CR当前的值//
    {% endif -%}
);
{% endif -%}
{% endfor -%}
{% endfor -%}
{% endblock instances -%}


{% block assign %}
{%- for reg, parameters in data.items() %}
{%- if loop.first %}
    {%- for bits, items in parameters.fields.items() %}
        {%- set definition = "_"+ items.definition if items.definition %}
        {%- set reg_def = reg + definition if definition else reg %}
        {%- if loop.first %}
        assign zjjd_du_sj = {{reg_def}}_du_shuj
        {%- else %}
                            |{{reg_def}}_du_shuj
        {%- endif %}
    {%- endfor %}
{%- else %}
    {%- for bits, items in parameters.fields.items() %}
    {%- set definition = "_"+ items.definition if items.definition %}
    {%- set reg_def = reg + definition if definition else reg %}
                            |{{reg_def}}_du_shuj
    {%- endfor %}                    
{%- endif %}
{%- endfor %}
;
{% endblock %}

always@(posedge shiz or negedge fuw_d)
begin
    if(~fuw_d)
        yjd__zjjd__shuj <= 16'b0;
    else
        yjd__zjjd__shuj <= zjjd_du_sj;
end




endmodule
