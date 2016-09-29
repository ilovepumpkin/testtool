#!/bin/bash

#####################################
#Component: Host 
#Author: Lynn
#Date:2013.08.20
#####################################

# FC Host
if [ $1 -gt 0 ];then
echo "Create $1 fc host."
for((i=1;i<=$1;i++))
do
	svctask mkhost -fcwwpn $i$(date +%N)$i$(($((RANDO%9000))+1000))$i -force -iogrp io_grp0:io_grp1:io_grp2:io_grp3 -name Auto_Host_FC_$i -type generic
done
else
echo "There is $1 FC host created."
fi

# iSCSI Host
if [ $2 -gt 0 ];then
echo "Create $2 iscsi host."
for((j=1;j<=$2;j++))
do
	svctask mkhost -iscsiname iqn.1994-05.com.redhat:uranus-$j -name Auto_Host_ISCSI_$j
done
else
echo "There is $2 ISCSI host created."
fi



# SAS Host
if [ $3 -gt 0 ];then
echo "Create $3 SAS host."
for((a=1;a<=$3;a++))
do
        svctask mkhost -saswwpn $a$(date +%N)$a$(($((RANDO%9000))+1000))$a -force -iogrp io_grp0 -name Auto_Host_SAS_$a -type generic
done
else
echo "There is $3 SAS host created."
fi


# Host - Vdisk appings
if [ $4 -gt 0 ];then
echo "Create $4 Host-Vdisk mapping."
for((b=1;b<=$4;b++))
do
	svctask mkvdiskhostmap -force -host 0 $b
done
else
echo "There is $4 Host-Vdisk apping."
fi


