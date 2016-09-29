#!/usr/bin/env python
from rqm.rqmlib import *
from config import *

testplan_name='DS8k 7.0 GUI FVT'
iteration_name='Sprint 1'

rqm=RQM()
rqm.projectAreaName='Unified GUI'
rqm.login(username,password)
items=rqm.gen_report(testplan_name,iteration_name,True)
rqm.logout

