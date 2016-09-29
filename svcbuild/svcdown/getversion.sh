#!/bin/sh

if [ "$RELEASE" = "lodestone740"  ];then
	sshpass -f user.passwd ssh shenrui@bolborn.ssd.hursley.ibm.com ls -t /$BUILD_TYPE/$RELEASE|awk '/^[0-9]+$/{print $1}'|sort|tail -n1
else
	sshpass -f user.passwd ssh shenrui@bolborn.ssd.hursley.ibm.com ls -t /$BUILD_TYPE/$RELEASE|awk '/^[0-9]+_[0-9]+$/{print $1}'|sort|tail -n1
fi

