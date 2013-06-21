base:
  '*':
    - salt.minion
    - zabbix.agent
  'salt-test-02':
    - zabbix.api
