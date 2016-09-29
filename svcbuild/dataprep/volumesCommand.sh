#!/bin/bash

#####################################
#Component: Volumes
#Author: Lynn
#Date:2013.08.08
#####################################
# Generic Volume
if [ $1 -gt 0 ];then
echo "Create $1 generic volume."
for((i=1;i<=$1;i++))
do
	svctask mkvdisk -mdiskgrp Auto_mdiskgrp0 -iogrp 0 -size 1 -unit mb -name Auto_Volumes_Gen_$i
done
else
echo "there is no generic volume created."
fi

# Thin-provision Volume 
if [ $2 -gt 0 ];then
echo "Create $2 thin-provision volume."
for((j=1;j<=$2;j++))
do
	svctask mkvdisk -autoexpand -cache readwrite -copies 1 -grainsize 256 -iogrp io_grp0 -mdiskgrp Auto_mdiskgrp0 -name Auto_Volumes_thin_$j -rsize 2% -size 1 -syncrate 50 -unit mb -vtype striped -warning 80%
done
else
echo "there is no thin-provision volume created."
fi

# irror Volume
if [ $3 -gt 0 ];then
echo "Create $3 mirror volume."
for((a=1;a<=$3;a++))
do
	svctask mkvdisk -cache readwrite -copies 2 -iogrp io_grp0 -mdiskgrp Auto_mdiskgrp0:Auto_mdiskgrp0 -name Auto_Volumes_mirror_$a -size 1 -syncrate 50 -unit mb -vtype striped
done
else
echo "there is no mirror volume created."
fi

# Thin-irror Volume
if [ $4 -gt 0 ];then
echo "Create $4 thin-mirror volume."
for((b=1;b<=$4;b++))
do
	svctask mkvdisk -autoexpand -cache readwrite -copies 2 -grainsize 256 -iogrp io_grp0 -mdiskgrp Auto_mdiskgrp0:Auto_mdiskgrp0 -name Auto_Volumes_thinirror_$b -rsize 2% -size 1 -syncrate 50 -unit mb -vtype striped -warning 80%
done
else
echo "there is no thin-mirror volume created."
fi

# Compressed Volume
if [ $5 -gt 0 ];then
echo "Create $5 compressed volume."
for((c=1;c<=$5;c++))
do
	svctask mkvdisk -autoexpand -cache readwrite -compressed -copies 1 -iogrp io_grp0 -mdiskgrp Auto_mdiskgrp0 -name Auto_Volumes_Compressed_$c -rsize 2% -size 1 -syncrate 50 -unit mb -vtype striped -warning 80%
done
else
echo "there is no compressed volume created."
fi

# Volumes Copy(To Compressed Volumes)
#for((d=5;d<=$(($2));d++))
#do
#	svctask addvdiskcopy -autoexpand -compressed -mdiskgrp Auto_mdiskgrp -rsize 2% -warning 80% $d
#done
