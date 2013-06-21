epel-repo:
  pkg.installed:
    - sources:
      - epel-release: salt://base/files/epel-release-6-8.noarch.rpm
    - order: 1
    
