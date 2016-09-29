#!/usr/biin/env python
import urllib2
import re
import os
import sys
from emailutil import *

username=sys.argv[3]
password=sys.argv[4]
build_root=sys.argv[1]
version=sys.argv[2]
work_dir=sys.argv[0]
work_dir=work_dir[0:work_dir.rfind('/')+1]

url_passed='http://9.122.121.13/mediasets/SONAS_IVT_PASSED/'        
url_failed='http://9.122.121.13/mediasets/SONAS_IVT_FAILED/'
url_queue='http://9.122.121.13/mediasets/SONAS_IVT_QUEUE/'
url_iso='http://9.122.121.13/mediasets/SONAS-ISO/'

def get_buildid(buildurl): 
	handle = urllib2.urlopen(buildurl)
	html=handle.read()
	builds=re.findall('<a href="SONAS-'+version+'-\d{12}-.*.iso">(.*)</a>',html)
	buildid=''
	if len(builds)>0:
		buildid=builds[-1]
	handle.close()
	return buildid

def get_latest_buildurl(buildurls):
	passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
	
	latest_buildid=''
	base_url=''
	for buildurl in buildurls:
		passman.add_password(None, buildurl, username, password)
		authhandler = urllib2.HTTPBasicAuthHandler(passman)
		opener = urllib2.build_opener(authhandler)
		urllib2.install_opener(opener)
	
		buildid=get_buildid(buildurl)
		if(buildid>latest_buildid):
			latest_buildid=buildid
			base_url=buildurl

	return base_url+latest_buildid,latest_buildid

latest_build_url,buildid=get_latest_buildurl([url_iso,url_queue,url_passed])

os.system('echo latest build url:'+latest_build_url)

sub_dir=build_root+buildid

if os.path.exists(sub_dir):
	sys.exit(sub_dir+' exists already. Skip the download.')
else:
	os.system('mkdir '+sub_dir)

iso_url=latest_build_url

os.chdir(work_dir)
iso_wget='wget --no-check-certificate --user='+username+' --password='+password+' '+iso_url+' -P '+sub_dir
print iso_wget
os.system(iso_wget)

iso_file=buildid
print 'Extracting war file from the iso file '+iso_file
os.system('cd '+work_dir)
os.system('./extract_war.sh '+sub_dir+'/'+iso_file+' '+version)
os.system('"cp" -rf '+sub_dir+'/sofs-ngui/opt/IBM/sonas/war/*.war '+sub_dir+'/')
os.system(work_dir+'mkverfile.sh '+sub_dir)

#os.system(work_dir+'gen_pseudo.sh '+sub_dir+'/SONAS_NGUI.war')
#os.system(work_dir+'gen_pseudo.sh '+sub_dir+'/ifs.war')
	
subject='Mainz build '+buildid+' (war files) is downloaded!'	
html=''
from_email='shenrui@cn.ibm.com'	
to_emails=['shenrui@cn.ibm.com','junjiyu@cn.ibm.com','wangnsh@cn.ibm.com','zhuzhenq@cn.ibm.com','ddjie@cn.ibm.com']
#to_emails=['shenrui@cn.ibm.com']
cc_emails=[]	
sendEmail(subject,html,from_email,to_emails,cc_emails)
print 'Notification email was sent'
