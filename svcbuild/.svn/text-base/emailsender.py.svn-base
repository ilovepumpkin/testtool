#!/usr/local/bin/python2.7
#!/usr/bin/env python

import smtplib,sys
from email.utils import COMMASPACE
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# Usage example: ./emailsender.py "subject test" "content test" "shenrui@cn.ibm.com,zhqyz@cn.ibm.com" "shenrui@cn.ibm.com,zhqyz@cn.ibm.com"

 
def sendEmail(subject,body,from_email,to_emails,cc_emails):
	msg = MIMEMultipart('alternative')
	msg['Subject'] = subject
	msg['From'] = from_email 
	msg['To'] = COMMASPACE.join(to_emails)
	msg['Cc'] = COMMASPACE.join(cc_emails)
	part1 = MIMEText(body, 'html')
	msg.attach(part1)
	to_emails=to_emails+cc_emails
	s = smtplib.SMTP('9.56.224.216')
	s.sendmail(from_email, to_emails, msg.as_string())
	s.quit()

if __name__=="__main__":

	subject=sys.argv[1]
	html=sys.argv[2]
	to=sys.argv[3]
	cc=sys.argv[4]


	to_emails=to.split(",")
	cc_emails=cc.split(",")


	# send an E-mail
	from_email='storwize_gui_fvt@cn.ibm.com'
	sendEmail(subject,html,from_email,to_emails,cc_emails)
	print 'Notification email was sent'

