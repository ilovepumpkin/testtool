#!/usr/bin/env python
import rqmlib

username='shenrui@cn.ibm.com'
password='yceny2qi'
testplan_name='SONAS 1.3 GUI FVT'
iteration_name='Sprint 11'

rqm=rqmlib.RQM()
rqm.login(username,password)
items=rqm.gen_report(testplan_name,iteration_name,True)
rqm.logout

