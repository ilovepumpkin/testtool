#!/bin/sh
down_build(){
#wget -P `pwd`  http://w3.ssd.hursley.ibm.com/build/lodestone740/140730/src/CommonUI/svn_revision
wget -P `pwd` http://w3.ssd.hursley.ibm.com/build/lodestone740/140730/log/svc21/BACKINGBUILD.log
download_PASS=$?
}
down_build
if [ $download_PASS -eq 0 ]
then
echo "errorlevel $download_PASS"
else
echo "$download fail"
fi

