#!/bin/bash

#####################################
#Component: Copy Services 
#Author: Lynn
#Date:2013.08.08
#####################################
# Create Consistency Group
if [ $1 -gt 0 ];then
echo "Create $1 consistency groups."
for((i=1;i<=$1;i++))
do
	svctask mkfcconsistgrp -name Auto_FCCG_$i
done
else
echo "There is $1 Consistency Group created."
fi

##############FC apping##############
#SnapShot fcmap
if [ $2 -gt 0 ];then
echo "Create $2 Flash Copy apping."
for((j=1;j<=$2;j++))
do
	svctask mkfcmap -cleanrate 0 -consistgrp Auto_FCCG_1 -copyrate 0 -source Auto_Volumes_Gen_$j -target Auto_Volumes_Gen_` expr $j + 1`
done
else
echo "There is $2 Flash Copy apping created."
fi

#Clone fcmap
#for((z=200;z<=300;z++))
#do
 #       svctask mkfcmap -autodelete -cleanrate 50 -consistgrp Auto_FVT_fccg_2 -copyrate 50 -source $z -target $(($z + 1))
#done

#Backup fcmap
#for((r=500;r<=600;r++))
#do
 #       svctask mkfcmap -cleanrate 50 -consistgrp Auto_FVT_fccg_3 -copyrate 50 -incremental -source $r -target $(($r + 1))
#done

################Start FlashCopy Consistency Group###############
svctask startfcconsistgrp -prep Auto_FCCG_1


##############Remote-Copy Consistency Group###############
# Create Remote-Copy consistency group
if [ $3 -gt 0 ];then
echo "Create $3 Remote-Copy consistency groups."
for((a=1;a<=$3;a++))
do
	svctask mkrcconsistgrp -name Auto_RCCG_$a
done
else
echo "There is $3 Remote Copy Consistency Group created."
fi


##############RC relationships###############
#Create etro irror remote copy relationship
if [ $4 -gt 0 ];then
echo "Create $4 remote copy metro mirror releationships."
for((b=1;b<=$4;b++))
do
	svctask mkrcrelationship -aux $b -cluster $5 -master $(($b + 1))
	svctask chrcrelationship -consistgrp Auto_RCCG_1 rcrel$b	
done
else
echo "There is $4 Remote Copy Releation ship created."
fi


################Start Remtoe Copy Consistency Group###############
svctask startrcconsistgrp Auto_RCCG_1



