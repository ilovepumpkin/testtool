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
    global cookie
    if cookie=="":
        cookie=resp["set-cookie"]
    return content.decode('gbk')

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

cats=["科普故事","动物故事","名人故事","历史故事","益智故事"]
for cat in cats:
    downByCategory(cat)
