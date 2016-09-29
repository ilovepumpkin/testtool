#!/usr/bin/env python
from mixreport import *
from config import *

reporter=Reporter(username,password)
report=reporter.propose_defect_fix_priority(testplan_name,iteration_name,'text')
print report
