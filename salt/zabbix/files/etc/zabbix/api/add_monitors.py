#!/bin/env python
#coding=utf8

##########################################################
# Add Monitor To Zabbix
# 
# Author: pengyao
# Date: 2013-06-19
##########################################################

import sys, os.path
import yaml

from zabbix.zapi import *

def _config(config_file):
    '''get config'''
    
    config_fd = open(config_file)
    config = yaml.load(config_fd)

    return config

def _get_templates(api_obj, templates_list):
    '''get templates ids'''

    templates_id = {}
    templates_result = api_obj.Template.getobjects({"host": templates_list})
    
    for each_template in templates_result:
        template_name = each_template['name']
        template_id = each_template['templateid']
        templates_id[template_name] = template_id

    return templates_id

def _get_host_templates(api_obj, hostid):
    '''get the host has linked templates'''

    templates_id = []
    templates_result = api_obj.Template.get({'hostids': hostid})
      
    for each_template in templates_result:
        template_id = each_template['templateid']
        templates_id.append(template_id)

    return templates_id


def _create_hostgroup(api_obj, group_name):
    '''create hostgroup'''

    ##check hostgroup exists
    hostgroup_status = api_obj.Hostgroup.exists({"name": "%s" %(group_name)}) 
    if hostgroup_status:
        print "Hostgroup(%s) is already exists" %(group_name)
        group_id = api_obj.Hostgroup.getobjects({"name": "%s" %(group_name)})[0]["groupid"]
    else:
        hostgroup_status = api_obj.Hostgroup.create({"name": "%s" %(group_name)})
        if hostgroup_status:
            print "Hostgroup(%s) create success" %(group_name)
            group_id = hostgroup_status["groupids"][0]
        else:
            sys.stderr.write("Hostgroup(%s) create failed, please connect administrator\n" %(group_name))
            exit(2)

    return group_id

def _create_host(api_obj, hostname, hostip, group_id):
     '''create host'''
    
     ##check host exists
     host_status = api_obj.Host.exists({"name": "%s" %(hostname)})
     if host_status:
         print "Host(%s) is already exists" %(hostname)
         hostid = api_obj.Host.getobjects({"name": "%s" %(hostname)})[0]["hostid"]
     else:
         host_status = api_obj.Host.create({"host": "%s" %(hostname), "interfaces": [{"type": 1, "main": 1, "useip": 1, "ip": "%s" %(hostip), "dns": "", "port": "10050"}], "groups": [{"groupid": "%s" %(group_id)}]})
         if host_status:
             print "Host(%s) create success" %(hostname)
             hostid = host_status["hostids"][0] 
         else:
             sys.stderr.write("Hostgroup(%s) create failed, please connect administrator\n" %(group_name))
             exit(3)

     return hostid

def _link_templates(api_obj, hostname, hostid, templates_list):
    '''link templates'''

    all_templates = []
    ##get templates id
    templates_id = _get_templates(api_obj, templates_list) 
    ##get the host currently linked tempaltes
    curr_linked_templates = _get_host_templates(api_obj, hostid)
    
    for each_template in templates_id:
        if templates_id[each_template] in curr_linked_templates:
            print "Host(%s) is already linked %s" %(hostname, each_template)
        else:
            print "Host(%s) will link %s" %(hostname, each_template)
        all_templates.append(templates_id[each_template])
    
    ##merge templates list
    for each_template in curr_linked_templates:
        if each_template not in all_templates:
            all_templates.append(each_template)

    ##convert to zabbix api style
    templates_list = []
    for each_template in all_templates:
        templates_list.append({"templateid": each_template})


    ##update host to link templates
    update_status = api_obj.Host.update({"hostid": hostid, "templates": templates_list})

    if update_status:
        print "Host(%s) link templates success" %(hostname)
    else:
        print "Host(%s) link templates failed, please contact administrator" %(hostname)


def _main():
    '''main function'''
  
    hosts = [] 
    if len(sys.argv) > 1:
        hosts = sys.argv[1:]
    
    config_dir = os.path.dirname(sys.argv[0])
    if config_dir:
        config_file = config_dir+"/"+"config.yaml"
    else:
        config_file = "config.yaml"

    ###get config options
    config = _config(config_file)
    Monitor_DIR = config["Monitors_DIR"]
    Hostgroup = config["Hostgroup"]
    Zabbix_URL = config["Zabbix_URL"]
    Zabbix_User = config["Zabbix_User"]
    Zabbix_Pass = config["Zabbix_Pass"]

    if not hosts:
        hosts = os.listdir(Monitor_DIR)

    ###Login Zabbix 
    zapi = ZabbixAPI(url=Zabbix_URL, user=Zabbix_User, password=Zabbix_Pass)
    zapi.login()

    ###Create Hostgroup
    group_id = _create_hostgroup(zapi, Hostgroup)
    
    
    for each_host in hosts:
        each_config_fd = open(Monitor_DIR+"/"+each_host) 
        each_config = yaml.load(each_config_fd)
     
        ##Get config options
        each_ip = each_config["IP"]
        each_templates = each_config["Templates"]

        ##Create Host
        hostid = _create_host(zapi, each_host, each_ip, group_id)
    
        if each_templates:
            ##Link tempaltes
            _link_templates(zapi, each_host, hostid, each_templates)
           


if __name__ == "__main__":
    _main()

