#!/usr/bin/env python
# -*- coding: utf-8 –*-
# coding=utf-8

import httplib2
import re
import simplejson
import os,chardet
import sys
import urllib

import urllib2,cookielib
from emailutil import *


LIB_SHUIDIAN="虹口分馆水电馆"
LIB_SHANGHAI="上海图书馆"

def httpget2(book_name,uri,page):
#    url=urllib.pathname2url(url)
    url='http://ipac.library.sh.cn/ipac20/ipac.jsp'
    body={'otherloc':'true','uri':uri,'page':page}
    req = urllib2.Request(url,urllib.urlencode(body))
    req.add_header('User-Agent','Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36')
    page = urllib2.urlopen(req)
    content = page.read()
    return content
'''
    try:
	content=content.decode('utf-8')
    except UnicodeDecodeError,e:
	pass
    return content
'''

def httpget(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36')
    page = urllib2.urlopen(req)
    content = page.read()
    return content


def search_book(book_name,querystr,lib_names):
    libdata=list()
    bdata={'bookname':book_name,'libdata':libdata}
	    
    for lib in lib_names:
	    lib_name=lib[0]
	    page=str(lib[1])
	    otherloc='true'
	    if lib_name==LIB_SHANGHAI:
		otherloc='false'	
	    url="http://ipac.library.sh.cn/ipac20/ipac.jsp?otherloc="+otherloc+"&page="+page+"&"+querystr
	    html=httpget(url)
	    html=utoutf(html)
	    p=re.compile('<table class="tableBackground" cellpadding="3" cellspacing="0" width="100%" border="0">.*</table></td>')	
	    t=p.findall(html)[0]
	    lines=t.split('</tr>')
	    for line in lines:
		if not line.startswith("<tr") :
			continue
		line=line.replace('#FCFCDC','white')
		parts=re.split('<td bgcolor="[a-zA-W#]+">',line)
		parts=map(lambda x:x.replace('<a class="normalBlackFont1" bgcolor="white" title="馆藏信息">','').replace('<a class="normalBlackFont1" title="馆藏信息">','').replace('</td><td bgcolor="white">','').replace('</a>','').replace('</td>','').replace('&nbsp;','n/a'),parts)
		if not (parts[6]=="普通外借资料" and parts[1]==lib_name):
			continue
		ldata={'found':'yes','libname':parts[1],'room':parts[2],'sn':parts[3],'state':parts[4],'returndate':parts[5]}
		libdata.append(ldata)
	    if len(lines)==0:
		libdata.append({'libname':lib_name,'found':'no'})
    return bdata

def utoutf(htm):
    s = htm 
    unic = re.findall("\&#\d{5};",s)
    for u in unic:
        uni = u;
        num = int(u[2:7])
        utf = unichr(num).encode('UTF-8')
        s = s.replace(uni,utf)
    out = s.replace("Windows-1252","UTF-8")
    return out

def search_books(books):
	alldata=list()
	returned_books=list()
	for book in books:
		bookname=book[0]
		uri=book[1]
		libname=book[2]
		bookdata=search_book(bookname,uri,libname)
		alldata.append(bookdata)

	for b in alldata:
		print '《'+b['bookname']+'》'	
		libdata=b['libdata']
		for l in libdata:
			found=l['found']
			if found=='yes':
				print '	',l['libname'],l['state'],l['returndate'],l['sn'],l['room']
				if (l['state']=='归还' and b not in returned_books):
					returned_books.append(b)
			elif found=='no':
				print ' ',l['libname'],"无此书"
	return returned_books

def send_emails(books):
	subject="部分图书已可借阅: "
	html="<html><head><meta http-equiv='Content-Type' content='text/html; charset=utf-8'></head>"
	for b in books:
		book_name="《"+b['bookname']+"》"
		subject=subject+" "+book_name
		html=html+"<b>"+book_name+"</b><br>"
		html=html+"<table border=1 padding=3><tr><th>馆址</th><th>状态</th><th>归还日期</th><th>索书号</th><th>馆藏类型</th></tr>"	
		for l in b['libdata']:
			html=html+"<tr><td>"+l['libname']+"</td><td>"+l['state']+"</td><td>"+l['returndate']+"</td><td>"+l['sn']+"</td><td>"+l['room']+"</td></tr>"
		html=html+"</table><br>"
	html=html+"<html>"
	sendEmail(subject.decode('utf-8'),html,'shenrui@cn.ibm.com',['shenrui@cn.ibm.com'],[])	
	print 'An email was sent.'


if __name__ == '__main__':
	books=[
	['一线架构师实践指南','uri=link=3100006@!3263436@!3100001@!3100002',[[LIB_SHUIDIAN,1]]],
	['陆犯焉识 专著','uri=full%3D3100001%40%214298828%40%211',[[LIB_SHUIDIAN,11]]],
	['陆犯焉识','uri=full%3D3100001%40%213711572%40%210',[[LIB_SHUIDIAN,11]]],
	['Photoshop混合模式深度剖析 专著','uri=full%3D3100001%40%214172749%40%210',[[LIB_SHANGHAI,1]]]
	]
	returned_books=search_books(books)
	if len(returned_books)>0:
		send_emails(returned_books)

