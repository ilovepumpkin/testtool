#!/usr/bin/env python
from cq.cqlib import *
from utils.emailutil import *
from config import *

cq=CQTable(username,password,'37002843')
cq.run_query()
html=cq.to('html',excluded_cols=['Action'])

subject='SONAS/IFS P1 Defects'	
from_email='shenrui@cn.ibm.com'
to_emails=['shenrui@cn.ibm.com','wangnsh@cn.ibm.com']

#	for debugging	
#	to_emails=['shenrui@cn.ibm.com']	
#	cc_emails=[]


sendEmail(subject,html,from_email,to_emails,[])

