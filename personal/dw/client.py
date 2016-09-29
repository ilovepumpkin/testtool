#!/usr/bin/env python
# coding=utf-8
from cq import *

username='admin'
password=''

def main():
    cq=ClearQuest('http://9.186.97.61/cqweb','developerWorks','SAMPL')
    cq.login(username,password)
#    cq.genreport('33554747')
    cq.genreport('33554747',params=[{'fieldPath':'State','op':cq.IN,'valueList':['Resolved','Opened']},{'fieldPath':'Severity','op':cq.LESS_THAN,'valueList':['3 － 中等']}] )
    cq.logout()

if __name__ == "__main__":
    main()

