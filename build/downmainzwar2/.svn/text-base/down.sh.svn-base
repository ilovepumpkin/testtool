#!/bin/sh
work_dir=$(cd "$(dirname "$0")"; pwd)
build_dir='/tmp/Mainz/'
username='shenrui@cn.ibm.com'
password='wbm4rycw'

#pass Mainz firewall
#/root/testtool/personal/firewall/ssh_pass.exp a2t-c-ssh.mainz.de.ibm.com $username $password


versions="1.4.2.0 1.5.0.0"
for version in $versions
do
	echo Enter build directory $build_dir and start clean old builds

	cd $build_dir
	while [ `ls -d SONAS-$version-*|wc -l` -gt 3 ]
	do
		ls -d -r SONAS-$version-*|tail -1|xargs rm -rf
	done

	echo Start downloading build script
	/usr/local/bin/python2.7 $work_dir/down.py $build_dir $version $username $password
done

