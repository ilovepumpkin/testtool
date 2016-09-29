#!/bin/sh

work_dir=$(cd "$(dirname "$0")"; pwd)

echo entering the working directory $work_dir
cd $work_dir

echo start down.sh
#./down.sh | tee down.log
#./down.sh >  down.log 2>&1
./down.sh >  down.log 2>&1
