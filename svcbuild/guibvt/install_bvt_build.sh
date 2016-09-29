#!/bin/sh

work_dir=$(cd "$(dirname "$0")"; pwd)
. $work_dir/config.sh

file_path=$1

full_bld_dir="$bld_dir/$build_type/$release"
latest_tested_file="$work_dir/latest_tested"

if [ ! $file_path = "" ];then
	latest_file_path=$file_path
else
	if [ ! -f $latest_tested_file ];then
		echo "[Error] $latest_tested_file does not exist."
		exit 2
	fi	

	latest_bld_dir=`ls -dt $full_bld_dir/*$1* |sort -r|head -n1`
	latest_file_path=`ls $latest_bld_dir/2076_*`
	if [ "$latest_file_path" = "" ]; then
		echo "[Error] Can not find the installation package under $full_bld_dir"	
		exit 2
	fi
	
	latest_tested=`cat $latest_tested_file`	
	latest_bld_version=`echo $latest_bld_dir|cut -d / -f5`
	if [ "$latest_tested" = "$latest_bld_version" ];then
		echo "[Error] $latest_bld_version was ever tested. Skip it."
		exit 2
	else
		echo "[Info] The build to be installed is $latest_bld_version."
		echo "$latest_bld_version" > "$latest_tested_file"	
	fi	
fi

$work_dir/../install/install_build.sh "$latest_file_path" $cluster_ip $node1_ip $node2_ip $install_useremails

