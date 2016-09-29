#!/usr/bin/env python
import simplejson as json
import urllib2, httplib2, urllib
import datetime
import sys
from utils.table import *

BASE_URL="https://tuccqweb.tucson.ibm.com/cqweb/"	

class ClearQuest:
    
    def __init__(self):
        self.op_dict={'less_than':'3','between':'9'}
        self.state_values=['Open','Assigned','MoreInfo','Rejected','Verify','Working','Closed']
        self.severity_values=['1','2','3','4']
	self.submitter_values=['Yu, Junji (junjiyu@cn.ibm.com)','Zhu, Zhen quan (zhuzhenq@cn.ibm.com)','Jiang, Ting (jtingsh@cn.ibm.com)','Shen, Rui (shenrui@cn.ibm.com)']
        
    def login(self,username,password):
        try:
            http= httplib2.Http(disable_ssl_certificate_validation=True)
            url = BASE_URL+'/cqlogin.cq?action=DoLogin'
            body = {'loginId': username,'password': password,'repository':'STGC_STORAGE','loadAllRequiredInfo':'true'}
            headers = {'Content-type': 'application/x-www-form-urlencoded'}
            response, content = http.request(url, 'POST', headers=headers, body=urllib.urlencode(body))
#            jsonstr=json.loads(content)
#            if jsonstr["status"]=='false':
#                sys.exit(jsonstr['message'])
            self.set_cookie=response['set-cookie']
            
            cquid=self.set_cookie[self.set_cookie.find(',')+1:]
            cquid=cquid[cquid.find('=')+1:]
            cquid=cquid[0:cquid.find(';')]
            self.cquid=cquid
        except AttributeError as e:
            sys.exit('Fail to log in the Clear Quest. Please check the connectivity and ensure the credential is correct.')
    
    def logout(self):
	http= httplib2.Http(disable_ssl_certificate_validation=True)        
	url = BASE_URL+'/cqlogin.cq?action=DoLogout'
        headers = {'Content-type': 'application/x-www-form-urlencoded','Cookie':self.set_cookie}
        body={'cquid':self.cquid}
        response, content = http.request(url, 'POST', headers=headers, body=urllib.urlencode(body))
        
        
    def group_by(self,elems,groupby_field,values):
 	counts={}
        for val in values:
            counts[val]=0
        
        for elem in elems:
            field_value=elem[groupby_field]
            for val in values:
                if field_value==val:
                    counts[val]=counts[val]+1
        return counts

    def query_defects(self,query_id):
	headers = {'Content-type': 'application/x-www-form-urlencoded;charset=UTF-8','Cookie': self.set_cookie}
	url= BASE_URL+'/cqqueryresults.cq'
        body={'action':'ExecuteQuery','cquid':self.cquid,'dojo.preventCache':'1307542089487','format':'JSON','refresh':'true','resourceId':'cq.repo.cq-query:'+query_id+'@STGC_STORAGE/STORG','rowCount':1500,'startIndex':1}

        http= httplib2.Http(disable_ssl_certificate_validation=True)
        response, content = http.request(url, 'POST', headers=headers, body=urllib.urlencode(body))
        jsonstr=json.loads(content)
#        total_num=jsonstr['resultSetData']['totalNumOfRows']
        rowData=jsonstr['resultSetData']['rowData']
	return rowData	
    

    def run_query(self,query_id):
        '''
        stardard method to execute a Clear Quest query and return a whole resutl set
        '''
	headers = {'Content-type': 'application/x-www-form-urlencoded;charset=UTF-8','Cookie': self.set_cookie}
	url= BASE_URL+'/cqqueryresults.cq'
        body={'action':'ExecuteQuery','cquid':self.cquid,'dojo.preventCache':'1307542089487','format':'JSON','refresh':'true','resourceId':'cq.repo.cq-query:'+query_id+'@STGC_STORAGE/STORG','rowCount':1500,'startIndex':1}

        http= httplib2.Http(disable_ssl_certificate_validation=True)
        response, content = http.request(url, 'POST', headers=headers, body=urllib.urlencode(body))
        jsonstr=json.loads(content)
        return jsonstr

    '''
    query a defect by its ID	
    '''	   			
    def get_defect2(self,defect_id):
	headers = {'Content-type': 'application/x-www-form-urlencoded','Cookie': self.set_cookie}
        url=BASE_URL+'/cqqueryresults.cq'

	valueList='["'+defect_id+'"]'
	query_id='36979536'

        data='[{"fieldPath": "Universal_Id", "op": 7, "valueList": '+valueList+', "fieldType": "DATE_TIME", "prompt": "Enter: Open_Date", "displayName": "Open_Date", "choiceListInfo": null}]'
        body={'action':'ExecuteQuery','cquid':self.cquid,'data':data,'dojo.preventCache':'1307542089487','format':'JSON','refresh':'true','resourceId':'cq.repo.cq-query:'+query_id+'@STGC_STORAGE/STORG','rowCount':1500,'startIndex':1}

        http= httplib2.Http(disable_ssl_certificate_validation=True)
        response, content = http.request(url, 'POST', headers=headers, body=urllib.urlencode(body))
        jsonstr=json.loads(content)    
	rowData=jsonstr['resultSetData']['rowData']
	return rowData[0]        
        
    '''
    query a defect by its Universal ID    
    '''                         
    def get_defect3(self,defect_id):
        headers = {'Content-type': 'application/x-www-form-urlencoded','Cookie': self.set_cookie}
        url=BASE_URL+'/cqqueryresults.cq'

        valueList='["'+defect_id+'"]'
        query_id='34644233'

        data='[{"fieldPath": "Universal_Id", "op": 7, "valueList": '+valueList+', "fieldType": "DATE_TIME", "prompt": "Enter: Open_Date", "displayName": "Open_Date", "choiceListInfo": null}]'
        body={'action':'ExecuteQuery','cquid':self.cquid,'data':data,'dojo.preventCache':'1307542089487','format':'JSON','refresh':'true','resourceId':'cq.repo.cq-query:'+query_id+'@STGC_STORAGE/STORG','rowCount':1500,'startIndex':1}

        http= httplib2.Http(disable_ssl_certificate_validation=True)
        response, content = http.request(url, 'POST', headers=headers, body=urllib.urlencode(body))
        jsonstr=json.loads(content)    
        rowData=jsonstr['resultSetData']['rowData']
        return rowData[0]  

    def gen_report(self,report_params):
        groupby_field=report_params.groupby_field
        if groupby_field=='Severity':
            values=self.severity_values
        elif groupby_field=='State':
            values=self.state_values
	elif groupby_field=='SubmitterInfo.Fullname_Login':
	    values=self.submitter_values   

	groupby_values=report_params.groupby_values
	if groupby_values:
	    values=groupby_values
 
        headers = {'Content-type': 'application/x-www-form-urlencoded','Cookie': self.set_cookie} 
        url=BASE_URL+'/cqqueryresults.cq'
        
        op_int=self.op_dict[report_params.op]

	date_format='%Y-%m-%d'
        
        if op_int=='3':
            valueList='["'+str(report_params.date1.strftime(date_format))+'"]'
        elif op_int=='9':
            valueList='["'+str(report_params.date1.strftime(date_format))+'","'+str(report_params.date2.strftime(date_format))+'"]'
        
        data='[{"fieldPath": "Open_Date", "op": '+op_int+', "valueList": '+valueList+', "fieldType": "DATE_TIME", "prompt": "Enter: Open_Date", "displayName": "Open_Date", "choiceListInfo": null}]'
        body={'action':'ExecuteQuery','cquid':self.cquid,'data':data,'dojo.preventCache':'1307542089487','format':'JSON','refresh':'true','resourceId':'cq.repo.cq-query:'+report_params.query_id+'@STGC_STORAGE/STORG','rowCount':1500,'startIndex':1}
        
        http= httplib2.Http(disable_ssl_certificate_validation=True) 
	response, content = http.request(url, 'POST', headers=headers, body=urllib.urlencode(body))
        jsonstr=json.loads(content)
        total_num=jsonstr['resultSetData']['totalNumOfRows']
        rowData=jsonstr['resultSetData']['rowData']
        dataset=self.group_by(rowData,groupby_field,values)
        self.format_report(report_params,dataset,total_num,groupby_field)
   
    def print_seperator(self, dot_str,width):
        line=''
        while width>=0:
            line=line+dot_str
            width=width-1
        print line
     
        
    def format_report(self,report_params,dataset,total_num,groupby_field):
       
	label_width = len(groupby_field)
	for key in dataset.keys():
		if len(key)>label_width:
			label_width=len(key)
	label_width=(label_width/8+1)*8

	total_width=label_width+len('Count')
	if len(report_params.title)>total_width:
		total_width=len(report_params.title)

	self.print_seperator('=',total_width)
        print '%s' % report_params.title
	self.print_seperator('=',total_width)
        print 'op: %s' % report_params.op
        print 'date1: %s' % report_params.date1
        print 'date2: %s' % report_params.date2
	self.print_seperator('-',total_width)
	
 
        print  groupby_field.ljust(label_width)+'Count'
	self.print_seperator('-',total_width)

        for key in sorted(dataset.keys()):
            print key.ljust(label_width)+str(dataset[key])
            
	self.print_seperator('-',total_width)
        print 'Total'.ljust(label_width)+str(total_num)
        
    def basic_login(self, username, password):
        url=BASE_URL+'/oslc/repo/STGC_STORAGE/db/STORG/record'
        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, url, username, password)
        authhandler = urllib2.HTTPBasicAuthHandler(passman)
        opener = urllib2.build_opener(authhandler)
        urllib2.install_opener(opener)
        
    def get_defect(self,defect_id):
        url=BASE_URL+'/oslc/repo/STGC_STORAGE/db/STORG/record/16777272-'+defect_id+'?rcm.contentType=application/json&oslc_cm.properties=Headline,State,id,Universal_Id,OwnerInfo,Severity,Component_Name,State'
        handle = urllib2.urlopen(url)
        jsonstr=json.loads(self.unescape(handle.read()))
        return jsonstr
    def unescape(self,astr):
        return astr.replace('&amp;','&').replace('&lt;','<').replace('&gt;','>').replace('&quot;','"').replace('&#039;',"'")

class ReportParams:
    def __init__(self,title,query_id,**kwargs):
            self.title=title
            self.query_id=query_id
            self.groupby_field=kwargs['groupby_field']
            self.op=kwargs['op']
            self.date1=kwargs['date1']
	    if kwargs.has_key('date2'):	
            	self.date2=kwargs['date2']
	    else:
		self.date2=None	
	    if kwargs.has_key('groupby_values'):
		self.groupby_values=kwargs['groupby_values'] 	
	    else:
		self.groupby_values=None
            if self.op=='between' and self.date2==None:
                sys.exit('The operator "between" requires two dates.')
            	   
class DateUtil:
    def today(self):
        return datetime.datetime.today()
        
    def this_monday(self):
        return self.today() + datetime.timedelta(self.today().weekday())
        
    def next_monday(self):
        return self.today() + datetime.timedelta(7-self.today().weekday())
        
    def this_sunday(self):
        return self.today() + datetime.timedelta(6-self.today().weekday())
        
    def last_sunday(self):
        return self.this_sunday()-datetime.timedelta(7)
    
    def last_sunday_2(self):
        return self.this_sunday()-datetime.timedelta(14)
        
    def date(self,date_str):
        return datetime.datetime.strptime(date_str,'%Y-%m-%d')
        

class CQTable:
    model=None

    def __init__(self,username,password,query_id):
        self.username=username
        self.password=password
        self.query_id=query_id

    def run_query(self):
        cq=ClearQuest()
        cq.login(self.username,self.password)
        self.model=CQTableModel(cq.run_query(self.query_id))
        cq.logout()

    def to(self,o_type,**kwargs):
        m=self.model
        if kwargs.has_key('excluded_cols'):
            m.set_excluded_cols(kwargs['excluded_cols'])
        displayer=TableDisplayer(m.get_colnames(),m.get_rows())
        return displayer.format(o_type)
    
    def get_emails(self,emailcol):
        m=self.model
        return m.get_emails(emailcol)

class CQTableModel:
    excluded_cols=list()
    rowdata=None
    coldata=None
	

    def __init__(self,json):
        self.jsondata=json
        self.rowdata=self.jsondata['resultSetData']['rowData']
        self.coldata=self.jsondata['resultSetData']['colData']

    def get_emails(self,emailcol):
        emails=set()
        for row in self.rowdata:
            emails.add(row[emailcol])
        return list(emails)    

    def set_excluded_cols(self,excluded_cols):
        self.excluded_cols=excluded_cols

    def __is_excluded__(self,colname):
        try:
            self.excluded_cols.index(colname)
        except:
            return False
        return True

    def get_colnames(self):
        colnames=list()
        for col in self.coldata:
            colname=col['field']
            if not self.__is_excluded__(colname):
                colnames.append(colname)
        return colnames

    def get_rows(self):
        colnames=self.get_colnames()
        rows=list()
        for line in self.rowdata:
            row=list()
            for colname in colnames:
                row.append(self.unescape(line[colname]))
            rows.append(row)    
        return rows


    def unescape(self,astr):
        return astr.replace('&amp;','&').replace('&lt;','<').replace('&gt;','>').replace('&quot;','"').replace('&#039;',"'")
