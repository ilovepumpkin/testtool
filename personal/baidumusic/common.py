#!/usr/bin/env python
# coding=utf-8

import httplib2
import re
import simplejson
import os
import sys
import urllib

import urllib2,cookielib

def login(username,password):
        cj = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	opener.addheaders = [('User-agent','Opera/9.23')]
        urllib2.install_opener(opener)
	get_api_url = 'http://passport.baidu.com/v2/api/?getapi&class=login&tpl=music&tangram=false'
	req = urllib2.Request(get_api_url)
	page = urllib2.urlopen(req)
	
	req = urllib2.Request(get_api_url)
	page = urllib2.urlopen(req)
	c = page.read()
	#print c

	tokent_regex = re.compile('''bdPass\.api\.params\.login_token='(.*?)';''',re.DOTALL)
	match = tokent_regex.findall(c)
	if match :
		token = match[0]
		#print self.token
	else :
		print c
		raise Exception,"can not get login token"

	login_url = 'https://passport.baidu.com/v2/api/?login'
	params = {}
	params['charset'] = 'UTF-8'
	params['codestring'] = ''
	params['token'] = token
	params['isPhone'] = 'false'
	params['index'] = '0'
	params['u'] = ''
	params['safeflg'] = '0'
	params['staticpage'] = 'pass_jump.html'
	params['loginType'] = '1'
	params['tpl'] = 'music'
	params['callback'] = 'callback'
	params['username'] = username
	params['password'] = password
	params['verifycode'] = ''
	params['mem_pass'] = 'on'
	req = urllib2.Request(login_url)
	#req.add_header('Cookie',urllib.urlencode(self.cookies))
	page = urllib2.urlopen(req,urllib.urlencode(params))
	c = page.read()

def httpget(url):
    req = urllib2.Request(url)
    page = urllib2.urlopen(req)
    content = page.read()
    try:
	content=content.decode('utf-8')
    except UnicodeDecodeError,e:
	pass
    return content

def httpget2(url):
    req = urllib2.Request(url)
    page = urllib2.urlopen(req)
    content = page.read()
    return content

def httppost(url,body):
    data = urllib.urlencode(body)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    content = response.read()	
    return content.decode('utf-8')

def down_file(file_path,file_link):
    if os.path.exists(file_path):
        print file_path+' exists. Skip downloading it.'
    else:
        wgetcmd='wget --retry-connrefused -O "'+file_path+'" "'+file_link+'"'
        os.system(wgetcmd.encode('utf-8'))


def download(idList,out_dir):
    if not os.path.exists(out_dir):
       os.system('mkdir -p '+out_dir)

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

