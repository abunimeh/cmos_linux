.. _backend:

backend构架介绍
========================================
平台的backend框架主要是给runner提供一些辅助功能来实现更好的用户体验，同时它还是数据中心，所有simulation、regression的数据通过一个web前端向外展示

Database
----------------------------------------
使用PostgreSQL9.5搭建的SQL Server，目前只有记录regression信息的一个database，所有regression的信息会汇总到这里

Web Framework
----------------------------------------
利用Django1.10, bootstrap3搭建的web框架，详细的regression report以及平台文档都是通过这个web框架对外展示

如何访问平台
----------------------------------------
在linux eda和windows虚拟机通过访问 http://172.51.13.205:8000 打开平台的index

index页面如下图所示：

    .. image:: images/INDEX.png

进入regression report web app，会显示一个所有kick off regression的用户列表：

    .. image:: images/user_list.png

点击想要查看report的用户，会显示一个日期入口列表，上半部分列出的是该日期merge到一起的regression report，下半部分列出的是每次的regression report：

    .. image:: images/date_list.png

点击想要查看的merged report或者single report，会显示一个项目入口列表，列出该report所有的projects以及这个用户在这个report里面的project的passing rate：

    .. image:: images/proj_list.png

点击想要查看的project，会显示模块的入口列表，列出该project所有的modules以及module的passing rate：

    .. image:: images/module_list.png

继续点击想要查看的module，会显示case的状态列表，列出该module已经被kick off的case以及case的status：

    .. image:: images/case_list.png

点击case的status链接，将会指出相关的log路径。因为我们目前的workspace没有nas支持，eda之间的log不同步，后面在nas支持开启之后，会通过这个链接直接显示log内容：

    .. image:: images/log_list.png


开发阶段说明
----------------------------------------
backend目前还在开发初期阶段，regression report只是一个初期试用版，因此该手册也会根据backend的release定期更新，欢迎大家试用，如有任何问题及建议，请联系平台组 **yigy@cpu.com.cn**
