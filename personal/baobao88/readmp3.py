#!/usr/bin/python
import sys

def getID3(filename):
    fp = open(filename, 'r')
    fp.seek(-128, 2)
 
    fp.read(3) # TAG iniziale
    title   = fp.read(30)
    artist  = fp.read(30)
    album   = fp.read(30)
    anno    = fp.read(4)
    comment = fp.read(28)
     
    fp.close()
 
    return {'title':title.encode('utf8'), 'artist':artist, 'album':album, 'anno':anno}

if __name__ == "__main__":  
    path=sys.argv[1]
    print getID3(path)  