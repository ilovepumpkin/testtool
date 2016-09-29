#!/usr/bin/env python
# coding=utf-8

import httplib2
import re
import simplejson
import os
import sys
import urllib

cookie=""

def login():
    url="http://www.jinmiao.cn/"
    http= httplib2.Http(".cache")
    resp,content=http.request(url, 'GET')
    global cookie
    cookie=resp["set-cookie"]
    url="http://www.jinmiao.cn/ajax.aspx"
    username='ilovepumpkin1'
    password='passw0rd'
    http= httplib2.Http(".cache")
    headers = {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8','Cookie':cookie}
    body={'cmd':'login','username':username,'password':password}
    resp,content=http.request(url, 'POST',headers=headers, body=urllib.urlencode(body))
    cookie=cookie+"; iwmsUser=%7Bver:1,id:8810,name:'ilovepumpkin1',psw:'C019988915ED3ADD',admin:0,admPs:0,signin:0,msg:0,keep:0,lastSet:6446720%7D"
 
def httpget(url):
    http= httplib2.Http(".cache")
    global cookie
    headers={'Cookie':cookie}
    resp,content=http.request(url, 'GET',headers=headers)
    return content.decode('gbk')

def httppost(url,body):
    http= httplib2.Http(".cache")
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    response, content = http.request(url, 'POST', headers=headers, body=urllib.urlencode(body))
    return content.decode('utf-8')

def handleHomepageByMainCatName(catNameList):
    html=httpget('http://www.jinmiao.cn').encode('utf-8')
    for catName in catNameList:
        print 'Start downloading main category <'+catName+'>'
        p=re.compile('<a href=".*aspx" class="sNav">'+catName+'</a><div class="navChild"><ul>(.*)<\/ul>')
        rt=p.findall(html)
        section=rt[-1]
        section=section.split('</ul>')[0]
        section=section.replace('<li style="width:20%">','')
        section=section.replace('</li>','')
        parts=section.split('</a>')
        for part in parts:
            if part=='':
                continue
            temp=part.split('>')            
            subCatName=temp[-1]
            subCatUrl='http://www.jinmiao.cn/'+part.split('"')[1]
            handleCatPage(subCatUrl,catName+"/"+subCatName)

def handleHomepageBySubCatName(catNameList):
    html=httpget("http://www.jinmiao.cn/").encode('utf-8')

    for catName in catNameList:
        p=re.compile('<li style="width:20%"><a href="(c\d{3}.aspx)">'+catName+'</a></li>')
        catlink="http://www.jinmiao.cn/"+p.findall(html)[0]
        handleCatPage(catlink,catName)
           
def handleCatPage(catUrl,catName):
    print 'Start downloading sub category <'+catName+'>'
    if not os.path.exists(catName):
       os.system('mkdir -p "'+catName+'"')
    elif os.path.exists(catName+"/.done"):
       print catName+" was done.Skip it."
       return
    else:
       # delete the newest one(it might be broken) so redownload it.
       os.system('ls -d $PWD/'+catName+'/*|tail -1|xargs rm -rf')

    catId=catUrl.split("/")[-1].split(".")[0]
    html=httpget(catUrl)
    p=re.compile('<li class="p_total">1/(\d*)</li>')
    pageNum=p.findall(html)
    if len(pageNum)==0:
        print 'Looks like there is no stories in this category <'+catName+'>'
        return
    maxPageNum=int(pageNum[0])
    for pageNum in range(maxPageNum):
        catPageUrl="http://www.jinmiao.cn/"+catId+"p"+str(pageNum+1)+".aspx"
        html=httpget(catPageUrl)
        p=re.compile('<a href="(.*)" target="_blank" class="nL[oi]+[nc]+k">(.*)</a>')
        links=p.findall(html)
        
        for link in links:
            fulllink='http://www.jinmiao.cn/'+link[0]
            name=link[1]
            #name=name[1:len(name)]
            handleDownloadPage(fulllink,name,catName)            
    os.system('touch "'+catName+'/.done"')

def handleDownloadPage(url,name,catName):
    html=httpget(url)
    '''
    html=html.lower()
    p=re.compile('href="(.*mp3)"')
    try:
        mp3link='http://www.jinmiao.cn'+p.findall(html)[0]
    except IndexError as e:
        print 'Failed to find download link in the page - '+url
        return
    '''
    p=re.compile('<a href="(.*[mM]+[pP]3)" target="_blank">')
    rt=p.findall(html)
    if len(rt)==0:
        p=re.compile('<A href="(.*[mM]+[pP]3)" target=_blank>')
        rt=p.findall(html)
        if len(rt)==0:
            print 'Failed to find download link in the page - '+url
            return

    mp3link='http://www.jinmiao.cn'+rt[0]

    mp3path=catName.decode('utf-8')+"/"+name+".mp3"
    if os.path.exists(mp3path):
       print mp3path+' exists. Skip downloading it.'
    else:
       wgetcmd_mp3='wget --retry-connrefused -O "'+mp3path+'" --header "Cookie:'+cookie+'" '+mp3link
       wgetcmd_mp3=wgetcmd_mp3+';touch "'+mp3path+'"'
       os.system(wgetcmd_mp3.encode('utf-8'))

# by sub category name
'''
subCatNames=['安徒生童话']
login()
handleHomepageBySubCatName(subCatNames)
'''
mainCatNames=['高年级有声读物-mp3下载']
login()
handleHomepageByMainCatName(mainCatNames)

