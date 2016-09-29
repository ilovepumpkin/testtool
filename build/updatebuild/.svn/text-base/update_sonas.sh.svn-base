#!/bin/sh

work_dir=$(cd "$(dirname "$0")"; pwd)
cd /tmp/Mainz
newest_build=`ls -dt $PWD/*$1* | head -n1`
echo The latest build is:$newest_build
war_path=$newest_build/SONAS_NGUI.war
cd $work_dir

./deploy_sonas.sh $war_path  mgmt001st001
./deploy_sonas.sh $war_path  mgmt001st002
