#!/bin/sh

work_dir=$(cd "$(dirname "$0")"; pwd)
cd /tmp/Mainz
newest_build=`ls -dt $PWD/*$1* | head -n1`
echo The latest build is:$newest_build
war_path=$newest_build/ifs.war
cd $work_dir

./deploy_ifs.sh $war_path  9.123.196.232
./deploy_ifs.sh $war_path  9.123.196.237
