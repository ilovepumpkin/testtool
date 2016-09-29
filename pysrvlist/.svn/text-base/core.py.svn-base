#!/usr/bin/env python
import paramiko
import httplib2
import urllib

def execCmd(host,port,username,password,cmd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(
                paramiko.AutoAddPolicy())
    ssh.connect(host, port=port,username=username, 
                password=password)
    stdin, stdout, stderr=ssh.exec_command(cmd)
    stdin.close()
    return stdout.read()

def getSVCVersion(host):
    result=execCmd(host,26,'root','l0destone',"sainfo lsservicestatus | grep -e node_sw_ | awk '{print $2}'")
    temp=result.split('\n')
    return temp[0]+"("+temp[1]+")"

def getSonasVersion(ip):
    try:
        http= httplib2.Http(disable_ssl_certificate_validation=True)
        baseUrl='https://'+ip+':1081'
        loginUrl=baseUrl+'/login'
        guiVerUrl=baseUrl+'/gui_version.txt'
        hmiVerUrl=baseUrl+'/hmi_version.txt'
        username='admin'
        password='admin'
        body = {'login': username,'password': password}
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        response, content = http.request(loginUrl, 'POST', headers=headers, body=urllib.urlencode(body))
        headers={'Content-type': 'application/x-www-form-urlencoded','Cookie':response['set-cookie']}
        response, guiVersion= http.request(guiVerUrl,'GET',headers=headers)
        response, hmiVersion= http.request(hmiVerUrl,'GET',headers=headers)
        return guiVersion.strip()+"("+hmiVersion.strip()+")" 
    except AttributeError as e:
        print e

def testWebConn(url):
    try:
        http= httplib2.Http(disable_ssl_certificate_validation=True)
        response, content = http.request(url, 'GET')
        print response
        if response['status']=='200':
            return True
        else:
            return False
    except IOError as e:
        return False
 

#print getSVCVersion('9.186.9.81')    
#print getSonasVersion("9.123.196.236")
#print testWebConn("http://9.123.196.235")
