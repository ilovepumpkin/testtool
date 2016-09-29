#!/usr/bin/env python
# coding=utf-8

from common import *

def get_artistid(artist_name):
    search_artist_url="http://ting.baidu.com/search/artist?key="+artist_name
    html=httpget(search_artist_url)
    p=re.compile('/artist/redirect\?id=(\d*)')
    result=p.findall(html)
    if len(result)==0:
        sys.exit("Sorry, I don't know this artist - "+artist_name)
    artist_id=result[0]

    url="http://ting.baidu.com/data/artist/redirect?id="+artist_id
    http= httplib2.Http(".cache")
    resp,content=http.request(url, 'GET')
    return resp["content-location"].split("/")[-1]

if len(sys.argv)==1:
    sys.exit("Usage:./ting_artist.py <artist name>")
artist_name=sys.argv[1]
artist_id=get_artistid(artist_name)
if artist_id=="":
    sys.exit("Failed to get artist id for "+artist_name)
songlist_url='http://ting.baidu.com/artist/'+artist_id+'/song?order=hot&start=0&size=10000'

print 'Start downloading all the songs of '+artist_name
download(songlist_url,artist_name)



