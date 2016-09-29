#!/bin/sh

work_dir=$(cd "$(dirname "$0")"; pwd)

echo "Build type: $BUILD_TYPE"
echo "Release: $RELEASE"
echo "Target dir: $TARGET_DIR"
echo "Log file: $LOG_FILE"
echo "Cluster IP: $CLUSTER_IP"
echo "Node1 IP: $NODE1_IP"
echo "Node2 IP: $NODE2_IP"

echo Entering the working directory $work_dir
cd $work_dir

# step: download
$work_dir/down.sh

# step: install
LASTEST_INSTALLED=".$CLUSTER_IP.latest"
BLACK_LIST=".$CLUSTER_IP.blacklist"
build_dir="$TARGET_DIR/$BUILD_TYPE/$RELEASE"
latest_build=`ls -t $build_dir|head -n1` 
latest_file="$build_dir/$latest_build/2076_$latest_build.tgz.gpg"
if [ ! -e "$LASTEST_INSTALLED" ];then
	touch "$LASTEST_INSTALLED"	
fi
if [ ! -e "$BLACK_LIST" ];then
        touch "$BLACK_LIST"
fi
latest_installed=`cat $LASTEST_INSTALLED`
echo $latest_installed

is_in_blacklist=`grep "$latest_file" $BLACK_LIST |wc -l`
if [ "$is_in_blacklist" = "1" ];then
	echo Skip installing because $latest_file was in the black list.	
	exit 1
fi

if [ "$latest_installed" != "$latest_file"  ];then
	echo Installing $latest_file on $CLUSTER_IP 
	/root/testtool/svcbuild/install/install_build.sh "$latest_file" "$CLUSTER_IP" "$NODE1_IP" "$NODE2_IP" shenrui@cn.ibm.com
	if [ $? = 0 ];then
		echo "$latest_file" > "$LASTEST_INSTALLED"
		exit 0
	else
		echo "The installation failed. Add the build name in the black list. Then reinstall the previous good build."
		echo "$latest_file" > "$BLACK_LIST"	
		/root/testtool/svcbuild/install/install_build.sh "$latest_installed" "$CLUSTER_IP" "$NODE1_IP" "$NODE2_IP" shenrui@cn.ibm.com
	fi
else
	echo Skip installing because $latest_file was already installed before.
	exit 1
fi
