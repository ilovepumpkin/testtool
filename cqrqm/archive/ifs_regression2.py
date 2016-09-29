#!/usr/bin/env python
from rqm.rqmlib import *
from config import *

testplan_name='IFS 1.2 GUI FVT'
iteration_name='Regression 2'

rqm=RQM()
rqm.login(username,password)
items=rqm.gen_report(testplan_name,iteration_name,False)
rqm.logout

