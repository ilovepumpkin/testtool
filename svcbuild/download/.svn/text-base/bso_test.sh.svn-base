#!/bin/sh
work_dir=$(cd "$(dirname "$0")"; pwd)
test_url="http://w3.ssd.hursley.ibm.com/hurssg/index.php"

resp=`curl $test_url`
email_to="shenrui@cn.ibm.com,likezhao@cn.ibm.com"

if [ "$resp" = "" ];then
        echo "send email"
        $work_dir/../emailsender.py "Hi honey, could you please help me pass the Hursley BSO on 9.123.196.241" ""  "$email_to" ""
	exit 1
else
        echo "BSO passed already"
	exit 0
fi
