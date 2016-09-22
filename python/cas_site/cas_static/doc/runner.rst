.. _runner:

runner(pj)使用手册
========================================

初始化pj
----------------------------------------
利用module来加载pj：

``$ module load pj``

您也可以添加 ``module load pj`` 行到~/.cshrc将pj自动加载，module的详细用法可以参考 `Tools工具配置 <http://172.51.13.70/do/view/Main/Tools_configure>`_

子命令参数模式
----------------------------------------
linux多参数tools基本都是子命令参数模式，如yum, apt-get, pip, git, svn等，这种参数模式的优点是将功能点按照子命令归类，模块化边界清晰。

以svn为例，我们可以通过 ``svn -h`` 来查看svn所有的子命令：
::

   $ svn -h
   usage: svn <subcommand> [options] [args]
   Subversion command-line client, version 1.6.11.
   Type 'svn help <subcommand>' for help on a specific subcommand.
   Type 'svn --version' to see the program version and RA modules
     or 'svn --version --quiet' to see just the version number.
   
   Most subcommands take file and/or directory arguments, recursing
   on the directories.  If no arguments are supplied to such a
   command, it recurses on the current directory (inclusive) by default.
   
   Available subcommands:
      add
      blame (praise, annotate, ann)
      cat
      changelist (cl)
      checkout (co)
      cleanup
      commit (ci)
      copy (cp)
      delete (del, remove, rm)
      diff (di)
      export
      help (?, h)
      import
      info
      list (ls)
      lock
      log
      merge
      mergeinfo
      mkdir
      move (mv, rename, ren)
      propdel (pdel, pd)
      propedit (pedit, pe)
      propget (pget, pg)
      proplist (plist, pl)
      propset (pset, ps)
      resolve
      resolved
      revert
      status (stat, st)
      switch (sw)
      unlock
      update (up)
   
   Subversion is a tool for version control.
   For additional information, see http://subversion.tigris.org/

其中从add开始到update都是svn的子命令，每个子命令负责一类特征明显的操作，比如checkout负责从svn code repo中取code到本地所有相关的操作，checkout的行为根据checkout后面跟的参数的不同而不同。

子命令checkout的参数可以通过 ``svn checkout -h`` 来查看：
::

   $ svn checkout -h
   checkout (co): Check out a working copy from a repository.
   usage: checkout URL[@REV]... [PATH]
   
     If specified, REV determines in which revision the URL is first
     looked up.
   
     If PATH is omitted, the basename of the URL will be used as
     the destination. If multiple URLs are given each will be checked
     out into a sub-directory of PATH, with the name of the sub-directory
     being the basename of the URL.
   
     If --force is used, unversioned obstructing paths in the working
     copy destination do not automatically cause the check out to fail.
     If the obstructing path is the same type (file or directory) as the
     corresponding path in the repository it becomes versioned but its
     contents are left 'as-is' in the working copy.  This means that an
     obstructing directory's unversioned children may also obstruct and
     become versioned.  For files, any content differences between the
     obstruction and the repository are treated like a local modification
     to the working copy.  All properties from the repository are applied
     to the obstructing path.
   
     See also 'svn help update' for a list of possible characters
     reporting the action taken.
   
   Valid options:
     -r [--revision] ARG      : ARG (some commands also take ARG1:ARG2 range)
                                A revision argument can be one of:
                                   NUMBER       revision number
                                   '{' DATE '}' revision at start of the date
                                   'HEAD'       latest in repository
                                   'BASE'       base rev of item's working copy
                                   'COMMITTED'  last commit at or before BASE
                                   'PREV'       revision just before COMMITTED
     -q [--quiet]             : print nothing, or only summary information
     -N [--non-recursive]     : obsolete; try --depth=files or --depth=immediates
     --depth ARG              : limit operation by depth ARG ('empty', 'files',
                               'immediates', or 'infinity')
     --force                  : force operation to run
     --ignore-externals       : ignore externals definitions
   
   Global options:
     --username ARG           : specify a username ARG
     --password ARG           : specify a password ARG
     --no-auth-cache          : do not cache authentication tokens
     --non-interactive        : do no interactive prompting
     --trust-server-cert      : accept unknown SSL server certificates without
                                prompting (but only with '--non-interactive')
     --config-dir ARG         : read user configuration files from directory ARG
     --config-option ARG      : set user configuration option in the format:
                                    FILE:SECTION:OPTION=[VALUE]
                                For example:
                                    servers:global:http-library=serf

例如我们想checkout svn上某个特定changelist，就可以利用-r参数 ``svn checkout URL -r CL`` ；不想让checkout的信息打印在stdout上就可以利用-q参数 ``svn checkout URL -q``。

所以checkout子命令就只负责与checkout动作相关的所有操作，其他操作比如commit，merge会有其它子命令负责。

查看pj子命令
----------------------------------------
pj就是如上一段所讲的子命令参数体系，查看pj的全部子命令：

::

   $ pj -h
   usage: pj [-h] [-l LOG] {run,regr,cov,flist,vplan,reg,doc,clean} ...
   
   positional arguments:
     {run,regr,cov,flist,vplan,reg,doc,clean}
       run                 sub cmd about running simulation
       regr                sub cmd about kicking off regression
       cov                 sub cmd about merging and analyzing coverage
       flist                sub cmd about generating filelist
       vplan               sub cmd about processing vplan
       reg                 sub cmd about generating auto reg
       doc                 sub cmd about generating natural docs
       clean               sub cmd about cleaning output
   
   optional arguments:
     -h, --help            show this help message and exit
     -l LOG                input log name <MUST come first>

目前pj的全部子命令有：

- run：负责simulation相关的所有操作，包括verdi
- regr：负责regression相关
- cov：负责coverage相关
- flist：负责RTL、TB等filelist生成相关
- vplan：负责vplan相关
- reg：负责autoreg相关
- doc：负责NaturalDocs相关
- clean：负责clean output以及中间文件相关

pj子命令参数详细说明
----------------------------------------

子命令run
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
- 查看子命令run的全部参数：

  + ``$ pj run -h``

- 列出一个module下全部case：

  + ``$ pj run -m MODULE -list``
  + pj允许在proj trunk的任意dir下面跑，所以需要得到module name信息

- 跑module下面的所有case：

  + ``$ pj run -m MODULE -all``

- 跑一个case：

  + ``$ pj run -m MODULE -c CASE``

- 跑一个case（支持case命名的隐式规则）：

  + ``$ pj run -c CASE(MODULE__***)``
  + 如果一个case name的第一个双下划线 ``__`` 前面是module name，就无需通过 ``-m`` 指定module name

- 跑多个case：

  + ``$ pj run -c CASE1 CASE2 ...``

- 只compilation(analysis+elaboration)，不simulation：

  + ``$ pj run -m MODULE -comp``

- 指定seed（*）：

  + ``$ pj run -c CASE -seed SEED``

- random seed（*）：

  + ``$ pj run -c CASE -seed random``

- dump波形（*）：

  + ``$ pj run -c CASE -wave``

- dump mem（*）：

  + ``$ pj run -c CASE -wave mem``

- 波形显示glitch（*）：

  + ``$ pj run -c CASE -wave glitch``

- 打开verdi自动load波形：

  + ``$ pj run -c CASE -verdi``

- dump波形之后打开verdi自动load波形：

  + ``$ pj run -c CASE -wave -verdi``

- 没有tb，供desinger用verdi查看rtl：

  + ``$ pj run -m MODULE -verdi``

- 用verdi设置断点，单步调试：

  + ``$ pj run -c CASE -gui``

- 指定随机次数（*）：

  + ``$ pj run -c CASE -rt TIMES``

- 带coverage的simulation（*）：

  + ``$ pj run -c CASE -cov``
  + 会默认load vdb constraint file PROJ_MODULE/config/cov.filter

- 带效率分析报告的simulation（*）：

  + ``$ pj run -c CASE -prof time``
  + ``$ pj run -c CASE -prof mem``

- 自定义tools options（*）：

  + ``$ pj run -c CASE -A ANA_OPTS``
  + ``$ pj run -c CASE -E ELAB_OPTS``
  + ``$ pj run -c CASE -E SIMU_OPTS``
  + 在analysis, elaboration, simulation三个阶段添加用户自己需要的simulation tools的options

（*）group.cfg与case.cfg中如果配置了同样的功能，cmd中相同功能的参数可以去掉，都存在的情况下cmd args的优先级高

根据\*标注的特点，我们可以将绝大部分的cmd args放到cfg里面来配置，cmd会被简化成统一的样式 ``$ pj run -c CASE`` 根据平台的这个特性，这里会有两种主要的工作方式：

- cfg based

  + 平台的新特性
  + cmd简单
  + 可以同时kick off不同options的case
  + 每个特殊case的配置不需要特别记录
  + 可以对所有case全局控制analysis, elaboration, simulation各个阶段

- cmd args based

  + 之前验证环境使用的比较传统的工作方式
  + 每个case都用cmd args的方式来控制
  + 学习成本低

大家可以根据自己的喜好来选择不同的工作方式，也可以各取所需，结合它们的特点混合使用

子命令regr
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
- 查看子命令regr的全部参数：

  + ``$ pj regr -h``

- 跑一个module的一种类型的regression：

  + ``$ pj regr -m MODULE -t REGR_TYPE``

- 跑多个module的多种类型的regression：

  + ``$ pj regr -m MODULE1 MODULE2 ... -t REGR_TYPE1 REGR_TYPE2 ...``

- 默认的regression type是sanity，跑一个module的sanity可以简化为：

  + ``$ pj regr -m MODULE``

- 跑一个module全部case的regression：

  + ``$ pj regr -m MODULE -t all``
  + all是一种内置的regression type，不需要用户配置

- 跑指定随机次数的regression：

  + ``$ pj regr -m MODULE -rt TIMES``

- 跑带coverage的regression：

  + ``$ pj regr -m MODULE -cov``

- **跑完regression自动显示web report：**

  + ``$ pj regr -m MODULE -rpt``

默认regression结束会在stdout上显示regression report table，并在output下生成regr_rpt文件。完整的包括所有人，所有历史的report可以访问 http://172.51.13.205:8000/regr ，关于该report平台、platform server以及平台数据库请参考 :ref:`backend`

子命令cov
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
- 查看子命令cov的全部参数：

  + ``$ pj cov -h``

- merge一个模块的coverage：

  + ``$ pj cov -m MODULE``

- 利用verdi打开一个模块merge好的coverage：

  + ``$ pj cov -m MODULE -verdi``
  + 会默认load vdb waiver PROJ_MODULE/config/\*.el

- 生成coverage report：

  + ``$ pj cov -m MODULE -rpt``
  + 会默认load vdb waiver PROJ_MODULE/config/\*.el

子命令flist
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
flist是一套递归产生总体filelist的衍生规则，里面可以包含以下内容：

- 包含路径的文件（相对路径或绝对路径）
- +define+宏定义
- +incdir+查询路径（相对路径或绝对路径）
- 注释 （//或#行注释）
- -f FILE指定任意其它filelist

rtl designer提供每个模块以及顶层的filelist，pj flist负责产生提供给design和verification使用的统一filelist。

- 查看子命令flist的全部参数：

  + ``$ pj flist -h``

- 根据提供的base files生成filelist：

  + ``$ pj flist -f FILE1 FILE2 ...``

子命令vplan
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
- 查看子命令vplan的全部参数：

  + ``$ pj vplan -h``

- 反标PROJ_MODULE/vplan目录下的全部xml文件：

  + ``$ pj vplan -m MODULE``

子命令reg
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
- 查看子命令reg的全部参数：

  + ``$ pj reg -h``

子命令doc
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
- 查看子命令doc的全部参数：

  + ``$ pj doc -h``

- 利用NaturalDocs生成inline docs：

  + ``$ pj doc -m MODULE``

子命令clean
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
- 查看子命令clean的全部参数：

  + ``$ pj clean -h``

- clean一个module的output：

  + ``$ pj clean -m MODULE``
  + 包括analysis、elaboration、simulation阶段的所有生成的文件以及所有case，请谨慎操作

- clean一个case的simulation output：

  + ``$ pj clean -m MODULE -c CASE``
  + ``$ pj clean -c CASE`` （case命名满足隐式规则情况下）
  + 包括这个case的所有seed目录

- clean多个case的simulation output：

  + ``$ pj clean -c CASE1 CASE2 ...``
  + 包括多个case的所有seed目录

- clean一个module的coverage：

  + ``$ pj clean -m MODULE -cov``
  + 包括merge的结果以及coverage reports

pj将全部中间文件按类放置于PROJ_MODULE/output下，在了解这些分类目录的前提下，用rm也可以很方便的clean，目录结构功能细节请参考 `平台目录结构`_

平台目录结构
----------------------------------------
这里主要介绍和平台有关的目录结构

PROJ_ROOT/share/cmn/config/
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
proj.cfg所在目录

PROJ_ROOT/verification/MODULE
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
每个模块的主要工作目录
::
   
   MODULE
   ├── c                         # 模块simulation所需要的c和asm文件
   ├── config                    # module.cfg, case.cfg, cov.filter, \*.el等文件
   ├── doc                       # NaturalDocs生成的doc
   ├── flist                     # rtl.flist, tb.flist
   ├── output                    # 所有仿真文件，临时文件，中间文件等不需要checkin的文件
   │   ├── __c_lib__             # c和asm编译出来的库文件
   │   ├── __cov__               # coverage相关文件
   │   │   ├── cm                # coverage数据
   │   │   └── merge             # coverage merge后的数据以及生成的report
   │   ├── __group__             # analysis+elaboration相关文件
   │   │   ├── DEFAULT           # DEFAULT group compilation相关文件，包括生成的simv
   │   │   ├── group1            # group1 group compilation相关文件，包括生成的simv
   │   │   └── group2
   │   └── module_sanity_test    # module_sanity_test case相关文件
   │       ├── 1                 # 以seed命令的目录，在该seed下simulation相关文件
   │       ├── 119974
   │       ├── 205236
   │       ├── 316245
   │       ├── 370561
   │       ├── 415104
   │       ├── 563042
   │       ├── 716947
   │       ├── 753549
   │       ├── 91185
   │       └── 979315
   ├── reg                       # reg相关文件
   ├── scr                       # custom script相关文件
   ├── tb                        # tb所有文件
   └── vplan                     # vplan相关文件

每个新模块在已经有c与tb目录的情况下，只需要完成 **config目录下的module.cfg和case.cfg** 还有 **flist目录下的rtl.flist与tb.flist** 就可以调用pj了

开发阶段说明
----------------------------------------
pj目前还在开发阶段，以上列出的所有子命令包括参数以及目录结构只是开发计划中的一小部分，有些子命令已经基本完备，例如run, regr, cov，有些子命令还没有开始全面开发，例如vplan, reg，因此该手册也会根据pj的release定期更新，欢迎大家试用，如有任何问题及建议，请联系平台组 **yigy@cpu.com.cn**
