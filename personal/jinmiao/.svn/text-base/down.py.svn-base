#!/usr/bin/env python
# coding=utf-8

import httplib2
import re
import simplejson
import os
import sys
import urllib

cookie=""

def httpget(url):
    http= httplib2.Http(".cache")
    resp,content=http.request(url, 'GET')
    return content.decode('gb2312')

def httppost(url,body):
    http= httplib2.Http(".cache")
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    response, content = http.request(url, 'POST', headers=headers, body=urllib.urlencode(body))
    return content.decode('utf-8')

def downByCategory(catName):
    html=httpget("http://www.jinmiao.cn/c798.aspx").encode('utf-8')
    p=re.compile('<a href="(.*)">'+catName+'</a>')
    catlink="http://www.jinmiao.cn/"+p.findall(html)[0]

    if not os.path.exists(catName):
       os.system('mkdir -p '+catName)

    html=httpget(catlink)
    p=re.compile('<a href="(.*)" target="_blank" class="nLink">(.*)</a>')
    links=p.findall(html)
    for link in links:
        fulllink='http://www.jinmiao.cn/'+link[0]
        name=link[1]
        name=name[1:len(name)]
        html=httpget(fulllink)
        p=re.compile('<A href="(.*)" target=_blank>') 
        mp3link='http://www.jinmiao.cn'+p.findall(html)[0]
        mp3path=catName.decode('utf-8')+"/"+name+".mp3"
        wgetcmd_mp3='wget --retry-connrefused -O "'+mp3path+'" --header "Cookie:'+cookie+'" '+mp3link
        os.system(wgetcmd_mp3.encode('utf-8'))

	
catName='上下五千年'
url='http://www.goodkejian.com/ertonggushi9.htm'

if not os.path.exists(catName):
	os.system('mkdir -p '+catName)

html=httpget(url)
p=re.compile('<div class="name">(.*) mp3</div>')
names=p.findall(html)
#for name in names:
#	dUrl='http://down.goodkejian.com/gushi/睡前故事mp3下载 '+name.encode('utf-8')+'.rar'
#	print dUrl
p=re.compile('<a href="http://www\.goodkejian\.com/down\.asp\?id=(\d*)&amp;sid=2">')
ids=p.findall(html)

id_from=int(ids[0])
for aid in ids:
	url='http://www.goodkejian.com/down.asp?id='+str(aid)+'&sid=2'
	http= httplib2.Http(".cache")
	resp,content=http.request(url, 'GET')
	dUrl=resp['content-location']
	name=names[int(aid)-id_from]
        mp3path=catName.decode('utf-8')+"/"+name+".rar"
        wgetcmd_mp3='wget --retry-connrefused -O "'+mp3path+'" '+dUrl
        os.system(wgetcmd_mp3.encode('utf-8'))


