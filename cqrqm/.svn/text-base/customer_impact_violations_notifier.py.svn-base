#!/usr/bin/env python
from cq.cqlib import *
from config import *
from utils.emailutil import *

cq=CQTable(username,password,'37143020')
cq.run_query()
content=cq.to('html',excluded_cols=['SubmitterInfo.User_ID.email'])
emails=cq.get_emails('SubmitterInfo.User_ID.email')
#emails=['shenrui@cn.ibm.com']
print content
guide='For a sev1 or sev2 defect, don\'t use a customer impact lower than 650 - perm err/funct broken/job abend<br>For a sev 3 defect, don\'t use a customer impact higher than 650 - perm err/funct broken/job abend<br>For a sev 4 defect, don\'t use a customer impact higher than 520 - usability . . . if the problem is more serious than a usability problem, it should be sev 3<br>'
if len(content)>0:
	sendEmail('Customer Impact violations notification',guide+content,'shenrui@cn.ibm.com',emails,['shenrui@cn.ibm.com','wangnsh@cn.ibm.com'])


