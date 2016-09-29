#!/usr/bin/env python
# -*- coding: utf-8 –*-

import smtplib
from email.utils import COMMASPACE
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
 
def sendEmail(subject,body,from_email,to_emails,cc_emails):
	msg = MIMEMultipart('alternative')
	msg['Subject'] = subject
	msg['From'] = from_email 
	msg['To'] = COMMASPACE.join(to_emails)
	msg['Cc'] = COMMASPACE.join(cc_emails)
	part1 = MIMEText(body, 'html','utf-8')
	msg.attach(part1)
	to_emails=to_emails+cc_emails
	s = smtplib.SMTP('na.relay.ibm.com')
	s.sendmail(from_email, to_emails, msg.as_string())
	s.quit()

#sendEmail('python email','content','shenrui@cn.ibm.com','shenrui@cn.ibm.com')
