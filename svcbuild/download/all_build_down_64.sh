#!/bin/sh
work_dir=$(cd "$(dirname "$0")"; pwd)
cd $work_dir
build_home="/build"
echo "Test Hursley BSO..."
./bso_test.sh
if [ $? = 1 ]
then
echo "BSO failed, mail has been sent!"
else
./down_build_64.sh $build_home buildboxes,build lodestone740 2145,2076,2077,2072,2071 "shenrui@cn.ibm.com,likezhao@cn.ibm.com,yechen@cn.ibm.com,youmiaoz@cn.ibm.com,bjlizhen@cn.ibm.com,shhull@cn.ibm.com,sxyu@cn.ibm.com,yugangsh@cn.ibm.com,wangnsh@cn.ibm.com,ddjie@cn.ibm.com" >>$work_dir/all_build_down.log
#./down_build.sh $build_home build,buildboxes lodestone730 2145,2076,2077,2072,2071,4939 likezhao@cn.ibm.com 140410
fi
