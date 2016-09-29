#!/usr/bin/python
# coding=utf-8
import simplejson as json
import urllib2, httplib2, urllib
import sys
import copy
import re

class ClearQuest:

    EQUALS=1
    NOT_EQUAL=2
    LESS_THAN=3
    LESS_THAN_OR_EQUAL_TO=4
    GREATER_THAN=5
    GREATER_THAN_OR_EQUAL_TO=6    
    CONTAINS=7
    NOT_CONTAIN=8
    BETWEEN=9
    NOT_BETWEEN=10
    IS_NULL=11
    IS_NOT_NULL=12
    IN=13
    NOT_IN=14

    def __init__(self,base_url,repository,database):
        self.base_url=base_url
        self.repository=repository
        self.database=database
        self.base_query_url=self.base_url+'/cqqueryresults.cq'

    def login(self,username,password):
        try:
            http= httplib2.Http(disable_ssl_certificate_validation=True)
            url = self.base_url+'/cqlogin.cq?action=DoLogin'
            body = {'loginId': username,'password': password,'repository':self.repository,'loadAllRequiredInfo':'true'}
            headers = {'Content-type': 'application/x-www-form-urlencoded'}
            response, content = http.request(url, 'POST', headers=headers, body=urllib.urlencode(body))
            self.set_cookie=response['set-cookie']
            self.cquid=re.search('JSESSIONID=([^,|.]*); Path=/$',self.set_cookie).group(1)
            self.headers={'Content-type': 'application/x-www-form-urlencoded','Cookie':self.set_cookie}
        except AttributeError as e:
            print e
            sys.exit('Fail to log in the Clear Quest. Please check the connectivity and ensure the credential is correct.')
    
    def logout(self):
	http= httplib2.Http(disable_ssl_certificate_validation=True)        
	url = self.base_url+'/cqlogin.cq?action=DoLogout'
        body={'cquid':self.cquid}
        response, content = http.request(url, 'POST', headers=self.headers, body=urllib.urlencode(body))
       

    def runquery(self,query_id,**kwargs):
        data=''
        if kwargs.has_key('params'):
            params=kwargs['params']
            data=json.dumps(params)

        res_id='cq.repo.cq-query:{0}@{1}/{2}'.format(query_id,self.repository,self.database) 
        body={'action':'ExecuteQuery','cquid':self.cquid,'data':data,'dojo.preventCache':'1307542089487','format':'JSON','refresh':'true','resourceId':res_id,'rowCount':1500,'startIndex':1}
        http= httplib2.Http(disable_ssl_certificate_validation=True) 
	response, content = http.request(self.base_query_url, 'POST', headers=self.headers, body=urllib.urlencode(body))
        jsonstr=json.loads(content)
        return jsonstr

    def cn_len(self,s):
        symbols=u'”“'
        cn_symbol_count=0
        for symbol in symbols:
            cn_symbol_count+=s.count(symbol)
        cn_c_count=len(s.encode('gbk'))-len(s)
        en_c_count=len(s)-cn_c_count
        cn_len=(cn_c_count-cn_symbol_count)*2+cn_symbol_count+en_c_count
        return cn_len

    def cn_ljust(self,string,width,fillchar):
        cn_len=self.cn_len(string)
        fill_str=''.join([fillchar for num in range(1,width-cn_len)])
        return string+fill_str

    def formatreport(self,jsonstr):
        resultset=jsonstr['resultSetData']
        coldata=resultset['colData']
        rowdata=resultset['rowData']
        repstr=''
        
        colnames=[]
        colfields=[]
        for col in coldata:
            colnames.append(col['name'])
            colfields.append(col['field'])

        rows=[]
        for row in rowdata:
            line=[]
            for field in colfields:
                line.append(self.unescape(row[field]))
            rows.append(line)    

        collens=[]
        tmplist=copy.deepcopy(rows)
        tmplist.insert(0,colnames)

        for i in xrange(len(colnames)):
            maxlen=0
            for tmprow in tmplist:
                tmplen=self.cn_len(tmprow[i])
                if tmplen>maxlen:
                    maxlen=tmplen
            collens.append(maxlen+4)

        for row in tmplist:
            for i in xrange(len(row)):
                repstr+=self.cn_ljust(row[i],collens[i],' ')
            repstr+='\n'

        return repstr


    def genreport(self,query_id,**kwargs):
        print self.formatreport(self.runquery(query_id,**kwargs))

    def unescape(self,astr):
        return astr.replace('&amp;','&').replace('&lt;','<').replace('&gt;','>').replace('&quot;','"').replace('&#039;',"'")



