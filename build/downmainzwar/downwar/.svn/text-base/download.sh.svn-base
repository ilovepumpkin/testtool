#!/bin/sh

iso_url=$1
work_dir=$(cd "$(dirname "$0")"; pwd)
iso_name=`expr $iso_url |cut -d'/' -f7`
build_dir=/virtual/ISO
version=$2

echo $work_dir
echo $iso_name

rm -rf /tmp/sofs-ngui/*
rm -rf $build_dir/$iso_name

wget $1 -P $build_dir
$work_dir/extract_war.sh /virtual/ISO/$iso_name $version

