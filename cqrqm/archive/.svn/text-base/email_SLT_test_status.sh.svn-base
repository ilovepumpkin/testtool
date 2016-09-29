#!/bin/sh

work_dir=$(cd "$(dirname "$0")"; pwd)
#work_dir=D:/opt/cygwin/home/ilovepumpkin/testtool/cqrqm

#cd $work_dir

report=$($work_dir/SLT_test_status2.py)
report="<pre>$report</pre>"

# emailutil.py	<subjec>  <body>  <from>  <to>  <cc>
to=shenrui@cn.ibm.com,wangnsh@cn.ibm.com,zhuzhenq@cn.ibm.com,tniemeye@us.ibm.com,sbaszyns@us.ibm.com
#to=shenrui@cn.ibm.com
$work_dir/utils/emailutil.py "SLT test status" "$report" "shenrui@cn.ibm.com" "$to" ""


