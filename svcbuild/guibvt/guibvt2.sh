#!/bin/sh

work_dir=$(cd "$(dirname "$0")"; pwd)
log_file=$work_dir/guibvt.log
. $work_dir/config.sh

$work_dir/guibvt.sh > $log_file 

ts=`date "+%Y-%m-%d %H:%M:%S"`
cp $log_file "$work_dir/logs/guibvt.log.$ts"

#bld=`cat $work_dir/latest_tested`
#report_dir="/root/guibvtreports/$release-$bld $ts"
#mkdir -p "$report_dir"
#cp $log_file "$report_dir"
#scp -r Ting@9.125.92.33:/cygdrive/c/guibvt/reports "$report_dir"
#scp -r Ting@9.125.92.33:/cygdrive/c/guibvt/logs "$report_dir"
