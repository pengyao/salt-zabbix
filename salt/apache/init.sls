apache:
  pkg.installed:
    - name: httpd
  file.managed:
    - name: /etc/httpd/conf/httpd.conf
    - require: 
      - pkg: apache
  service.running:
    - name: httpd
    - enable: True
    - watch:
      - pkg: apache
      - file: apache

httpd-conf.d:
  file.directory:
    - name: /etc/httpd/conf.d/
    - watch_in:
      - service: apache
