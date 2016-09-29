#!/bin/sh

work_dir=$(cd "$(dirname "$0")"; pwd)

build_dir=$1
release=$2
file_name=$3

latest=`$work_dir/getlatest.exp "$work_dir" $release|tail -n1`
latest=`echo $latest|awk '{print substr($0,0,length($0)-1)}'`
file_name=${file_name/<version>/$latest}
#file_name=`echo $file_name | sed 's/<version>/$latest/g'`
url="http://w3.ssd.hursley.ibm.com/build/$release/$latest/inst.images/default/shipdata/$file_name"
ver_url="http://w3.ssd.hursley.ibm.com/build/$release/$latest/inst.images/svc20/shipdata/compass/version"

latest_dir=$build_dir/$latest
latest_file_dir=$latest_dir/$file_name

send_email(){
	body=$2
	body=${body//\\n/<br>}
	$work_dir/../emailsender.py "$1" "$body" "shenrui@cn.ibm.com" ""
}

if [ -f "$latest_file_dir" ]
then
	echo "$latest_file_dir exists already. Skip the download."
	exit 1
else
	mkdir -p $latest_dir
	wget -P $latest_dir $url 	
	wget -P $latest_dir $ver_url
	
	content=""
	if [ -f "$latest_file_dir" ];then
		subject="$latest_file_dir was downloaded!"
		send_email "$subject" "$content"
		exit 0
	else
		subject="Failed to download $file_name!"
		send_email "$subject" "$content"
		exit 1 
	fi
fi

echo "Cleaning old builds ..."
cd $build_dir
	while [ `ls -d *|wc -l` -gt 3 ]
	do
		ls -d -t *|tail -1|xargs rm -rf
	done

