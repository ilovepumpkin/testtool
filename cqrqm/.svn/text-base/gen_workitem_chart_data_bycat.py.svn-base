#!/usr/bin/env python
from rqm.rqmlib import *
from config import *

rqm=RQM()
rqm.projectAreaName=projectarea_name
rqm.login(username,password)
items=rqm.gen_report(testplan_name,iteration_name,True)
rqm.logout()

