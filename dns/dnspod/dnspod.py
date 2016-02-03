#!/usr/bin/env python
#-*- coding:utf-8 -*-
from apicn import * 
import json
import os
import re
import sys
import argparse

# dnspod token 
tid="token_id"
token="token"
# record default value
record_line=u"默认".encode("utf8")
ttl=600
# config
#config_file="/tmp/zpdns.conf"

# 读取配置文件，获取域名，子域名，记录类型，值等信息
def parseRecord(line):
    record_dict = {}
    line = line.strip('\n')
    type = line.split(" ")[0]
    global_domain = line.split(" ")[1]
    value = " ".join(line.split(" ")[2:])
    list = re.split('\.', global_domain)
    domain = ".".join(list[-2:])
    sub_domain = ".".join(list[:-2])
    record_dict.update({"sub_domain":sub_domain})
    record_dict.update({"record_type":type})
    record_dict.update({"value":value})
    record_dict.update({"domain":domain})
    return record_dict

# 查找dnspod帐号上已经绑定的域名
def getExistDomain():
    exist_domain_dict = {}
    api = DomainList(tid=tid, token=token)
    exist_domain_list = api().get("domains")
    for exist_domain in exist_domain_list :
	exist_domain_dict.update({exist_domain["name"]:{"status":exist_domain["status"], "id":exist_domain["id"]}})
    return exist_domain_dict

def getDomainId(domain):
    exist_domain_dict = getExistDomain()
    if exist_domain_dict.has_key(domain):
	domain_id = exist_domain_dict[domain]["id"]
	return domain_id
    else:
	print "domain no exist!"
	sys.exit()

# 获取域名存在的记录
def getExistRecord(domain_id):
    api = RecordList(domain_id=domain_id, tid=tid, token=token)
    exist_record_list = api().get("records")
    return exist_record_list

# 判断添加的记录是否已经存在
def recordIsExist(domain_id, sub_domain, record_type, value):
    exist_record_list = getExistRecord(domain_id)
    exist_record_id = ""
    for exist_record in exist_record_list :
	if exist_record["name"]==sub_domain and exist_record["type"] == "MX" and exist_record["value"] == value and exist_record["enabled"] == "1":
		exist_record_id = exist_record["id"]
		break
	elif exist_record["name"]==sub_domain and exist_record["type"] == record_type and exist_record["enabled"] == "1":
		exist_record_id = exist_record["id"]
		break
    print exist_record_id
    return exist_record_id

# 在dnspod上绑定域名
def addDomain(domain):
    api = DomainCreate(domain, tid=tid, token=token)
    return api().get("domain")["id"]
   	 
# 在dnspod上解绑域名
def removeDomain(domain):
    api = DomainRemove(domain, tid=tid, token=token)
    data = api()
    print data

# 添加记录
def addDomainRecord(domain_id, sub_domain, record_type, value): 
    if record_type == "MX":
	mx = 5
	value = value + "."
    else:
	mx = None
    if record_type == "CNAME":
	value = value + "."
    print domain_id, sub_domain, record_type, value, mx
    api = RecordCreate(domain_id=domain_id,sub_domain=sub_domain,record_type=record_type,record_line=record_line,value=value,ttl=ttl,mx=mx,tid=tid,token=token)
    if api().get("status")["code"] == "1":
        print "Add domain record success."
    else:
	print "Add domain record failed!"

# 修改域名状态
def changeDomainStatus(domain_id, status):
    api = DomainStatus(domain_id=domain_id, status=status, tid=tid, token=token)
    if api().get("status")["code"] == "1":
        print "change domain status success."
    else:
	print "change domain status failed!"

# 修改记录状态
def changeRecordStatus(domain_id, record_id, status):
    api = RecordStatus(domain_id=domain_id, record_id=record_id, status=status, tid=tid, token=token)
    if api().get("status")["code"] == "1":
        print "change record status success."
    else:
	print "change record status failed!"

# 修改记录
def updateDomainRecord(domain_id, record_id, sub_domain, record_type, value): 
    api=RecordModify(domain_id=domain_id,record_id=record_id,sub_domain=sub_domain,record_type=record_type,record_line=record_line,value=value,ttl=ttl,tid=tid, token=token)
    if api().get("status")["code"] == "1":
        print "update record status success."
    else:
	print "update record status failed!"

def generate(config_file):
    if os.path.isfile(config_file):
	file_object = open(config_file, 'rb')
	for line in file_object:
	    record_dict=parseRecord(line)
	    sub_domain = record_dict["sub_domain"]
	    domain = record_dict["domain"]
	    record_type = record_dict["record_type"]
	    value = record_dict["value"]
    	    exist_domain_dict = getExistDomain()
	    if exist_domain_dict.has_key(domain):
		domain_status = exist_domain_dict[domain]["status"]
		domain_id = exist_domain_dict[domain]["id"]
		if domain_status != "enable":
		    changeDomainStatus(domain_id, status="enable")
		exist_record_id = recordIsExist(domain_id, sub_domain, record_type, value)
		if exist_record_id:
		    changeRecordStatus(domain_id, exist_record_id, status="disable")
		    addDomainRecord(domain_id, sub_domain, record_type, value)
		    #updateDomainRecord(domain_id, record_id, sub_domain, record_type, value)
		else:
		    addDomainRecord(domain_id, sub_domain, record_type, value)
	    else:
		domain_id = addDomain(domain)
		addDomainRecord(domain_id, sub_domain, record_type, value)
	file_object.close()
    else:
	print "No config!"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="dnspod api", formatter_class=argparse.RawDescriptionHelpFormatter, \
	 epilog='''
Example:
	python dnspod.py -f config_file
	python dnspod.py -A 'A @.baidu.com 2.2.2.2'
	python dnspod.py -A 'MX @.baidu.com mx01.baidu.com'
	python dnspod.py -A 'TXT @.baidu.com "v=spf1 ipv4:1.1.1.0/24 -all"'
	'''
	)
    parser.add_argument("-f", action="store", dest='file')
    parser.add_argument("-l", action="store_true", dest='list', help="list all damains")
    parser.add_argument("-s", action="store", dest='show', help="show record on domain")
    parser.add_argument("-N", action="store", dest='add_domain', help="Add a domain")
    parser.add_argument("-D", action="store", dest='remove_domain', help="Remove a domain")
    parser.add_argument("-d", action="store", dest='disable_domain', help="Disable a domain")
    parser.add_argument("-e", action="store", dest='enable_domain', help="Enable a domain")
    parser.add_argument("-A", action="store", dest='add_record', help="Add a record")
    args = parser.parse_args()
    if args.file:
	generate(args.file)

    if args.list:
	domain_dict = getExistDomain()
	for (domain,value) in domain_dict.items():
	    print domain
	    print value

    if args.show:
	domain_id = getDomainId(args.show)
	record_list = getExistRecord(domain_id);
	for record in record_list:
	    print record['name'], record['type'], record['value'], record['enabled']

    if args.add_domain:
	addDomain(args.add_domain)

    if args.disable_domain: 
	domain_id = getDomainId(args.disable_domain) 
	status = "disable"
	changeDomainStatus(domain_id, status)

    if args.enable_domain:
	domain_id = getDomainId(args.enable_domain)
	status = "enable"
	changeDomainStatus(domain_id, status)

    if args.remove_domain:
	domain_id = getDomainId(args.remove_domain)
	removeDomain(domain_id)

    if args.add_record :
	record_dict = parseRecord(args.add_record)
	sub_domain = record_dict["sub_domain"]
	domain = record_dict["domain"]
	record_type = record_dict["record_type"]
	value = record_dict["value"]
	domain_id = getDomainId(domain)
	exist_record_id = recordIsExist(domain_id, sub_domain, record_type, value)
	if exist_record_id:
	    changeRecordStatus(domain_id, exist_record_id, status="disable")
	    addDomainRecord(domain_id, sub_domain, record_type, value)
	else:
	    addDomainRecord(domain_id, sub_domain, record_type, value)

