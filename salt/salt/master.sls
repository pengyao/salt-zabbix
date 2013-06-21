include:
  - salt.minion

salt-master:
  pkg.installed:
    - name: salt-master
  file.managed:
    - name: /etc/salt/master
    - require:
      - pkg: salt-master
  service.running:
    - enable: True
    - watch:
      - pkg: salt-master
      - file: salt-master

salt-master-role:
  file.append:
    - name: /etc/salt/roles
    - text:
      - 'salt-master'
    - require:
      - file: roles
      - service: salt-master
      - service: salt-minion
    - watch_in:
      - module: sync_grains
