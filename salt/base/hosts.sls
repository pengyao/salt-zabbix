host-salt-test-01:
  host.present:
    - ip: 172.16.0.111
    - order: 1
    - names:
      - salt-test-01

host-salt-test-02:
  host.present:
    - ip: 172.16.0.112
    - order: 1
    - names:
      - salt-test-02

host-salt-test-03:
  host.present:
    - ip: 172.16.0.113
    - order: 1
    - names:
      - salt-test-03

