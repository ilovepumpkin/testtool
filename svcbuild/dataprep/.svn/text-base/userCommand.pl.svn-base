#!/bin/bash

#####################################
#Component: User 
#Author: Lynn
#Date:2014.06.11
#####################################

# Security Admin
if [ $1 -gt 0 ];then
echo "Create $1 security admin user."
for((i=1;i<=$1;i++))
do
	svctask mkuser -name Auto_Sec_$i -password l0destone -usergrp 0
done
fi


# Administrator
if [ $2 -gt 0 ];then
echo "Create $1 administrator user."
for((j=1;j<=$2;j++))
do
	svctask mkuser -name Auto_Adm_$j -password l0destone -usergrp 1
done
fi

# Copy Operator
if [ $3 -gt 0 ];then
echo "Create $1 copy operator user."
for((a=1;a<=$3;a++))
do
	svctask mkuser -name Auto_Copy_$3 -password l0destone -usergrp 2
done
fi

# Service
if [ $4 -gt 0 ];then
echo "Create $1 service user."
for((b=1;b<=$4;b++))
do
	svctask mkuser -name Auto_Service_$4 -password l0destone -usergrp 3
done
fi

# Monitor
if [ $5 -gt 0 ];then
echo "Create $1 monitor user."
for((c=1;c<=$5;c++))
do
	svctask mkuser -name Auto_Monitor_$5 -password l0destone -usergrp 4
done
fi


#User Group
if [ $6 -gt 0 ];then
echo "Create $1 user group."
for((d=1;d<=$6;d++))
do
	svctask mkusergrp -name Auto_UserGrp_$d -role Monitor
	svctask mkuser -name Auto_UserGrp_$d -password l0destone -usergrp Auto_UserGrp_1
done
fi

