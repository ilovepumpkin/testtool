#!/bin/sh

bdir=$1
echo $bdir
#ver=`echo $bdir | cut -d'/' -f4|cut -d'-' -f4|cut -d'.' -f1`
ver=`echo $bdir | cut -d'/' -f4|sed 's/.iso/ /g'`
echo $ver
echo $ver > $bdir/gui_version.txt
cd $bdir
zip SONAS_NGUI.war gui_version.txt
zip ifs.war gui_version.txt


