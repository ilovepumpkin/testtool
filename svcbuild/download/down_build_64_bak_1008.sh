#!/bin/sh
# Version 20140414 Add another argument to send note
# Version 20140411
work_dir=$(cd "$(dirname "$0")"; pwd)
cd $work_dir
local_dir_home=$1
build_type=$2
release=$3
platform=$4
emails=$5
build_level=$6

arg_count=$#
send_mail_flag=0
bvt_ready_exit_flag=1

arr_build_type=(${build_type//,/ })
arr_release=(${release//,/ })
arr_platform=(${platform//,/ })
subject="[lodestone740] New Build (64bit) is downloaded to $local_dir_home"
content="<h4 align=\"center\"> ====PLS DO NOT REPLY TO THIS ID====</h4>"

echo "==========================================================================================================================="
echo "Usage:  ./down_build.sh [build_dir] [build_type] [release1,release2] [platform1,platform2] [emails] [(optional)build_level]"
echo ""
echo "Example ./down_build.sh `pwd` buildboxes lodestone740,lodestone730 2145,2076 user1@cn.ibm.com,user2@cn.ibm.com"
echo "==========================================================================================================================="
if [ $arg_count -lt 5 ]
      then
      echo "$0 $*"
      echo "ErrorMsg: The number of arguments is not enough!"
      exit 1
fi

send_email(){
	body=$2
	body=${body//\\n/<br>}
#	$work_dir/../emailsender.py "$1" "$body" "shenrui@cn.ibm.com,likezhao@cn.ibm.com,yechen@cn.ibm.com,youmiaoz@cn.ibm.com,bjlizhen@cn.ibm.com,jtingsh@cn.ibm.com,weishux@cn.ibm.com,zhuzhenq@cn.ibm.com" "likezhao@cn.ibm.com"
	if [ $send_mail_flag == 1 ]
		then
		$work_dir/../emailsender.py "$1" "$body" "$emails" ""
	else
		echo "No new build download, skip send mail!"
	fi
 #$work_dir/../emailsender.py "$1" "$body" "likezhao@cn.ibm.com" ""
}

down_build(){
	echo "Downloaing builds ..."
	build_dir=$1
	build_url=$2
	wget -P $build_dir $build_url
	DL_PASS_FLAG=$?
	}

clean_build(){
	echo "Cleaning old builds ..."
	clean_dir=$1
	retain_count=$2
	cd $clean_dir
        while [ `ls -d *|wc -l` -gt $retain_count ]
        do
                ls -d -t *|tail -1|xargs rm -rf
        done
}
check_md5sum(){
	downloadpath=$1
#	downloadpath="/SVC/build/730/buildbox/140331"
	checksumfile="${downloadpath}/md5sums"
	checksumfile_2="${downloadpath}/md5sum"
	if [ ! -f $checksumfile ] 
	then
		if [ ! -f $checksumfile_2 ]
		then
		log_mail_content "md5sum file doesn't exist,skip MD5check"
		return 0
		else 
		cp ${downloadpath}/md5sum ${downloadpath}/md5sums
		fi
	fi
	excludedfiles=(md5sums md5sum version BACKINGBUILD.log CommonUI.rev gui_svn_revision commonUI_svn_revision)
	for filename in `ls $downloadpath`; do
		echo "${excludedfiles[@]}"|grep -wqF "$filename" | head -n1 && continue
		md5sum=`cat $checksumfile | sed -n "/\${filename}/p"|awk '{print $1}'`
		result=`md5sum $downloadpath/$filename|awk '{print $1}'`
		if [ "$result" = "$md5sum" ]
			then
				log_mail_content "$filename passed MD5Checksum!" "NOT_SEND"
		else
				log_mail_content "$filename failed MD5Checksum!It was deleted automatically"
#				rm -f ${downloadpath}/$filename
				send_mail_flag=1
				bvt_ready_exit_flag=1
		fi
	done
	return 0
}

log_mail_content(){
	echo "$1"
	if [ "$2"x != "NOT_SEND"x ]
		then
		content="${content}\n$1"
	fi
}

get_latest(){
	if [ $arg_count == 6 ]
		then 
		latest=$build_level
	else
		latest=`$work_dir/getlatest.exp "$work_dir" $1 $2|tail -n1`
		latest=`echo $latest|awk '{print substr($0,0,length($0)-1)}'`
	fi
}

get_svc_version(){
svc_version=`$work_dir/getsvc.exp "$work_dir" $1 $2 $3 |tail -n1`
svc_version=`echo $svc_version|awk '{print substr($0,0,length($0)-1)}'`
}
 get_svn_revision (){
rm -rf $3/gui_svn_revision
rm -rf $3/commonUI_svn_revision
 svn_revision_gui_url="http://w3.ssd.hursley.ibm.com/build/$1/$2/src/gui/svn_revision"
 svn_revision_commonUI_url="http://w3.ssd.hursley.ibm.com/build/$1/$2/src/CommonUI/svn_revision"
 wget -P $3 $svn_revision_gui_url -O $3/gui_svn_revision
 wget -P $3 $svn_revision_commonUI_url -O $3/commonUI_svn_revision
 gui_svn_revision=`cat "$3/gui_svn_revision"`
 commonUI_svn_revision=`cat $3/commonUI_svn_revision`
}

echo "Main script is starting ... "

for i in ${arr_build_type[@]}
  do
	for j in ${arr_release[@]}
		do
			log_mail_content "<b><br> Build release: $j /$i<br></b>"
			get_latest $i $j
			get_svc_version $i $j $latest
			local_latest_dir=$local_dir_home/$i/$j/$latest"_64"
			mkdir -p $local_latest_dir
			get_svn_revision $j $latest $local_latest_dir
			log_mail_content "<i>GUI #SVN: $gui_svn_revision, CommonUI #SVN: $commonUI_svn_revision </i> <br>"

	    	for k in ${arr_platform[@]}
	       		do
		   			file_name=$k"_"$latest"_64.tgz.gpg"
					base_build_file_name=$latest"_64.tgz.gpg"
					 base_build_file_name_ug1=$latest"_64_ug1.tgz.gpg"
					file_name_ug1=$k"_"$latest"_64_ug1.tgz.gpg"
		   			latest_file=$local_latest_dir/$file_name
					latest_file_ug1=$local_latest_dir/$file_name_ug1
		   			url="http://w3.ssd.hursley.ibm.com/build/$j/$latest/inst.images/svc22_64/shipdata/$file_name"
					ug1_url="http://w3.ssd.hursley.ibm.com/build/$j/$latest/inst.images/svc22_64/shipdata/$file_name_ug1"
		   			md5_url="http://w3.ssd.hursley.ibm.com/build/$j/$latest/inst.images/svc22_64/shipdata/md5sums"
					md5_url_2="http://w3.ssd.hursley.ibm.com/build/$j/$latest/inst.images/svc22_64/shipdata/md5sum"
					base_build_file_name_url="http://w3.ssd.hursley.ibm.com/build/$j/$latest/inst.images/svc22_64/shipdata/$base_build_file_name"
					base_build_file_name_ug1_url="http://w3.ssd.hursley.ibm.com/build/$j/$latest/inst.images/svc22_64/shipdata/$base_build_file_name_ug1"
					version_url="http://w3.ssd.hursley.ibm.com/build/$j/$latest/inst.images/svc22_64/shipdata/compass/version"
					buildlog_url="http://w3.ssd.hursley.ibm.com/build/$j/$latest/log/$svc_version/BACKINGBUILD.log"
		   			if [ -f "$latest_file" ] ; then
								log_mail_content "${file_name} exists already. Skip the download"
		 			else
				 		mkdir -p $local_latest_dir
				 		down_build $local_latest_dir $url
					#	down_build $local_latest_dir $ug1_url
						if [ $DL_PASS_FLAG -eq 0 ]
							then
							log_mail_content "${file_name} downloaded successfully!"
					#		log_mail_content "${file_name_ug1} has been downloaded!"
							send_mail_flag=1
							bvt_ready_exit_flag=0
						else
						log_mail_content "${file_name} downloaded fail!"
						fi
					fi
				
					if [ -f "$latest_file_ug1" ] ; then
							log_mail_content "${file_name_ug1} exists already. Skip the download"
					else
						#mkdir -p $local_latest_dir
						down_build $local_latest_dir $ug1_url
						if [ $DL_PASS_FLAG -eq 0 ]
							then
							log_mail_content "${file_name_ug1} downloaded successfully!"
							send_mail_flag=1
						else
							log_mail_content "${file_name} downloaded fail!"
							send_mail_flag=1
						fi
					fi
				done	

 			if  [ -f "${local_latest_dir}/$base_build_file_name" ]
				then
					echo "$base_build_file_name exists, skip the download"
			else
				down_build $local_latest_dir $base_build_file_name_url
				if [ $DL_PASS_FLAG -eq 0 ] 
				then
					log_mail_content "${base_build_file_name} downloaded successfully!"
					send_mail_flag=1
				else
					log_mail_content "${file_name} downloaded fail!"
					send_mail_flag=1
				fi
			fi


		if  [ -f "${local_latest_dir}/$base_build_file_name_ug1" ]
			then
				echo "$base_build_file_name_ug1 exists, skip the download"
		else
		down_build $local_latest_dir $base_build_file_name_ug1_url
			if [ $DL_PASS_FLAG -eq 0 ]
				then
					log_mail_content "${base_build_file_name_ug1} downloaded successfully!"
			else
				log_mail_content "${base_build_file_name_ug1} downloaded fail!"
			fi
		fi

			if  [ -f "${local_latest_dir}/md5sums" ]  
				then
					echo "md5sums exists"
			else
				down_build $local_latest_dir $md5_url
				down_build $local_latest_dir $md5_url_2
			fi
		check_md5sum $local_latest_dir 
		    
			if  [ -f "${local_latest_dir}/version" ]
			   then
				      echo "version file exists"
		     else
			   down_build $local_latest_dir $version_url
			 fi

			if [ -f "${local_latest_dir}/CommonUI.rev" ]
				then
					echo "CommonUI.rev exists"
			else
				 echo "Get commonui version..."
			 	echo `$work_dir/getcommonuirev.exp $i $j $latest | tail -n1` > $local_latest_dir/CommonUI.rev
			fi

		if [ -f "${local_latest_dir}/BACKINGBUILD.log" ]
			then
				echo "BACKINGBUILD.log file exists"
			else
			 down_build $local_latest_dir $buildlog_url
		 fi

		clean_build $local_dir_home/$i/$j 10
	done
#		clean_build $local_dir_home/$i/$j 3
done

	send_email "$subject" "${content}" 
	exit $bvt_ready_exit_flag
