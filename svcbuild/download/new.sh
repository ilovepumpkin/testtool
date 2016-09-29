#!/bin/sh
work_dir=$(cd "$(dirname "$0")"; pwd)
cd $work_dir
build_home="/build"
#./down_build.sh $build_home build,buildboxes lodestone730 2145,2076,2077,2072,2071,4939 "shenrui@cn.ibm.com,likezhao@cn.ibm.com,yechen@cn.ibm.com,youmiaoz@cn.ibm.com,bjlizhen@cn.ibm.com,jtingsh@cn.ibm.com,weishux@cn.ibm.com,zhuzhenq@cn.ibm.com"
#./down_build.sh $build_home build,buildboxes lodestone730 4939 likezhao@cn.ibm.com 140521
./down_build_64_bak_1008.sh $build_home buildboxes lodestone740 2145,2076 likezhao@cn.ibm.com 140924a
echo "exit code is $?"
