#!/usr/bin/env python
import urllib2
import re
import os
import sys
from emailutil import *

username='shenrui'
password='4rfv5tgb'
build_root=sys.argv[1]
version=sys.argv[2]
work_dir=sys.argv[0]
work_dir=work_dir[0:work_dir.rfind('/')+1]


url='http://fscc-x36m3-3.mainz.de.ibm.com/AutoBuild/bvt_isologs/BVT-PASSED/'        
passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
passman.add_password(None, url, username, password)
authhandler = urllib2.HTTPBasicAuthHandler(passman)
opener = urllib2.build_opener(authhandler)
urllib2.install_opener(opener)

handle = urllib2.urlopen(url)
html=handle.read()
handle.close()
builds=re.findall('<a href="SONAS-'+version+'-\d{12}-r\d{5}M?.iso">(.*)</a>',html)
buildid=''
if len(builds)>0:
	buildid=builds[-1]
#print builds
#print buildid
failed_url='http://fscc-x36m3-3.mainz.de.ibm.com/AutoBuild/bvt_isologs/BVT-FAILED/'
handle = urllib2.urlopen(failed_url)
html=handle.read()
handle.close()
builds=re.findall('<a href="SONAS-'+version+'-\d{12}-r\d{5}M?.iso">(.*)</a>',html)
failed_buildid=""
if len(builds)>0:
	failed_buildid=builds[-1]

latest_build_url=url+buildid
if failed_buildid>buildid:
	buildid=failed_buildid
	latest_build_url=failed_url+failed_buildid

os.system('echo latest build url:'+latest_build_url)
sub_dir=build_root+buildid

if os.path.exists(sub_dir):
	sys.exit(sub_dir+' exists already. Skip the download.')
else:
	os.system('mkdir '+sub_dir)

os.system('ssh root@9.155.103.28 \'/root/downwar/download.sh '+latest_build_url+' '+version+'\'')

os.system('scp root@9.155.103.28:/tmp/sofs-ngui/opt/IBM/sonas/war/SONAS_NGUI.war '+sub_dir)
os.system('scp root@9.155.103.28:/tmp/sofs-ngui/opt/IBM/sonas/war/ifs.war '+sub_dir)

os.system(work_dir+'mkverfile.sh '+sub_dir)

#os.system(work_dir+'gen_pseudo.sh '+sub_dir+'/SONAS_NGUI.war')
#os.system(work_dir+'gen_pseudo.sh '+sub_dir+'/ifs.war')
	
subject='Mainz build '+buildid+' (war files) is downloaded!'	
html=''
from_email='shenrui@cn.ibm.com'	
to_emails=['shenrui@cn.ibm.com','zhuzhenq@cn.ibm.com','wangnsh@cn.ibm.com','jtingsh@cn.ibm.com','hullsh@cn.ibm.com']
#to_emails=['shenrui@cn.ibm.com']
cc_emails=[]	
sendEmail(subject,html,from_email,to_emails,cc_emails)
print 'Notification email was sent'
