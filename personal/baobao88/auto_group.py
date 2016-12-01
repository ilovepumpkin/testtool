#!/usr/bin/env python
# coding=utf-8

import re
import os
import sys
import shutil 

def findCommStr(str1,str2):
    print "str1:"+str1
    print "str2:"+str2
    str1_len=len(str1)
    print str1_len
    i=str1_len
    while (i>0):
        print str1[:i]
        if str2.startswith(str1[:i]):
            break
        i-=1  
    print i    
    if i==0:
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

def group(path):
    folders=[]
    for root,dirs,files in os.walk(path,True):
        i=0
        file_count=len(files)
        while i<file_count:
            # print files[i]
            str1=files[i]
            print str1
            if validate(str1):                
                if len(folders)>0:
                    print folders
                    found=filter(lambda x:str1.startswith(x),folders)
                    if len(found)>0:
                        shutil.move(str1.encode('utf8'),os.path.join(root,found[0]))
                else:    
                    if i<file_count-1:   
                        str2=files[i+1]
                        if validate(str2):
                            comm_str=findCommStr(str1,str2)
                            print "comm: "+comm_str
                            if not comm_str==None:
                                folders.append(comm_str)
                                folder_path=os.path.join(root,comm_str)
                                print "创建文件夹: "+folder_path
                                if not os.path.exists(folder_path):
                                    os.mkdir(folder_path)
                                    shutil.move(str1.encode('utf8'),folder_path)
                                    shutil.move(str2.encode('utf8'),folder_path)
            i+=1

    
print findCommStr('塔克的郊外03.mp3','四月（小山雀的日历）.mp3')==None 
# if __name__ == "__main__":  
#     path = os.path.abspath('.')
#     group(path)  