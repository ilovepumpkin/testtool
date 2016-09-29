#!/bin/sh 

echo "Build type: $BUILD_TYPE"
echo "Release: $RELEASE"
echo "Target dir: $TARGET_DIR"
echo "Log file: $LOG_FILE"

build_type=$BUILD_TYPE
release=$RELEASE
target_base_dir=$TARGET_DIR
work_dir=$(cd "$(dirname "$0")"; pwd)

buildnum=`$work_dir/getversion.sh`
echo ">>>>$buildnum"

if [ "$buildnum" = ""  ];then
	subject="The fetched latest build number is empty. Maybe the GSA account password is expired."	
	send_email "$subject" "" "shenrui@cn.ibm.com"
	exit 1
fi

target_dir="$target_base_dir/$build_type/$release/$buildnum"
mkdir -p "$target_dir"

down_file(){
	cd "$work_dir"
	file_path="$target_dir/$1"
	if [ ! -f $file_path ];then
		if [ "$RELEASE" = "lodestone740"  ];then
			gpg_dir="inst.images/svc22_64/shipdata"
		else
			gpg_dir="install/gpg"
		fi
		gpg_file="/$build_type/$release/$buildnum/$gpg_dir/$1"
		down_cmd="scp shenrui@bolborn.ssd.hursley.ibm.com:$gpg_file $target_dir"
		sshpass -f user.passwd $down_cmd

		md5_remote=$(sshpass -f user.passwd ssh shenrui@bolborn.ssd.hursley.ibm.com md5sum $gpg_file|awk '{print $1}')
		md5_local=$(md5sum $file_path|awk '{print $1}')
		echo "remote md5:$md5_remote"
		echo "local md5:$md5_local"
		if [ "$md5_remote" = "$md5_local" ];then
			subject="$file_path was downloaded successfully."
		else
			subject="$file_path was corrupted. Already delete it."			
			rm -rf $file_path
		fi
		send_email "$subject" "" "shenrui@cn.ibm.com"
	else
		echo "$file_path exists already. Skip the download."
	fi
}

send_email(){
	subject=$1
        body=$2
        body=${body//\\n/<br>}
	to="$3"
	echo $subject
        $work_dir/../emailsender.py "$subject" "$body" "$to" ""
}

delete_old(){
        cd "$target_base_dir/$build_type/$release"
        while [ `ls -d *|wc -l` -gt 3 ]
        do
                ls -d -r *|tail -1|xargs rm -rf
        done
}

delete_old
down_file "2076_$buildnum.tgz.gpg"
