#!/usr/bin/env python
from cq.cqlib import *
from rqm.rqmlib import *
from config import *

national_day=5
mid_autumn=1

week_working_days=4
total_pts=110

'''
caculate the plan data
'''
date_util=DateUtil()
start_date=date_util.date('2013-7-15')
end_date=date_util.date('2013-11-29')
today=date_util.today()

total_days=(end_date-start_date).days
total_days=total_days/7*week_working_days+total_days%7+1-national_day-mid_autumn

passed_days=(today-start_date).days
passed_days=passed_days/7*week_working_days+passed_days%7+1

'''
caculate the actual data
'''
rqm=RQM()
rqm.projectAreaName=projectarea_name
rqm.login(username,password)
plan_uuid=rqm.get_testplan_uuid(testplan_name)
iteration_uuid=rqm.get_iteration_uuid(testplan_name,iteration_name)
total=rqm.get_execdata(plan_uuid,iteration_uuid)
rqm.logout()

done_pts=total[1]

print 'Planned Finished Rate:',round(100*float(passed_days)/float(total_days),0),'% (',passed_days,'/',total_days,')'
print 'Actual Finished Rate:',round(100*float(done_pts)/float(total_pts),0),'% (',done_pts,'/',total_pts,')'


