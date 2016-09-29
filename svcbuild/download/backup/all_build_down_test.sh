#!/bin/sh

work_dir=$(cd "$(dirname "$0")"; pwd)
build_home="/SVC/build_auto"
cd $work_dir
./down_build.sh $build_home build,buildboxes lodestone730 2145,2076,2077,2072,2071,4939
echo $work_dir
echo $build_home
pwd
ls
./getlatest.exp /root/testtool/svcbuild/download/ build lodestone730
