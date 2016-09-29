#!/usr/bin/env python
import urllib2
import re
import os
import sys
import time
from emailutil import *

username='shenrui'
password='6789yuio'
build_root=sys.argv[1]
version=sys.argv[2]
work_dir=sys.argv[0]
work_dir=work_dir[0:work_dir.rfind('/')+1]

url='https://tucgsa.ibm.com/gsa/tucgsa/projects/s/sonas_sw/builds/'        
passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
passman.add_password(None, url, username, password)
authhandler = urllib2.HTTPBasicAuthHandler(passman)
opener = urllib2.build_opener(authhandler)
urllib2.install_opener(opener)

handle = urllib2.urlopen(url)
html=handle.read()
handle.close()
#print html

builds=re.findall('<A HREF="'+version+'-[\d|\w]*/">(.*)</A>\s*(\d\d-[\w|\W]{3}-\d{4} \d\d:\d\d)',html)

# Look for the latest build by the time stamp
buildid=builds[0][0]
recentdate_str=builds[0][1]
recentdate=time.strptime(recentdate_str,"%d-%b-%Y %M:%S")
for build in builds:
	tmp_buildid=build[0]
	tmp_recentdate_str=build[1]
	tmp_recentdate=time.strptime(tmp_recentdate_str,"%d-%b-%Y %M:%S")
	if(tmp_recentdate>recentdate):
		buildid=tmp_buildid
		recentdate=tmp_recentdate
latest_build_url=url+buildid

os.system('echo latest build for '+version+':'+latest_build_url)

handle=urllib2.urlopen(latest_build_url)
html=handle.read()
#print html

iso_file=re.findall('<A HREF="SONAS-'+version+'-.*.iso">(.*)</A>',html)[-1]
iso_url=latest_build_url+iso_file
md5_file=re.findall('<A HREF="SONAS-'+version+'-.*.md5">(.*)</A>',html)[-1]
md5_url=latest_build_url+md5_file
ifsupgrade_files=re.findall('<A HREF="IBM2073_INSTALL_'+version+'-.*">(.*)</A>',html)

if len(ifsupgrade_files)==2:
	ifsupgrade_url=latest_build_url+ifsupgrade_files[0]
	ifsupgrade_md5_url=latest_build_url+ifsupgrade_files[1]

build_dir=build_root+buildid
if os.path.exists(build_dir):
	print build_dir+' exists already. Skip the download.'
else:
	# download iso file
	print 'Downloading '+iso_url
	os.system('/usr/bin/wget --http-user='+username+' --http-password='+password+' --no-check-certificate -P '+build_dir+' '+iso_url) 
	print 'Downloading '+md5_url
	os.system('/usr/bin/wget --http-user='+username+' --http-password='+password+' --no-check-certificate -P '+build_dir+' '+md5_url)
	os.chdir(build_dir)
	os.system('md5sum -c '+md5_file+' > md5check_result')
	os.chdir(work_dir)
	print 'Extracting war file from the iso file '+iso_file
	os.system('./extract_war.sh '+build_dir+'/'+iso_file+' '+version)
	# download IFS upgrade file
	if len(ifsupgrade_files)==2:
		print 'Downloading '+ifsupgrade_url
        	os.system('/usr/bin/wget --http-user='+username+' --http-password='+password+' --no-check-certificate -P '+build_dir+' '+ifsupgrade_url)
        	os.system('/usr/bin/wget --http-user='+username+' --http-password='+password+' --no-check-certificate -P '+build_dir+' '+ifsupgrade_md5_url)
	# send an E-mail
	subject='HMI build '+iso_file+' is downloaded!'	
	html=''
	from_email='shenrui@cn.ibm.com'	
 	to_emails=['shenrui@cn.ibm.com','junjiyu@cn.ibm.com','wangnsh@cn.ibm.com','zhuzhenq@cn.ibm.com','ddjie@cn.ibm.com']
	cc_emails=[]	
	sendEmail(subject,html,from_email,to_emails,cc_emails)
	print 'Notification email was sent'
