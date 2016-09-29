#!/bin/sh

work_dir=$(cd "$(dirname "$0")"; pwd)
iso_dir=$1
version=$2
#iso_dir=/tmp/HMI/1.3.0.0-40g/SONAS-1.3.0.0-40g-r79076.iso
n=`expr $iso_dir |cut -d'/' -f4|cut -d'-' -f2`
nguirpm=sofs-ngui-$version-$n.noarch.rpm
sofsngui_dir=`expr ${iso_dir%/*}`/sofs-ngui

echo $sofsngui_dir

mkdir -p /mnt/disk
mount -o loop $iso_dir /mnt/disk
cp /mnt/disk/SoNAS/$nguirpm /tmp
umount /mnt/disk
rm -rf $sofsngui_dir; mkdir $sofsngui_dir
mv /tmp/$nguirpm $sofsngui_dir
cd $sofsngui_dir

$work_dir/rpm2cpio.sh $nguirpm | cpio -dimv
