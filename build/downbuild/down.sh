#!/bin/sh
work_dir=$(cd "$(dirname "$0")"; pwd)
build_dir='/tmp/HMI/'

versions="1.3.2.3 1.4.2.0 1.5.0.0 1.4.1.0"

for version in $versions
do

	echo Enter build directory $build_dir and start clean old builds for $version

	cd $build_dir
	while [ `ls -d $version-*|wc -l` -gt 4 ]
	do
		ls -d -t $version-*|tail -1|xargs rm -rf
	done

	echo Start downloading build script for $version
	/usr/local/bin/python2.7 $work_dir/down.py $build_dir $version
done
