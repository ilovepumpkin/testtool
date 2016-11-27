#!/bin/bash

dir=$1

if [ "$dir" = "" ];then
	echo "请指定目录名"
	exit 1
fi

mkdir -p "$dir"
echo "目录【$dir 】已创建"

ls -F | grep [^\/]$|grep "$dir"|xargs -i mv "{}" "$dir"
echo "故事已转移至目录【$dir】"
