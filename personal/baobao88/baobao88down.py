#!/usr/bin/env python
# coding=utf-8

import traceback
import httplib2
import re
import simplejson
import os
import sys
import urllib
import urllib2
from urllib2 import HTTPError

cookie = ""


def login():
    global cookie
    url = "http://www.baobao88.com/member/index_do4.php"
    username = 'ilovepumpkin'
    password = 'passw0rd'
    http = httplib2.Http(".cache")
    headers = {'Content-Type':
        'application/x-www-form-urlencoded;charset=UTF-8', 'Cookie': cookie}
    body = {'fmdo': 'login', 'dopost': 'login',
        'userid': username, 'pwd': password}
    resp, content = http.request(
        url, 'POST', headers=headers, body=urllib.urlencode(body))
    setcookie = resp['set-cookie']
    PHPSESSID = re.compile('PHPSESSID=[\w\d]+;').findall(setcookie)[0]
    DedeUserID = re.compile('DedeUserID=\d+;').findall(setcookie)[0]
    DedeUserIDckMd5 = re.compile(
        'DedeUserIDckMd5=[\w\d]+;').findall(setcookie)[1]
    DedeLoginTime = re.compile('DedeLoginTime=\d+;').findall(setcookie)[0]
    DedeLoginTimeckMd5 = re.compile(
        'DedeLoginTimeckMd5=[\w\d]+;').findall(setcookie)[1]
    cookie = PHPSESSID+DedeUserID+DedeUserIDckMd5+DedeLoginTime+DedeLoginTimeckMd5 + \
        'AJSTAT_ok_pages=6; AJSTAT_ok_times=1; bdshare_firstime=1372830511943;acopendivids=jason; acgroupswithpersist=pets'


def httpget(url):
    http = httplib2.Http(".cache")
    headers = {'Cookie': cookie}
    resp, content = http.request(url, 'GET', headers=headers)
    return content


def get_mp3_url(url):
    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', cookie))
    f = opener.open(url,None,5)
    return f.geturl()


def httppost(url, body):
    http = httplib2.Http(".cache")
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    response, content = http.request(
        url, 'POST', headers=headers, body=urllib.urlencode(body))
    return content.decode('utf-8')

def find(name, path):
    for root, dirs, files in os.walk(path):
        for file in files:
            file=file.decode('utf8')
            if name == file:
               return os.path.join(root.decode('utf8'), name)

def fetchCatName(url):
    html = httpget(url)
    html = html.decode('gbk')
    # print html
    entries = re.compile('<a href="[/\-\.a-z0-9]+" class="red2">(((?!<).)+)</a>').findall(html)
    if len(entries)>0:
        return entries[0][0]+"/"+entries[1][0]+"/"+entries[2][0]
    else:
        print "Failed to fetch category name for url: "+url
        sys.exit(0)    

def go(catUrl):

    catName=fetchCatName(catUrl).encode('utf8');

    last_page_file = catName+'/'+'.last_page'
    last_item_file = catName+'/'+'.last_item'
    done_file = catName+'/'+'.done'
    failed_file = catName+'/'+'.failed'

    print 'Start downloading the category <'+catName+'>'
    if not os.path.exists(catName):
        os.system('mkdir -p "'+catName+'"')
    
    if os.path.exists(done_file):
        print catName+" was done.Skip it."
        return
    else:
        # delete very small files
        os.system('find '+catName+' -size -5k -type f -name *.mp3|xargs rm -rf')
        # delete the newest one(it might be broken) so redownload it.
        os.system('more '+last_item_file+' | xargs rm -rf')
        last_page = ''
        last_page_found = True
        if os.path.exists(last_page_file):
            last_page = open(last_page_file).readline().replace('\n', '')
            last_page_found = False
            print 'The last page is: '+last_page

        try:
            for i in range(1000):
                j = i+1
                url = catUrl[:catUrl.rindex('--')+2]+str(j)+".html"

                if not last_page_found:
                    if last_page != url:
                        continue
                    else:
                        print 'Last page found! - '+url
                        last_page_found = True

                html = httpget(url)
                html = html.decode('gbk')

                entries = re.compile(
                    '<input name="id\[\]" type="checkbox" value="(\d+)"  onclick="getcheck\(\'id\[\]\'\)"/><a href="([/\w\d]*.html)" target="_blank">([^<>"]*)</a>').findall(html)
                if(len(entries) == 0):
                    print '[End]'+url
                    break;

                print '[page'+str(j)+']'+url
                cmd_record_lastpage = 'echo "'+url+'">'+last_page_file
                os.system(cmd_record_lastpage)

                for entry in entries:
                    aId = entry[0]
                    storyPageUrl = 'http://www.baobao88.com'+entry[1]
                    title = entry[2]
                    mp3path = catName

                    # get the book name
                    bookName = ""
                    html = httpget(storyPageUrl)
                    # html = html.decode('gbk')
                    html = unicode(html,'gbk')
                    # entries = re.compile(
                    #     '<div class="t_mp3_info t_mp3_gc">.*《(.*)》.*</div>').findall(html)
                    entries = re.search(u'《((?!《).)+》',html)
                    if(entries!=None):
                        bookName = entries.group(0).encode('utf-8').replace('《','').replace('》','')
                        mp3path=mp3path+"/"+bookName
                        if not os.path.exists(mp3path):
                            os.system('mkdir -p "'+mp3path+'"')

                    mp3name=title+".mp3"        
                    mp3path = mp3path.decode('utf-8')+"/"+mp3name

                    # if os.path.exists(mp3path):
                    found_file=find(mp3name,catName)
                    if found_file!=None:
                        print found_file+' exists. Skip downloading it.'
                        continue

                    origDUrl=""    
                    dUrl=""
                    i=0    
                    for i in range(1,5):
                        dul=""
                        if i!=1:
                            dul="&dul="+str(i)
                        origDUrl = 'http://www.baobao88.com/member/loginsta_DOWN.php?id=' + aId+dul+"&tit="+urllib2.quote(title.encode('gbk'))+".mp3";
                        print "["+str(i)+"]"+origDUrl
                        try:
                            dUrl = get_mp3_url(origDUrl)
                            break
                        except Exception as e: 
                            print 'URL error: ',e
                            traceback.print_exc()
                            continue
                    
                    if i==4: # i==4 means all servers have been tried ever        
                        os.system('echo "'+mp3path.encode('utf-8')+'|'+origDUrl.encode('utf-8')+'">>'+failed_file)
                        continue    
                    
                    wgetcmd_mp3='wget --retry-connrefused -O "'+mp3path.encode('utf-8')+'" "'+dUrl+'"'
                    wgetcmd_mp3='echo "'+mp3path.encode('utf-8')+'">'+last_item_file+';'+wgetcmd_mp3
                    os.system(wgetcmd_mp3)
            
            os.system('touch '+done_file)
        except Exception as e:  
            print 'Error occurred: ',e
            traceback.print_exc()
            sys.exit(0)    

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
            # name=name[1:len(name)]
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
'''
mainCatNames=['高年级有声读物-mp3下载']
login()
handleHomepageByMainCatName(mainCatNames)
'''
'''
login()
print cookie
url='http://www.baobao88.com/member/loginsta_DOWN.php?id=113974&tit=%E7%B3%BA%EC%CA%F7'
dUrl=get_mp3_url(url)
dUrl=urllib2.unquote(dUrl)
print dUrl
os.system('wget -O 测试.mp3 '+dUrl)
'''

# catList=[["http://www.baobao88.com/list/68/15--0--0--.html",'7-12岁儿童故事'],["http://www.baobao88.com/list/131/23--0--0--.html","小学课文朗读一年级"],["http://www.baobao88.com/bbmusic/baike/95_.html","儿童百科"],["http://www.baobao88.com/youshen/chengyu/99_.html","成语故事"],["http://www.baobao88.com/youshen/shangxiawuqiannian/100_.html","上下五千年"],["http://www.baobao88.com/youshen/bbstory/zuowen/134_.html","小学生作文"]]
# catList=[["http://www.baobao88.com/babybook/wenxue/zuowen/91_.html","小学作文"],["http://www.baobao88.com/babybook/baike/shenghuo/40_.html","生活百科"],["http://www.baobao88.com/babybook/baike/zhiran/43_.html","自然百科"],["http://www.baobao88.com/babybook/baike/jiankang/41_.html","健康百科"],["http://www.baobao88.com/babybook/baike/anquan/","安全百科"]]

catList=[["http://www.baobao88.com/list/101/15--182--138--.html"]]

login()
for cat in catList:
    go(cat[0])
