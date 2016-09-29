#!/bin/sh

work_dir=$(cd "$(dirname "$0")"; pwd)
iso_dir=$1
#version=$2
#iso_dir=/tmp/HMI/1.3.1.0-r91153M/SONAS-1.3.1.0-111218180546-r91153M.iso
n=`expr $iso_dir |cut -d'/' -f5|cut -d'-' -f3`
v=`expr $iso_dir |cut -d'/' -f5|cut -d'-' -f2`
nguirpm=sofs-ngui-$v-$n.noarch.rpm
echo $nguirpm
sofsngui_dir=/tmp/sofs-ngui

echo $sofsngui_dir

mkdir -p /mnt/disk
mount -o loop $iso_dir /mnt/disk
cp /mnt/disk/SoNAS/$nguirpm /tmp
umount /mnt/disk
rm -rf $sofsngui_dir; mkdir $sofsngui_dir
mv /tmp/$nguirpm $sofsngui_dir
cd $sofsngui_dir

$work_dir/rpm2cpio.sh $nguirpm | cpio -dimv
