#!/usr/bin/env python
from cq.cqlib import *
from utils.emailutil import *
from config import *
import sys

def unescape(xml):
        return xml.replace('&amp;','&').replace('&lt;','<').replace('&gt;','>').replace('&quot;','"').replace('&#039;',"'")

cq=ClearQuest()
cq.login(username,password)
qid='36687737'
rows=cq.query_defects(qid)
if len(rows)==0:
	sys.exit('there is no result')
else:
	submitters=set()
	
	for row in rows:
		headline=row['Headline']
		submitter=row['SubmitterInfo.Fullname_Login']
                submitter_name=submitter[0:submitter.find('(')]
		submitters.add(submitter_name)

	counter={}
	for name in submitters:
		sonas_name=name+'_sonas'
                ifs_name=name+'_ifs'
		counter[sonas_name]=0
		counter[ifs_name]=0

	sonas_total=0
	ifs_total=0
	for name in submitters:
		for row in rows:
			headline=row['Headline']
        	        submitter=row['SubmitterInfo.Fullname_Login']
                	submitter_name=submitter[0:submitter.find('(')]
	               	if name==submitter_name:
				sonas_name=name+'_sonas'
				ifs_name=name+'_ifs'
				if headline.startswith('IFS GUI:'):
					ifs_total=ifs_total+1
					counter[ifs_name]=counter[ifs_name]+1
				else: 
					sonas_total=sonas_total+1
                                        counter[sonas_name]=counter[sonas_name]+1
	html='<a href="https://tuccqweb.storage.tucson.ibm.com/cqweb/restapi/STGC_STORAGE/STORG/QUERY/'+qid+'?format=HTML&noframes=true" target="_blank">Click this link to look at your defects</a><br><br>'	
	summary='<table border="1"><tr bgcolor="yellow"><td>Tester</td><td>SONAS</td><td>IFS</td></tr>'
	for name in submitters:
		sonas_count=counter[name+'_sonas']
		ifs_count=counter[name+'_ifs']
		tr='<tr><td>'+name+'</td><td>'+str(sonas_count)+'</td><td>'+str(ifs_count)+'</td></tr>'
		summary=summary+tr
	summary=summary+'<tr><td>'+str(sonas_total+ifs_total)+'</td><td>'+str(sonas_total)+'</td><td>'+str(ifs_total)+'</td></tr>'
	summary=summary+'</table>'
	html=html+summary+'<br/>'

	header='<table border=1><tr bgcolor="yellow"><td>UniversalId</td><td>Headline</td><td>Submitter</td><td>Severity</td><td>State</td><td>Fixed in Revision</td><td>Fixed in Release</td></tr>'
#	header='<table border="1"><tr bgcolor="yellow"><td>UniversalId</td><td>Headline</td><td>Submitter</td><td>Severity</td><td>State</td></tr>'
	html=html+header
	to_emails=[]	
	for row in rows:
		uid=row['Universal_Id']
		headline=row['Headline']
		submitter=row['SubmitterInfo.Fullname_Login']
		submitter_name=submitter[0:submitter.find('(')]
		submitter_email=submitter[submitter.find('(')+1:len(submitter)-1]
		to_emails.append(submitter_email)	
		severity=row['Severity']
		state=row['State']
		action=row['Action']
                inrelease=row['Original_Release_Name']

		if action=='':
			action='&nbsp;'
		color='white'
		if state=='Rejected' or state=='MoreInfo':
			color='red'
		tr='<tr bgcolor="'+color+'"><td>'+uid+'</td><td>'+headline+'</td><td>'+submitter_name+'</td><td>'+severity+'</td><td>'+state+'</td><td>'+action+'</td><td>'+inrelease+'</td></tr>'
#		tr='<tr bgcolor="'+color+'"><td>'+uid+'</td><td>'+headline+'</td><td>'+submitter_name+'</td><td>'+severity+'</td><td>'+state+'</td></tr>'
		html=html+tr
	html=html+'</table>'
#	html=html.decode('utf-8')
#	html=html.encode('ascii','igonre')
#	print html
#	html=unescape(html)	
#	print html

	html='<html><head><meta content="text/html;charset=UTF-8" http-equiv="Content-Type"></head><body>'+html+'</body></html>'

	subject='You have SONAS/IFS defects to verify'	
	from_email='shenrui@cn.ibm.com'
	to_emails=list(set(to_emails))
	cc_emails=['shenrui@cn.ibm.com','wangnsh@cn.ibm.com']

#	for debugging	
#	to_emails=['shenrui@cn.ibm.com']	
#	cc_emails=[]


	sendEmail(subject,html,from_email,to_emails,cc_emails)

cq.logout()

