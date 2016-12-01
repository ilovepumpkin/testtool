#!/usr/bin/env python
# coding=utf-8

import re
import os
import sys
import shutil 

path = os.path.abspath('.')

def findCommStr(str1,str2):
    # print "str1:"+str1
    # print "str2:"+str2
    str1=str1.decode('utf8')
    str2=str2.decode('utf8')
    minlen=min(len(str1),len(str2))
    i=1
    while (i<minlen):
        if str1[:i]!=str2[:i]:
            break
        i+=1  
    if i==1:
        return None
    else:
        return re.compile('\d*$').sub('',str1[:i-1])

def validate(name):
    if name.startswith('第'): 
        return False
    elif len(re.compile('^\d+').findall(name))>0:
        return False
    else:
        return True

def group():
    folders=[]
    for root,dirs,files in os.walk(path,True):
        print dirs
        folders.extend(map(lambda x:x.decode('utf8'),dirs))
        i=0
        files=sorted(files)
        file_count=len(files)
        while i<file_count:
            # print files[i]
            str1=files[i]
            print str1
            if validate(str1):                
                if len(folders)>0:
                    # print folders
                    found=filter(lambda x:str1.startswith(x.encode('utf8')),folders)
                    if len(found)>0:
                        dst=os.path.join(path,found[0].encode('utf8'))
                        filepath=os.path.join(dst,str1)
                        if not os.path.exists(filepath):
                            shutil.move(str1,dst)
                            continue
                if i<file_count-1:   
                    str2=files[i+1]
                    if validate(str2):
                        comm_str=findCommStr(str1,str2)
                        if comm_str!=None:
                            print 'comm:'+comm_str
                            folders.append(comm_str)
                            folder_path=os.path.join(path,comm_str.encode('utf8'))
                            if not os.path.exists(folder_path):
                                print "创建文件夹: "+folder_path
                                os.mkdir(folder_path)
                                shutil.move(str1,folder_path)
                                shutil.move(str2,folder_path)
            i+=1

    
# print findCommStr('警犬汉克历险记1（初次历险）1.mp3','宫克父子历险记20.mp3')==None
if __name__ == "__main__":  
    group()  