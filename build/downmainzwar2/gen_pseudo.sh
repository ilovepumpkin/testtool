#!/bin/sh

work_dir=$(cd "$(dirname "$0")"; pwd)
war_dir=$1
tmp_dir=/tmp/gvttmp
locale=zh_CN
files="Configuration Systems Home CommandParameters Remote Access RAS Config Global Files Monitor"

sonas_msg_dir=WEB-INF/classes/com/ibm/sonas/gui/msg
evo_msg_dir=WEB-INF/classes/com/ibm/evo/msg
svc_msg_dir=WEB-INF/classes/com/ibm/svc/gui/msg
ifs_msg_dir=WEB-INF/classes/com/ibm/ifs/gui/msg

msg_dirs="$sonas_msg_dir $evo_msg_dir "

# flag=0: sonas war file; flag=1: ifs war
flag=$(echo $war_dir | grep -qE 'SONAS_NGUI.war$' ; echo $?)
if [ $flag -eq 1 ];then
	echo "This is an IFS war file so add SVC message files directory"
	msg_dirs="$msg_dirs $svc_msg_dir $ifs_msg_dir"
fi


echo "Create $tmp_dir"
rm -rf $tmp_dir
mkdir -p $tmp_dir

echo "Extracting message files into $tmp_dir"
for msg_dir in $msg_dirs
do
	unzip $war_dir "$msg_dir/*.properties" -d $tmp_dir
done

echo "Tranlsating the message files"
for msg_dir in $msg_dirs
do
	for file in $tmp_dir/$msg_dir/*.properties
	do 
		flag=$(echo $file|grep -q  _;echo $?) 
		if [ $flag -eq 1 ];then 
			cd $work_dir
			java -cp RPX:RPX/rpx.jar Nw $file $locale
		fi
	done
done

echo "Adding the translated message files back to the war file"
cd $tmp_dir
for msg_dir in $msg_dirs
do
	zip $war_dir $msg_dir/*_$locale.properties
done
