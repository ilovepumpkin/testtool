#!/usr/bin/env python
from cq.cqlib import *
from utils.emailutil import *
from config import *
import sys

def unescape(xml):
        return xml.replace('&amp;','&').replace('&lt;','<').replace('&gt;','>').replace('&quot;','"').replace('&#039;',"'")

cq=ClearQuest()
cq.login(username,password)
qid='37032836'
rows=cq.query_defects(qid)
if len(rows)==0:
	sys.exit('there is no result')
else:
	submitters=set()
        to_emails=[] 
	for row in rows:
		to_emails.append(row['SubmitterInfo.Internet_Email'])
		headline=row['Headline']
		submitter_name=submitter=str(row['SubmitterInfo.Fullname_Login'])
		if submitter.find('(')!=-1:
                	submitter_name=submitter[0:submitter.find('(')]
		submitters.add(submitter_name)

	counter={}
	for name in submitters:
		rejected_name=name+'_rejected'
                verify_name=name+'_verify'
                moreinfo_name=name+'_moreinfo'
		counter[rejected_name]=0
		counter[verify_name]=0
		counter[moreinfo_name]=0

	rejected_total=0
	verify_total=0
	moreinfo_total=0
	for name in submitters:
		for row in rows:
			state=row['State']
        	        submitter_name=submitter=row['SubmitterInfo.Fullname_Login']
                	if submitter.find('(')!=-1:
				submitter_name=submitter[0:submitter.find('(')]
	               	if name==submitter_name:
				rejected_name=name+'_rejected'
		                verify_name=name+'_verify'
                		moreinfo_name=name+'_moreinfo'
				if state=='Verify':
					verify_total=verify_total+1
					counter[verify_name]=counter[verify_name]+1
				elif state=='Rejected':
					rejected_total=rejected_total+1
					counter[rejected_name]=counter[rejected_name]+1
				elif state=='MoreInfo':
					moreinfo_total=moreinfo_total+1
					counter[moreinfo_name]=counter[moreinfo_name]+1
	html='<a href="https://tuccqweb.storage.tucson.ibm.com/cqweb/restapi/STGC_STORAGE/STORG/QUERY/'+qid+'?format=HTML&noframes=true" target="_blank">Click this link to look at your defects</a><br><br>'	
	summary='<table border="1"><tr bgcolor="yellow"><td>Submitter</td><td>Rejected</td><td>Verify</td><td>MoreInfo</td><td>Subtotal</td></tr>'
	for name in submitters:
		rejected_name=name+'_rejected'
                verify_name=name+'_verify'
	        moreinfo_name=name+'_moreinfo'

		rejected_count=counter[rejected_name]
		verify_count=counter[verify_name]
		moreinfo_count=counter[moreinfo_name]
		total_count=rejected_count+moreinfo_count+verify_count
		tr='<tr><td>'+name+'</td><td>'+str(rejected_count)+'</td><td>'+str(verify_count)+'</td><td>'+str(moreinfo_count)+'</td><td>'+str(total_count)+'</td></tr>'
		summary=summary+tr
	summary=summary+'<tr bgcolor="yellow"><td>Total</td><td>'+str(rejected_total)+'</td><td>'+str(verify_total)+'</td><td>'+str(moreinfo_total)+'</td><td>'+str(rejected_total+verify_total+moreinfo_total)+'</td></tr>'
	summary=summary+'</table>'
	html=html+summary+'<br/>'
      
#	header='<table border=1><tr bgcolor="yellow"><td>UniversalId</td><td>Headline</td><td>Submitter</td><td>Severity</td><td>State</td><td>Fixed In</td></tr>'
	header='<table border="1"><tr bgcolor="yellow"><td>UniversalId</td><td>Headline</td><td>Submitter</td><td>Severity</td><td>State</td></tr>'
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
		if action=='':
			action='&nbsp;'
		color='white'
		if state=='Rejected' or state=='MoreInfo':
			color='red'
#		tr='<tr bgcolor="'+color+'"><td>'+uid+'</td><td>'+headline+'</td><td>'+submitter_name+'</td><td>'+severity+'</td><td>'+state+'</td><td>'+action+'</td></tr>'
		tr='<tr bgcolor="'+color+'"><td>'+uid+'</td><td>'+headline+'</td><td>'+submitter_name+'</td><td>'+severity+'</td><td>'+state+'</td></tr>'
		html=html+tr
	html=html+'</table>'
#	html=html.decode('utf-8')
#	html=html.encode('ascii','igonre')
#	print html
#	html=unescape(html)	
#	print html

	html='<html><head><meta content="text/html;charset=UTF-8" http-equiv="Content-Type"></head><body>'+html+'</body></html>'
       
	subject='You have SONAS/IFS GUI defects in Verify/MoreInfo/Rejected - please take action ASAP. Thanks!'	
	from_email='shenrui@cn.ibm.com'
	to_emails=list(set(to_emails))
	cc_emails=['shenrui@cn.ibm.com','wangnsh@cn.ibm.com','sbaszyns@us.ibm.com','tniemeye@us.ibm.com','liuycdl@cn.ibm.com','ksperry@us.ibm.com']
	
#	print to_emails

#	for debugging	
#	to_emails=['shenrui@cn.ibm.com']	
#	cc_emails=[]

	sendEmail(subject,html,from_email,to_emails,cc_emails)

cq.logout()

