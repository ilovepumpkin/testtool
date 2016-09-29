#!/usr/bin/env python
# coding=utf-8

from common import *

toplist=[["http://ting.baidu.com/top/dayhot","热歌榜"],["http://ting.baidu.com/top/new","新歌榜"],["http://ting.baidu.com/top/rock","摇滚榜"],["http://ting.baidu.com/top/jazz","爵士榜"],["http://ting.baidu.com/top/folk","民谣榜"],["http://ting.baidu.com/top/ost","影视歌曲榜"]]
    
if len(sys.argv)==1:
   print("Usage:./ting_top.py <toplist num>")
   num=0
   for item in toplist:
       print str(num)+"."+item[1]
       num+=1
   sys.exit(0)
   
top_num=sys.argv[1]
error_msg="Please input the number among "+str(range(len(toplist)))
try:
    int(top_num)
except ValueError as e:
    sys.exit(error_msg)

if int(top_num) not in range(len(toplist)):
    sys.exit(error_msg)

top=toplist[int(top_num)]
url=top[0]
topname=top[1]

print 'Start download songs in '+topname

download(url,topname)
