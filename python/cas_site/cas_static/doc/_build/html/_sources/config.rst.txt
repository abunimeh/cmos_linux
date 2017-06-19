.. _config:

配置文件使用手册
========================================

三种配置文件
----------------------------------------
配置文件是平台对用户的唯一接口，并且根据项目的不同、module的不同而不同，如果将平台看成一个类的话，配置文件就相当于平台根据项目例化时的构造函数，配置文件里提供了所有的参数一同影响平台的行为

平台在项目中有三种配置文件：

- PROJ_ROOT/share/config/proj.cfg

  + 项目唯一
  + 配置文件覆盖优先级低
  + 设置了runtime环境变量、回归配置参数以及simv配置文件与case配置文件的默认参数

- PROJ_MODULE/config/simv.cfg

  + 模块唯一
  + 配置文件覆盖优先级高
  + 设置了模块所有的simv以及每个simv的特性
  + simv是基于analysis与elaboration阶段结束的产物，提供给simulation使用

- PROJ_MODULE/config/case.cfg

  + 模块唯一
  + 配置文件覆盖优先级高
  + 里面设置了模块所有的case以及每个case的特性
  + case是基于simulation阶段的概念，每个case只能使用一个simv进行simulation，所以每个case对应一个simv进行simulation
  + 同级目录下的case_*.cfg也会被pj拿到并解析，但是DEFAULT section仍然是case.cfg的DEFAULT

配置文件格式
----------------------------------------
配置文件采用unix cfg格式，也是大多数linux tool与eda tool采用的cfg格式，如yum, apt-get, pip, git, svn, vcs, verdi等，这种配置文件的优点是对用户友好，缺点是无法设置复杂的数据结构，不过对用户的接口简单这条原则本身就不需要复杂的数据结构。

以verdi的novas.conf中的部分内容为例，来说明cfg文件的组成：
::

   [qBaseWindowStateGroup]
   Verdi_1\qBaseWindowRestoreStateGroup\qDockerWindow_defaultLayout\qDockerWindow_restoreNewChildState=true
   
   [qBaseWindow_saveRestoreSession_group]
   10=/workspace/tools/yigy/cpu1/verification/zszx/output/zszx_sanity_test/1/verdiLog/novas_autosave.ses
   
   [qDockerWindow_C]
   Verdi_1\position.x=0
   Verdi_1\position.y=0
   Verdi_1\width=900
   Verdi_1\height=700

- 其中[]标注的部分是section，表示一类配置
- section下面每个=行表示具体配置的option，=左右分别代表这个option的key与value
- 每个cfg文件都是由sections与options组成
- 在平台的cfg文件规则中，value是支持多值的，多值之间用半角逗号 ``,`` 分隔。

proj.cfg配置文件
----------------------------------------
每个project只有一份的配置文件，用来配置项目级别的特性，只建议project owner修改，不建议module owner修改

[boot_env], [module_env]
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
这两个section是平台用到的runtime环境变量，这样设置的目的是防止env污染，这两个section中设置的环境变量只有在pj运行过程中有效，pj运行前后都无效

[proj]
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
proj section用来配置与proj顶层有关参数

- tree_ignore

  + 用来配置tree命令的ignore目录，在pj提示所有可用module的时候过滤掉不需要显示的目录信息

- rtl_top

  + 用来指定chip顶层的module名字

- c_opts

  + 用来指定默认的c compilter使用的编译参数

[regression_simv], [regression_case], [regression_opts]
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
当kick off regression的时候，regression option负责统一管控 **覆盖** 所有默认的相同option的值，regression_opts option负责统一管控 **添加** 所有默认的相同option的值, regression_simv与regression_case负责compilation与simulation阶段的在regression模式下全局开关

[vplan_sheets], [vplan_column_width]
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
vplan是由验证相关人员维护的一套用于表征验证进度与验证完备性的文档，作为sign off的标准之一存在，目前是以excel表格的方式存放。这两个section是控制中心自行开发的vplan的格式，分别控制vplan内部的sheets的表格头名称与宽度，不可随意更改

[x86_ins]
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
用来配置集成到pj的x86指令集相关参数

[leda]
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
用来配置leda flow的相关参数

[env_simv]
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
env_simv section用来提供所有simv.cfg中可能用到的全部option的默认值，由于proj.cfg的优先级低于simv.cfg的优先级，因此simv.cfg中出现的相同option的值会覆盖这个section中的默认值

- sub_modules

  + 用来指定该module下的子module，格式是MODULE:TYPE，其中MODULE为模块名，TYPE为模块类型，比如rtl、bfm等
  + 该配置会影响生成的filelist
  + 该配置为空的时候，pj自动产生用来analysis的filelist仅由rtl.flist与tb.flist构成
  + 该配置非空，除了模块自己的 会按照TYPE将所有子模块flist目录下的TYPE.flist拿来用以构成analysis用的filelist

- flist是一套递归产生总体filelist的衍生规则，里面可以包含以下内容：

  + 包含路径的文件（相对路径或绝对路径）
  + +define+宏定义
  + +incdir+查询路径（相对路径或绝对路径）
  + 注释 （//或#行注释）
  + -f FILE指定任意其它filelist

- vhdl_tool, ana_tool, elab_tool

  + 用来指定需要做vhdl analysis, verilog analysis, elaboration
  + 默认值是vhdlan, vlogan, vcs

- file__FILENAME

  + 开放型option
  + 会在simv analysis & elaboration目录下成名为FILENAME、内容为对应option value的文件
  + 阶段执行前生成，以便analysis与elaboration过程使用

- pre_cmd, post_cmd

  + 用来配置在analysis和elaboration阶段之前与之后执行的自定义的命令
  + 可以在这里执行compilation(analysis+elaboration)的自定义脚本

- tb_top

  + 用来指定tb的top module名字
  + 默认值是test_top

- uvm, cov, wave, gui, prof, fpga

  + analysis和elaboration阶段的主要管控开关，管控每个simv的行为
  + 分别是uvm方法学环境参数开关、覆盖率收集参数开关、dump波形开关、设置断点单步执行开关、收集效率分析报告开关

- wave_format

  + 预留的支持多种格式的波形文件的option
  + 目前只支持fsdb

- custom_ana_opts, custom_elab_opts

  + 用户自定义添加的analysis阶段与elaboration阶段tool的options

- vt_TOOLNAME_dut_ana_opts, vt_TOOLNAME_tb_ana_opts, at_TOOLNAME_dut_ana_opts, at_TOOLNAME_tb_ana_opts, et_TOOLNAME_elab_opts

  + 用来指定相应的阶段工具的相应参数
  + 第一个_前的vt表示vhdl_tool、at表示ana_tool、et表示elab_tool
  + 第一个_后的名称表示相应的工具名称

- verdi_opts

  + 用来指定verdi的相应参数

- cov_elab_opts, wave_elab_opts, gui_elab_opts, prof_elab_opts, fpga_ana_opts

  + 分别受cov, wave, gui, prof开关控制的tool options
  + 当开关是on的时候会添加到相应阶段的tool otpions中

- wf_WAVEFORMAT_elab_opts

  + 这个option与wave_format option的值相关
  + 会根据wave_format的值添加到相应阶段的tool options中

[env_case]
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
env_case section用来提供所有case.cfg中可能用到的全部option的默认值，由于proj.cfg的优先级低于case.cfg的优先级，因此case.cfg中出现的相同option的值会覆盖这个section中的默认值

- lsf_*

  + 与lsf相关的参数可以在这里设置

- file__FILENAME

  + 与env_simv section中的类似
  + 开放型option
  + 会在case simulation目录下先生成名为FILENAME、内容为对应option value的文件
  + 阶段执行前生成，以便simulation过程使用

- pre_cmd, post_cmd

  + 用来配置在simulation阶段之前与之后执行的自定义的命令
  + 可以在这里执行simulation的自定义脚本

- random_times

  + 用来配置一个case的simulation次数
  + 每次simulation都是不同的随机seed

- seed

  + 用来配置一个case的seed
  + 不设置的情况下seed为1
  + 设置具体数值的时候seed固定为该数值
  + 设置random的时候seed会随机产生

- uvm, cov, wave, wave_mem, wave_glitch, gui, prof_mem, prof_time

  + simulation阶段的主要管控开关，管控每个case的行为
  + 分别是uvm方法学环境参数开关、覆盖率收集参数开关、dump波形开关、dump mem开关、dump波形显示glitch开关、设置断点单步执行开关、收集mem效率分析开关、收集time效率分析开关

- custom_simu_opts

  + 用户自定义添加simulation阶段tool的options

- uvm_simu_opts, cov_simu_opts, wave_WAVEFORMAT_simu_opts, wave_WAVEFORMAT_glitch_simu_opts, gui_simu_opts, prof_mem_simu_opts, prof_time_simu_opts

  + 分别受uvm, cov, wave, wave_glitch, gui, prof_mem, prof_time开关控制的tool options
  + 当开关是on的时候会添加到相应阶段的tool options中

- seed_simu_opts

  + 这个option与seed的值相关
  + 会根据seed的至添加到相应阶段的tool options中

- regression_type

  + 定义case的regression type
  + 支持多种类型，类型之间用 ``,`` 分隔
  + 用户可以从下表定义的regression类型中选择添加到这里

    ======= ===============================================
    类型     周期描述
    ======= ===============================================
    sanity  用来检验基本功能是否正确，通常在rtl改动之后需要kick off
    nightly 每晚kick off
    weekly  每周kick off
    all     内置类型，无需用户填写，包括module的所有case
    ======= ===============================================

- pass_string, fail_string, ignore_string

  + log解析过程中判断该case是否pass的用户自定义string
  + 在平台log parser中有一些内置好的string，通常情况下log parser都会做出正确的判断，如果用户需要改变log parser的行为，可以在这里更改
  + 每种string都可以写多种，用 ``,`` 分隔

log parser解析原理是：

- 对log按行解析
- 检测到ignore_string，跳过该行
- 检测到fail_string，该case是fail
- 检测到case没有结束，该case是pending
- log所有行没有fail_string，检测到pass string，该case是pass
- log所有行没有fail_string，没有检测到pass string，该case是unknown
- 对于uvm的case不需要pass_string，检测到没有UVM_ERROR与UVM_FATAL，而且case正常结束，该case是pass

- vplan_desc, vplan_owner, vplan_priority

  + 对应vplan中test_case那张sheet的相应case的描述部分
  + 分别反标case的description, owner, priority

simv.cfg配置文件
----------------------------------------
每个module只有一份的配置文件，用来配置模块级别在analyasis与elaboration阶段的特性，里面记录了该module的全部simv，每个section就是一个simv，每个simv都有自己一套独立的analysis与elaboration结果，module owner负责修改

[DEFAULT]
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
无论在cfg文件中是否写出来，每个cfg文件都会有一个DEFAULT section，该section的作用是提供所有其它section的默认值

simv所有的option的默认值在proj.cfg的env_simv section里面都已经提供，但是proj.cfg是整个project层面的默认值，不允许module owner修改，所以DEFAULT这个section的目的就在于提供给module owner一个module层面的可以异于project层面的默认值

[SIMV_NAME]
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
除了DEFAULT section之外，其他每个section就是一个simv，用户可以自己定义simv name，可以在这个simv section下面定制该simv个性化的options

simv section, DEFAULT section, proj.cfg env_simv section这三个section中可选的option是一致的，proj.cfg env_simv section是一个全集，提供所有option的默认值，它们的优先级是simv section > DEFAULT section > proj.cfg env_simv section

以下面一个simv.cfg为例来说明用法：
::

   # this config is used for simv level, 2nd entry (analysis and elaboration stage)
   [DEFAULT]
   ### simv default pre/post cmd in analysis and elaboration
   pre_cmd =
   post_cmd =
   
   ### simv default TB top
   tb_top = module_tb
   
   ### simv default flow control switches
   uvm = on
   cov = off
   wave = off
   gui = off
   prof = off
   
   ### simv default analysis and elaboration options
   custom_ana_opts =
   custom_elab_opts =
   
   [cov_simv]
   cov = on
   
   [dump_simv]
   wave = on

- DEFAULT section可以列出感兴趣的管控全部simvs的options，options全集在proj.cfg文件的env_simv section中
- 该模块的tb_top叫module_tb，异于默认的test_top，同时所有的simv在elaboration阶段都用module_tb，所以需要在DEFAULT section修改
- analysis与elaboration两个阶段的管控开关列在这里，只是给自己一个提示，方便修改，上面都是proj.cfg的默认值
- custom_ana_opts与custom_elab_opts也是为了方便修改列在这里
- 该模块一共有三个simv：DEFAULT, cov_simv, dump_simv，所以该模块会有三套编译结果
- cov_simv里cov设置为on，虽然DEFAULT是off，但是因为优先级的原因cov_simv里面cov = on，没有列出来的option与DEFAULT section一致，DEFAULT section里没有列出来的option与proj.cfg env_simv section一致

case.cfg配置文件
----------------------------------------
每个module只有一份的配置文件，用来配置模块级别在simulation阶段的特性，里面记录了该module的全部case，除了DEFAULT以外，每个section就是一个simv，每个simv都有自己一套独立的simulation结果，module owner负责修改

[DEFAULT]
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
无论在cfg文件中是否写出来，每个cfg文件都会有一个DEFAULT section，该section的作用是提供所有其它section的默认值

case所有的option的默认值在proj.cfg的env_case section里面都已经提供，但是proj.cfg是整个project层面的默认值，不允许module owner修改，所以DEFAULT这个section的目的就在于提供给module owner一个case层面的可以异于project层面的默认值

[CASE_NAME]
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
除了DEFAULT section之外，其他每个section就是一个case，用户需要在这里列出所有的case，同时可以在case section下面定制该case个性化的options

case section, DEFAULT section, proj.cfg env_case section这三个section中可选的option是一致的，proj.cfg env_case section是一个全集，提供所有option的默认值，它们的优先级是case section > DEFAULT section > proj.cfg env_case section

以下面一个case.cfg为例来说明用法：
::

   # this config is used for case level, 2nd entry (simulation stage)
   [DEFAULT]
   ### case default pre/post cmd in simulation
   pre_cmd =
   post_cmd =
   
   ### case default simulation random times (No.)
   random_times =
   
   ### case default seed (random/No.)
   seed =
   
   ### case default flow control switches
   uvm = on
   cov = off
   wave = off
   wave_mem = off
   wave_glitch = off
   run_gui = off
   prof_mem = off
   prof_time = off

   ### case default tools simulation options
   custom_simu_opts =
   
   ### case default regression type
   regression_type =
   
   [module__sanity_test]
   regression_type = sanity
   [module__direct_test]
   regression_type = nightly, weekly
   simv = dump_simv
   wave = on
   wave_glitch = on
   [module__random_test]
   regression_type = nightly, weekly
   simv = cov_simv
   random_times = 10
   [module__random_test2]
   regression_type = weekly
   seed = 12345

- DEFAULT section可以列出感兴趣的管控全部case的options，options全集在proj.cfg文件的env_case section中
- 该模块的没有使用全局管控的options开关，DEFAULT里面都是proj.cfg env_case section里的默认值
- 该模块一共有4个case：module__sanity_test, module__direct_test, module__random_test, module__random_test2
- module__sanity_test

  + regression类型是sanity
  + 没有指定simv就属于DEFAULT simv，会使用DEFAULT simv进行simulation

- module__direct_test

  + regression类型既是nightly，又是weekly
  + 属于simv.cfg的dump_simv，使用dump_simv生成的simv进行simulation
  + 该case会dump波形，并且dump的波形会打开glitch

- module_random_test

  + regression类型既是nightly，又是weekly
  + 属于simv.cfg的cov_simv，使用cov_simv生成的simv进行simulation
  + kick off 10次random的simulation，每次都使用不同的random seed

- module_random_test2

  + regression类型是weekly
  + 使用12345的seed kick off 1次simulation

利用平台runner(pj)工作
----------------------------------------
project owner配置好proj.cfg，module owner配置好simv.cfg和case.cfg之后，来利用pj开始工作吧，具体说明请参考 :ref:`runner`
