zabbix-api:
  Zabbix_URL: http://salt-test-01/zabbix
  Zabbix_User: admin
  Zabbix_Pass: zabbix
  Hostgroup: Salt-Discovery
  Monitors_DIR: /etc/zabbix/api/monitors/
  Templates_DIR: /etc/zabbix/api/templates/
  
zabbix-templates:
  memcached: Template_Memcached
