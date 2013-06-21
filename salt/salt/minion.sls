salt-minion:
  pkg.installed:
    - name: salt-minion
  file.managed:
    - name: /etc/salt/minion
    - source: salt://salt/files/etc/salt/minion
    - template: jinja
    - defaults:
        master: salt-test-01
    - require:
      - pkg: salt-minion
  service.running:
    - enable: True
    - watch:
      - pkg: salt-minion
      - file: salt-minion

roles:
  file.managed:
    - name: /etc/salt/roles
       
sync_grains:
  module.wait:
    - name: saltutil.sync_grains

mine_update:
  module.run:
    - name: mine.update
    - require:
      - module: sync_grains

salt-minion-role:
  file.append:
    - name: /etc/salt/roles
    - text:
      - 'salt-minion'
    - require:
      - file: roles
      - service: salt-minion
    - watch_in:
      - module: sync_grains
