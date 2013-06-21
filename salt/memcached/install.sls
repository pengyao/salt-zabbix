include:
  - zabbix.agent
  - salt.minion

memcached:
  pkg.installed:
    - name: memcached
  service.running:
    - name: memcached
    - enable: True
    - watch:
      - pkg: memcached
  
memcached-role:
  file.append:
    - name: /etc/salt/roles
    - text:
      - 'memcached'
    - require:
      - file: roles
      - service: memcached
      - service: salt-minion
    - watch_in:
      - module: sync_grains
