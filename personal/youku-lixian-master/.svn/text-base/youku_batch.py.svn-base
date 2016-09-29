#!/usr/bin/env python
# coding=utf-8

import httplib2
import re
import simplejson
import os
import sys
import urllib

def httpget(url):
    http= httplib2.Http(".cache")
    resp,content=http.request(url, 'GET')
    '''
    try:
	content=content.decode('utf-8')
    except UnicodeDecodeError,e:
	pass
    '''
    return content    

name='咱们结婚吧'
ext='flv'
url='http://www.soku.com/search_video/q_%E5%92%B1%E4%BB%AC%E7%BB%93%E5%A9%9A%E5%90%A7'
start_idx=13

work_dir=sys.argv[0]
work_dir=work_dir[0:work_dir.rfind('/')+1]
#print work_dir

html=httpget(url)
#p=re.compile('<li><a href="(.*)" title="(.*)" charset="[\d|-]+" target="_blank">\d+</a></li>',re.MULTILINE)
p=re.compile("<a href='(http://v\.youku\.com/v_show/\w+\.html)' site='youku' _log_cate=\"\d+\" _log_type='\d+' _log_ct='\d+' _log_pos=\d+  _log_directpos='\d+'  _log_title='"+name+"' _log_sid='\d+' target='_blank'>(\d+)</a>",re.MULTILINE)
metadata=p.findall(html)
#print metadata
#print len(metadata)
for item in metadata:
	v_url=item[0]
	v_idx=item[1]
	if int(v_idx)>=start_idx:
		v_name=name+str(v_idx)+"."+ext
		if os.path.exists(v_name):
			print v_name+" already exists."
		else:
			print '[Begin] Downloading '+v_name
			os.system(work_dir+'/youku.py '+v_url)
			os.system('mv '+name+"."+ext+" "+v_name)
			print '[End] Downloading '+v_name

