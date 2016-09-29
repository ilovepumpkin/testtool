#!/usr/bin/env python
from cq.cqlib import *
from utils.emailutil import *
from config import *
import sys
from utils.table import *
from utils.emailutil import *

NOT_CATEGORIZED='NotCategorized'
EXCLUDED_DEFECTS=['S1031627']

def unescape(xml):
        return xml.replace('&amp;','&').replace('&lt;','<').replace('&gt;','>').replace('&quot;','"').replace('&#039;',"'")

def print_items(rows,need_email,for_ifs):
        project='SONAS'
	if for_ifs:
		project='IFS'
	
	items=list()
	emails=set()
	for row in rows:	
		headline=unescape(row['Headline'])
		uid=row['Universal_Id']
		submitter=row['SubmitterInfo.Fullname_Login']
		submitter_name=submitter[0:submitter.find('(')]
		submitter_email=submitter[submitter.find('(')+1:len(submitter)-1]	
		owner=row['OwnerInfo.Fullname_Login']
		owner_name=owner[0:owner.find('(')]
		severity=row['Severity']
		priority=row['Priority']
		state=row['State']
		#print '%s	%s	%s	%s	%s' % (uid,headline,submitter_name,severity,state)
                item=[uid,headline,submitter_name,state,severity]
                items.append(item)
		emails.add(submitter_email)
        
        d=TableDisplayer([],items)
        output=d.format('text')
	print output
	#emails=['shenrui@cn.ibm.com']
	if need_email:
		print 'Sending email'
                html=d.format('html')
		sendEmail('['+project+'] Please set valid component prefix to your defects',html,'shenrui@cn.ibm.com',list(emails),['shenrui@cn.ibm.com','wangnsh@cn.ibm.com'])
		print 'Email sent'

def print_items_wiki(rows):
	line=''
	for row in rows:
                uid=row['Universal_Id']
                headline=unescape(row['Headline'])
                submitter=row['SubmitterInfo.Fullname_Login']
                submitter_name=submitter[0:submitter.find('(')]
                submitter_email=submitter[submitter.find('(')+1:len(submitter)-1]
                owner=row['OwnerInfo.Fullname_Login']
                owner_name=owner[0:owner.find('(')]
                severity=row['Severity']
                priority=row['Priority']
                state=row['State']
		line=line+uid+'	   '+headline+'<br>'
	print line


def print_sep(dot_str,width):
        line=''
        while width>=0:
            line=line+dot_str
            width=width-1
        print line

def doit(for_ifs,for_wiki):

	query_id='37015642'

        only_notcategorized=False

	if for_ifs:
		query_id='37082508'


	cats=['ACE','LocalAuthentication','Initialization','IPReport','AVT','Misc','UpgradeSoftware','V7k','NISBasic','SysLog','Overview','SystemsStatus','System','SystemDetails','Events','Performance','Capacity','FileSystems','Shares','FileSets','Snapshots','Quotas','BackupSelection','TSM','NDMP','Antivirus','Replication','Users','AuditLog','SMTP','Recipients','SNMP','DNS','ExtendedNIS','PDC','LDAP','AD','HTTP','NetworkGroups','PublicNetworks','NATGateway','CallHome','AOS','DateTime','DownloadLogs','CapacityPod','RunningTasksPod','HealthStatusPod','LoginPage','LandingPage','LowGraphicsMode','EZSetup',NOT_CATEGORIZED]
	
	comps=[]
	if len(sys.argv)>1:
 		temp=sys.argv[1]
		comps=temp.split(',')
	
	# validate the defined components
        for comp in comps:
		try:
			cats.index(comp)
		except:	
			sys.exit(comp+' is not a predefined component name.')

	if len(comps)>0:
            if len(comps)==1 and comps[0]==NOT_CATEGORIZED:
                only_notcategorized=True
            else:    
		cats=comps

	cq=ClearQuest()
	cq.login(username,password)
	rows=cq.query_defects(query_id)
	cq.logout()


	data={}
	for cat in cats:
		data[cat]=[]

	for row in rows:
		headline=row['Headline']
		uid=row['Universal_Id']
		if EXCLUDED_DEFECTS.count(uid)>0:
			continue
	
		pos=0
		if for_ifs:
                    if headline.startswith('GVT'):
			pos=2
                    else:
                        pos=1
                else:
                    if headline.startswith('GVT'):
                        pos=1

		d_cat='unknown'
		try:
			d_cat=headline.split(':')[pos].strip(' ')
		except:
			pass # it is possible that the submier does not include component prefix in defect
		
		if data.has_key(d_cat):
			data[d_cat].append(row)
		else:
			try:
				data[NOT_CATEGORIZED].append(row)
			except:
				pass # there will be no Other if the user privide the component list

	for key in sorted(data.keys()):
                if only_notcategorized and key!=NOT_CATEGORIZED:
                    continue 
                    
		items=data[key]
		if len(items)>0:
			print ''
			print '%s(%d)' % (key,len(items))
			print_sep('=',len(key)+4)
			if for_wiki:
				print_items_wiki(items)
			else:
				print_items(items,only_notcategorized,for_ifs)


