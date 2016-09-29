#!/usr/bin/env python
from __future__ import division
from rqm.rqmlib import *
from config import *
from mixreport import *
from cq.cqlib import *

myfilter={'testPlanName':'SONAS 1.3 SLT Plan'}

reporter=Reporter(username,password)

cq=ClearQuest()
cq.login(username,password)

rqm=RQM()
rqm.login(username,password)
ers=rqm.query_execrecords(myfilter)

total_points=0
total_passed=0
total_failed=0
total_inprogress=0
total_blocked=0
total_retest=0
total_permfailed=0
total_deferred=0
total_avail_for_retest=0
avail_for_retest=0

for er in ers:
  if re.search("GUI", er['name']):
    total_points=total_points+1
    if 'currentResultItemId' in er:
        stateName=er['currentResultStateName']
        if stateName == 'Passed':
          total_passed=total_passed+1
        if stateName == 'Failed':
          total_failed=total_failed+1
        if stateName == 'PermFailed':
          total_permfailed=total_permfailed+1
        if stateName == 'Retest':
          total_retest=total_retest+1
        if stateName == 'In Progress':
          total_inprogress=total_inprogress+1
        if stateName == 'Deferred':
          total_deferred=total_deferred+1
        if stateName == 'Blocked':
          total_blocked=total_blocked+1

        if stateName == 'Blocked' or stateName == 'Failed':
          lastresult=rqm.get_lastresult(er['currentResultItemId'])
          if 'defects' in lastresult:
            avail_for_retest=1
            defects=lastresult['defects']
            defect_list=[]
            for defect in defects:
                defecturl=defect['workItem']['itemId']
                defect_id=defecturl[defecturl.index('-')+1:]
                defect_id=reporter.dbid2id(defect_id)
                defect_list.append(cq.get_defect2(defect_id))
                defects=defect_list
            for defect in defects:
                defect_id=defect['Universal_Id']
                defect_state=defect['State']
                defect_headline=defect['Headline']
                if defect_state == 'Open' or defect_state == 'Assigned' or defect_state == 'Working' or defect_state == 'MoreInfo':
                    avail_for_retest=0

          total_avail_for_retest=total_avail_for_retest+avail_for_retest
          if avail_for_retest == 1:
            if total_avail_for_retest == 1:
              print 'List of failed or blocked ERs without active defects'
            print '%s\t%s' % (total_avail_for_retest,er['name'])

print
print 'Total\tPassed\tFailed\tPFail\tInProg\tDefer\tBlock\tRetest'
print '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (total_points,total_passed,total_failed,total_permfailed,total_inprogress,total_deferred,total_blocked,total_retest)
print ' \t{:.0%}\t{:.0%}\t{:.0%}\t{:.0%}\t{:.0%}\t{:.0%}\t{:.0%}'.format(total_passed/total_points,total_failed/total_points,total_permfailed/total_points,total_inprogress/total_points,total_deferred/total_points,total_blocked/total_points,total_retest/total_points)

success_rate=total_passed/(total_points-total_deferred)
success_rate_retest=(total_passed+total_retest+total_avail_for_retest+total_inprogress)/(total_points-total_deferred)

print
print 'Success rate is {:.0%}'.format(success_rate)
print '%s failed or blocked ERs have no associated active defects' % total_avail_for_retest
print 'Success rate after retest could be {:.0%}'.format(success_rate_retest)

rqm.logout()
