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

#login
login('ilovepumpkin@126.com','passw0rd')

artist_id=get_artistid(artist_name)
if artist_id=="":
    sys.exit("Failed to get artist id for "+artist_name)

artist_url='http://music.baidu.com/artist/'+artist_id
html=httpget(artist_url)
p=re.compile('<a class="list" hidefocus="true" href="#">(.*)<\/a>')
songs_count=p.findall(html)[0].split('(')[1].replace(')','')

songs_count=int(songs_count)

song_ids=[]
start_idx=0
while start_idx<songs_count:
    songs_page_url='http://music.baidu.com/data/user/getsongs?start='+str(start_idx)+'&ting_uid='+artist_id+'&order=hot'
    html=httpget(songs_page_url)
    html=html.decode("unicode-escape")
    html=html.replace('&quot;','')
    #print html.encode('utf-8')
    #html=re.sub('\\\u[\d|\w]{4}','',html)
    #p=re.compile("sid: (\d+),",re.MULTILINE)
    p=re.compile("sid:(\d+),.*sname:(.+)}",re.MULTILINE)
    song_ids+=p.findall(html)
    start_idx+=20

print str(len(song_ids))+" songs will be downloaded."

out_dir=artist_name
if not os.path.exists(out_dir):
   os.system('mkdir -p '+out_dir)

for song_info in song_ids:
    song_id=song_info[0]
    song_name=song_info[1].replace('}','').decode('unicode-escape')
    mp3name=song_name+"("+artist_name.decode('utf-8')+")"
    mp3path=out_dir.decode('utf-8')+"/"+mp3name+".mp3"

    if os.path.exists(mp3path):
        print mp3path+' exists. Skip downloading it.'
        continue

    down_page_url='http://music.baidu.com/song/'+song_id+'/download'
    html=httpget(down_page_url)
    
    #p=re.compile('<a target="_blank" title=".*" class="song-link-hook" href="/song/'+song_id+'">(.*)</a>')
    #rt=p.findall(html)
    #song_name=rt[0]	
   
    html=html.encode("utf-8")
    p=re.compile('href="(/data/music/file\?link=.*xcode=.*song_id=\d+)"')
    rt=p.findall(html)
    if(len(rt)==0):
        p=re.compile('<a target="_blank" href="(http://pan.baidu.com/share/link.*)">.*</a>') 
        rt=p.findall(html)
        if(len(rt)==0):
            continue
        pan_url=rt[0].replace('amp;','')
        pan_html=httpget(pan_url) 
        p=re.compile('"(http://d\.pcs\.baidu\.com/file/.*)",".*"')
        rt=p.findall(pan_html)
        if(len(rt)==0):
            continue
        else:
            std_mp3_url=rt[0] 
    else:
        std_mp3_url='http://music.baidu.com'+rt[0]
    #p=re.compile('downlink="\/data\/music\/file\?link=(.*)" name="')
    #exc_mp3_url=p.findall(html)[0]

    print 'Downloading '+song_name

    mp3link=std_mp3_url

    down_file(mp3path,mp3link)
    
    song_page_url='http://music.baidu.com/song/'+song_id
    html=httpget(song_page_url)
    p=re.compile('"href":"(\/data2\/lrc\/.*.lrc)"')
    rt=p.findall(html)
    if(len(rt)>0):
        lrc_id=rt[0]
        down_lrc_url='http://music.baidu.com/'+lrc_id
        lrclink=down_lrc_url
        lrcpath=out_dir.decode('utf-8')+"/"+mp3name+".lrc"
        down_file(lrcpath,lrclink)


#print idList

#print 'Start downloading all the songs of '+artist_name
#download(songlist_url,artist_name)


