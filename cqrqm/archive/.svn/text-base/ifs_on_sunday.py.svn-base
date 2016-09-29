#!/usr/bin/env python
from cq.cqlib import *
from config import *

date_util=DateUtil()
this_sunday=date_util.this_sunday()
last_sunday=date_util.last_sunday()
next_monday=date_util.next_monday()
today=date_util.today()
date_20110611=date_util.date('2011-6-11')


# Defect Discovery Rate
rep_params_1=ReportParams('Defect Discovery Rate','36649261',groupby_field='State',op='less_than',date1=next_monday)
# Defect By Severity Overtime
rep_params_2=ReportParams('Defect By Severity Overtime','36649242',groupby_field='Severity',op='between',date1=last_sunday,date2=this_sunday)
# Defect Backlog All Severity
rep_params_3=ReportParams('Defect Backlog All Severity','36649219',groupby_field='Severity',op='less_than',date1=next_monday)
# Defect Backlog By State
rep_params_4=ReportParams('Defect Backlog By State','36649225',groupby_field='State',op='less_than',date1=next_monday)
rep_params_5=ReportParams('Defect By Submitter Overtime','36649242',groupby_field='SubmitterInfo.Fullname_Login',op='between',date1=last_sunday,date2=this_sunday)

cq=ClearQuest()
cq.login(username,password)
# generating reports
cq.gen_report(rep_params_1)
cq.gen_report(rep_params_2)
cq.gen_report(rep_params_3)
cq.gen_report(rep_params_4)
cq.gen_report(rep_params_5)

cq.logout()




