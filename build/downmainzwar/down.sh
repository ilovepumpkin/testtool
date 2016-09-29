#!/bin/sh
work_dir=$(cd "$(dirname "$0")"; pwd)
build_dir='/tmp/Mainz/'

#versions="1.3.1.0 1.3.0.2"
versions="1.3.0.2"
for version in $versions
do
	echo Enter build directory $build_dir and start clean old builds

	cd $build_dir
	while [ `ls -d SONAS-$version-*|wc -l` -gt 3 ]
	do
		ls -d -r SONAS-$version-*|tail -1|xargs rm -rf
	done

	echo Start downloading build script
	/usr/local/bin/python2.7 $work_dir/down.py $build_dir $version
done

