#!/usr/bin/python
#coding=UTF-8
'''
Created on 2012-3-11
'''
import sys,os;
import re;
import time;
import MySQLdb;
import xml.etree.ElementTree as ET
    
def exe_sql(connection, sql, closeAfterExecute):
    executor = connection.cursor();
    executor.execute(sql);
    result = executor.fetchall();
    executor.close();
    if(closeAfterExecute) : 
        connection.close();
    return result;

def close_conn(connection):
    connection.close();
        
    
def raw_default(prompt, defaultValue=None):
   
    if defaultValue:
        prompt = "%s [ default is -> %s ]: " % (prompt, defaultValue);
        
    result = raw_input(prompt);
    if not result and defaultValue:
        return defaultValue
    return result

def highlight(text):
    return "\033[35;49;1m" + text + "\033[39;49;0m";

def get_work_dir():
    path = sys.path[0]
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)

'''
    Code Upon is common init and some Utils.                          
'''
class DNSGenerator(object):
    
    '''
        constants
    '''
    
    ipnat = {
        '10.101': '218.107.199.',
        '10.102': '218.107.218.',
        '10.103': '110.86.5.',
        
        '10.104': '110.87.98.',
        '10.106': '218.107.223.',
        '10.107': '58.23.6.',
        '10.108': '58.23.7.',
        '10.109': '218.107.217.',
    
    	'10.146': '61.28.21.',
    	'10.147': '61.28.19.',
    	'10.148': '61.28.20.',
    	'10.150': '61.28.114.',
    	'10.151': '61.28.115.',
    	'10.152': '61.28.116.',
    	'10.153': '61.28.117.',
	};
    
#    trigger_conf_file = r"D:/remote_clients.xml"
#    trigger_ct_conf_file = r"D:/ct_4_trigger.xml"
#    packer_ct_conf_file = r"D:/ct_4_packer.xml"
    trigger_conf_file = r"/usr/local/application/evermail/share/conf/remote_clients.xml"
    trigger_ct_conf_file = r"/usr/local/application/evermail/share/conf/ct_4_trigger.xml"
    packer_ct_conf_file = r"/usr/local/application/evermail/share/conf/ct_4_packer.xml"
   
    ct_ip = '218.107.199.37';   # ct net ip.
    cnt_ip = '218.107.199.35';  # content net ip.
    
    a_format = '+A %s: %s';
    mx_format = '+MX %s: %s';
    ptr_format = '+PTR %s: %s';
    spf_format = '+SPF %s: "v=spf1 a mx -all"';
    
    ct_format = '+A ct.%s: ' + ct_ip ;
    cnt_format = '+A content.%s: ' + cnt_ip;
    
    db_generated_file_name = 'generated.conf';
    trigger_generated_file_name = 'gen_trigger.conf';
    
    '''
        construct
    '''
    def init(self):
        self.__dbHost = raw_default("PLS input resource DB Host", '10.10.10.12');
        self.__dbUser = raw_default("PLS input resource DB User", '5edm');
        self.__dbPass = raw_default("PLS input resource DB Pass", 'ofxm1718_5edm');
        self.__dbName = raw_default("PLS input resource DB Name", 'resource_db');
        self.__conn = MySQLdb.connect(self.__dbHost, self.__dbUser,  self.__dbPass, self.__dbName, charset='utf8');
    
    def generate(self):
        self.bak_generate_file(self.db_generated_file_name);
        get_all_resource = 'select * from resource';
        resources = exe_sql(self.__conn, get_all_resource, True);
        genarate_file = open(self.get_generate_file_path(self.db_generated_file_name), 'a');
        for resource in resources:
            print '#### generate dns records for resource : ' + str(resource[0]);
            dns = ['#### generate dns records for resource : ' + str(resource[0])];
            ip_list = self.get_ip_list(resource[2], int(resource[3]), int(resource[4]), resource[5]);
            domains_str = resource[6];
            tracks_str = resource[7];
            ptr = resource[8];
#            dns.extend(self.generate_ptr(ip_list, ptr));
            dns.extend(self.generate_domains(ip_list, domains_str));
            dns.extend(self.generate_track(tracks_str));
            dns.append('\n\n\n');
            genarate_file.write("\n".join(dns));
            print highlight('done.');
        genarate_file.close();
        print '\nfile generated.conf has been generated.';
    
    def generate_track(self, tracks_str):
        print 'generate track(CT&CONTENT) records.'
        result = ['\n### track(CT & CONTENT) record ###'];
        if tracks_str:
            tracks = tracks_str.split(',');
            for track in tracks:
                result.append(self.ct_format % (track));
                result.append(self.cnt_format % (track));
        return result;     
    
    def generate_domains(self, ip_list, domains_str):
        print 'generate sender domain records.'
        result = ['\n### sender domain a & spf record ###']
        if domains_str:
            domains = domains_str.split(',');
            for idx, domain in enumerate(domains):
                print 'idx is: ' + str(idx);
                print 'ip list is: ' + str(ip_list);
                print 'used ip list is: ' + str(ip_list[idx::len(domains)]);
                
                # spf be first. because dns parse reverse
                result.append(self.spf_format % (domain));
                result.append(self.a_format % (domain, ','.join(ip_list[idx::len(domains)])));
                #result.append(self.a_format % (domain, ','.join(ip_list)));
		result.append(self.mx_format % (domain, domain))
        
        return result;
        
        
    def generate_ptr(self, ip_list, ptr_str):
        print 'generate PTR records.'
        result = ['\n#### IP <--> PTR domain  ###'];
        if ptr_str:
            result = ['\n#### IP --> PTR domain  ###'];
            for ip in ip_list:
                result.append(self.ptr_format % (ip, ptr_str));
            result.append('\n#### PTR domain to IP  ###');
            result.append(self.a_format % (ptr_str, ','.join(ip_list)));
        else:
            result.append('\n##### no ptr str specified.');
            
        return result;
    
    def get_ip_list(self, regex, from_index, to_index, exclude):
        ip_list = [];
        exclude_regex = re.compile(exclude) if exclude else None;
        for index in range(from_index, to_index + 1):
            ip = regex.replace('*', str(index));
            # if(not exclude_regex or not exclude_regex.match(ip)):
            if(not exclude_regex or not exclude_regex.search(ip)):
                ip_list.append(self.get_natip(ip));
        return ip_list;

    def get_natip(self, ip):
        segments = ip.split('.');
        prefix = '.'.join(segments[0:2]);
        nat_prefix = self.ipnat.get(prefix);
        if nat_prefix:
            return nat_prefix + segments[2];
        else:
            return ip;
    
    def bak_generate_file(self, name):
        if os.path.exists(self.get_generate_file_path(name)):
            os.rename(self.get_generate_file_path(name), self.get_generate_file_path(name) + '.' + str(time.time()))
        
    def get_generate_file_path(self, name):
        return get_work_dir() + os.path.sep + name;
    
    
#######################################################
####        generate trigger start here             ###
#######################################################
    
    def generate_trigger(self):
        print 'bakup old generated trigger dns records file';
        self.bak_generate_file(self.trigger_generated_file_name);
        genarate_file = open(self.get_generate_file_path(self.trigger_generated_file_name), 'a');
        
        print 'start to generate dns records for trigger.'
        print 'start to parse xml file remote_clients.xml ...'
        root = ET.parse(self.trigger_conf_file).getroot();
        clients = root.findall('remote-client');
        
        for client in clients :
            client_id = client.find('client-id').text;
            print 'parse xml for trigger client : ' + client_id;
            
            domains_str = client.find('from-domains').text;
            ptr_str = domains_str;
            ip_list = [];
            for ip_node in client.find('ips'):
                ip_list.append(self.get_natip(ip_node.text));
                
            dns = ['#### generate dns records for trigger client : ' + client_id];
            dns.extend(self.generate_ptr(ip_list, ptr_str));  
            dns.extend(self.generate_domains(ip_list, domains_str));
            dns.append('\n\n\n');
            genarate_file.write("\n".join(dns));
            
            print highlight('done.');
        
        track_dns = ['\n\n#### generate dns records for trigger track, packer track.']
        print 'start to parse xml file ct_4_trigger.xml ...'
        trigger_ct_root = ET.parse(self.trigger_ct_conf_file).getroot();
        track_list = map(lambda node: node.attrib['domain'], trigger_ct_root.findall('ct-server'));    
        
        print 'start to parse xml file ct_4_packer.xml ...'
        packer_ct_root = ET.parse(self.packer_ct_conf_file).getroot();
        track_list.extend(map(lambda node: node.attrib['domain'], packer_ct_root.findall('ct-server')));   
        track_dns.extend(self.generate_track(",".join(list(set(track_list)))));
        
        genarate_file.write("\n".join(track_dns));    
        genarate_file.close();
        print '\nfile has been generated.';
        
    
if __name__ == '__main__':
    args = sys.argv;
    if len(args) > 2 or (len(args) == 2 and args[1] != 'trigger'):
        script = str(args[0]); #.split(os.path.sep)[-1];
        print 'Wrong usage.'
        print 'usage: %s [trigger]' % (script)
        
    elif len(args) == 1:
        generator = DNSGenerator();
        generator.init();
        generator.generate();
        
    elif len(args) == 2 and args[1] == 'trigger':
        generator = DNSGenerator();
        generator.generate_trigger();
        
        
    
    
    
    
