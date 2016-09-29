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
    return content.decode('utf-8')

def httppost(url,body):
    http= httplib2.Http(".cache")
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    response, content = http.request(url, 'POST', headers=headers, body=urllib.urlencode(body))
    return content.decode('utf-8')


def download(songs_page_url,out_dir):
    if not os.path.exists(out_dir):
       os.system('mkdir -p '+out_dir)

    html=httpget(songs_page_url)
    p=re.compile('/song/(\d*)',re.MULTILINE)
    idList=set(p.findall(html))
    print str(len(idList))+' songs will be downloaded.'
    ids=",".join(idList)
    url="http://ting.baidu.com/data/music/songlink"

    body={'songIds':ids}
    html=httppost(url,body)
    jsonstr=simplejson.loads(html)
    songList=jsonstr['data']['songList']
    xcode=jsonstr['data']['xcode']
    for song in songList:
        mp3name=song['songName']+"("+song['artistName']+")"
        mp3link=song['songLink']+"?xcode="+xcode
        mp3path=out_dir.decode('utf-8')+"/"+mp3name+".mp3"
        lrclink='http://ting.baidu.com'+song['lrcLink']
        lrcpath=out_dir.decode('utf-8')+"/"+mp3name+".lrc"
        if os.path.exists(mp3path):
            print mp3path+' exists. Skip downloading it.'
        else:
            wgetcmd_mp3='wget --retry-connrefused -O "'+mp3path+'" '+mp3link
            wgetcmd_lrc='wget --retry-connrefused -O "'+lrcpath+'" '+lrclink
            os.system(wgetcmd_mp3.encode('utf-8'))
            os.system(wgetcmd_lrc.encode('utf-8'))

