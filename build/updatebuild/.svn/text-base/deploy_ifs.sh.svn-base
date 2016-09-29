#!/bin/bash

WAR_PATH=$1
MGMTNODE=$2

CLEAN=false

if [ -z "$WAR_PATH" ]; then 
    WAR_PATH=/opt/IBM/sonas/war/ifs.war
fi

if ! [ -f "$WAR_PATH" ]; then
    echo "WAR file $WAR_PATH not found!"
    exit 1;
fi

#Test if the script is running on the management node directly
if ! which lscluster &> /dev/null; then
	echo Copying the war to mgmt node
	scp -P1602 $WAR_PATH $MGMTNODE:/opt/IBM/sonas/war/ifs.war
	
	echo Copying self to mgmt node
	scp -P1602 $0 $MGMTNODE:/tmp 
	
	echo Running self on the mgmt node
	ssh -p1602 $MGMTNODE bash /tmp/$(basename $0)
	exit $?
fi

echo Deploying WAR from $WAR_PATH

rm -rf /opt/ibm/tomcat/webapps/ROOT*
rm -rf /opt/ibm/tomcat/work/Catalina/localhost/*
if $CLEAN; then
	echo Drop database schema
	su -l postgres -c '/usr/pgsql-9.0/bin/psql -d postgres -c "DROP SCHEMA FSCC CASCADE"'
fi
/etc/init.d/sofsgui restart
echo Sleep for 45 seconds
sleep 45

echo generating hmi_version.txt
get_version | cut -d':' -f2 > /opt/ibm/tomcat/webapps/ROOT/hmi_version.txt

if $CLEAN; then
	echo Recreate superman
	rmuser superman
	i=$(date +%Y%m%d%H%M%S)
	mkusergrp administrator_$i --role admin
	mkusergrp securityAdmin_$i --role securityadmin
	mkusergrp shareAdmin_$i --role exportadmin
	mkusergrp storageAdmin_$i --role storageadmin
	mkusergrp backupAdmin_$i --role service
	mkusergrp operator_$i --role monitor
	mkuser superman -p passw0rd -g administrator_$i,securityAdmin_$i,shareAdmin_$i,storageAdmin_$i,backupAdmin_$i,operator_$i 
fi

#Use this when you have an empty PostgreSQL database, after you installed the Sonas ISO
#echo Adding cluster using the mgmt node IP
#addcluster -h 172.31.136.2 -p test01
