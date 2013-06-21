base:
  '*':
    - base
    - salt.minion
    - zabbix.agent
  'salt-test-01':
    - salt.master
    - mysql.server
    - zabbix.server
    - zabbix.web
  'salt-test-02':
    - zabbix.api
  'salt-test-03':
    - memcached
