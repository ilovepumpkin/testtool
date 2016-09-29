#!/bin/sh

if [ "$#" = "0" ];then
	echo "Usage: down2.sh <build conf> [cluster conf]"
	exit 1
elif [ "$#" = "1" ];then
	is_install="no"
elif [ "$#" = "2" ];then
	is_install="yes"
fi

work_dir=$(cd "$(dirname "$0")"; pwd)
echo Entering the working directory $work_dir
cd $work_dir

build_conf="$work_dir/$1"
. $build_conf
echo "Build type: $BUILD_TYPE"
echo "Release: $RELEASE"
echo "Target dir: $TARGET_DIR"
echo "Log file: $LOG_FILE"

if [ $is_install = "yes"  ];then
	cluster_conf="$work_dir/$2"
	. $cluster_conf
	echo "Cluster IP: $CLUSTER_IP"
	echo "Node1 IP: $NODE1_IP"
	echo "Node2 IP: $NODE2_IP"
	$work_dir/down_install.sh > "$LOG_FILE" 2>&1
else
	$work_dir/down.sh > "$LOG_FILE" 2>&1
fi

