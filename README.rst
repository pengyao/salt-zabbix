SaltStack结合Zabbix完成服务自动部署及监控
#################################################


环境说明
********************************

基于`SaltStack`_ ,结合`Zabbix`_ 完成服务自动化部署及监控

本次测试的服务为`Memcached`_ 服务,监控模板采用`zbl/zabbix模板 <http://github.com/zbl/zabbix/>`_ , Zabbix API采用`zapi <https://github.com/baniuyao/ZabbixPythonApi>`_ 

**测试环境**:

===== ============= =============== =================== ========================================= ================
序号  主机名        IP              OS版本              角色                                      salt版本    
===== ============= =============== =================== ========================================= ================
1     salt-test-01  172.16.0.111    CentOS 6.4 X86_64   salt master/minion & zabbix server& web   0.15.1       
2     salt-test-02  172.16.0.112    CentOS 6.4 X86_64   salt minion & zabbix api操作机            0.15.1        
3     salt-test-03  172.16.0.113    CentOS 6.4 X86_64   salt minion & zabbix agent & memcached    0.15.1         
===== ============= =============== =================== ========================================= ================

**salt**: salt state

**pillar**: salt pillar

salt-test-01主机之前安装有 `MySQL-python <http://mirrors.sohu.com/centos/6/os/x86_64/Packages/MySQL-python-1.2.3-0.3.c1.1.el6.x86_64.rpm>`_ 软件包, 以保证mysql的相关state模块可以使用

执行过程
*********************************
    
    # salt '*' saltutil.sync_all

    # salt '*' state.highstate

    # salt 'salt-test-02' state.highstate


当前问题
*********************************
1. 当前采用的Zabbix API为1.8 API，不支持2.0中的模板自动导入功能，因此在部署完zabbix server后，安装memcached服务前，需要登录zabbix web导入监控模板
2. 由于采用salt mine进行角色传递，传递给zabbix api操作机，因此需要执行两次state.highstate，第一次会将角色信息以mine方式传递给salt master,第二次会将角色信息传递给zabbix api操作机





.. _Salt: http://saltstack.org/

.. _SaltStack: http://saltstack.org/

.. _Zabbix: http://www.zabbix.com/

.. _Memcached: http://memcached.org/
