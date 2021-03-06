#!/bin/sh

node1_ip=$3
node2_ip=$4
cluster_ip=$2
file_path=$1
useremails=$5

bypassezsetup="0"

arr=(${file_path//\// })
file_name=${arr[${#arr[*]}-1]}
commonuirev_path=${file_path/$file_name/CommonUI.rev}
timeout_up=20

gwip=`echo $cluster_ip|awk '{gsub(/[0-9]+$/,"1");print}'`

cmd_reset="satask chenclosurevpd -reset"
cmd_mkcluster="satask mkcluster -clusterip $cluster_ip -mask 255.255.255.0 -gw $gwip"
cmd_chpwd="svctask chuser -password passw0rd superuser"
cmd_ezsetup_no="svctask chsystem -easysetup no"
cmd_restart_tomcat="satask restartservice -service tomcat"
cmd_getstatus="sainfo lsservicenodes"
cmd_getnodestatus="sainfo lsservicestatus|grep node_status"
cmd_version="cat /compass/version"
cmd_settimezone="svctask settimezone -timezone 246"
cmd_addenc="svctask chenclosure -managed yes 1"
cluster_url="https://$cluster_ip"
cmd_curl="curl -o /dev/null -s -w '%{http_code}' -k https://localhost --connect-timeout 300"


work_dir=$(cd "$(dirname "$0")"; pwd)

read_prodcode(){
	temp=$(echo "$1"|awk '{print substr($0,0,3)}')
	code=""
	if [ "$temp" = "IBM" ];then
		code=$(echo "$1"|awk '{print substr($0,4,4)}')	
	else
		code=$(echo "$1"|awk '{print substr($0,0,4)}')
	fi
	echo "$code"
}

check_prodcode(){
	if [ "$prodcode" = "2145" ];then
		timeout_up=30
	elif [ "$prodcode" = "2076" ];then
		timeout_up=20
	else
        	send_failure_email "$prodcode is not supported."
		exit 1
	fi
}

ensure_file_exists(){
	if [ ! -f $file_path ];then
		send_failure_email "$file_path does not exist."	
		exit 1
	fi	
}

install_node(){
	node_ip=$1
	file_path=$2
	arr=(${file_path//\// })
	file_name=${arr[${#arr[*]}-1]}

	$work_dir/sshcopyid.exp $node_ip
	echo_info "Copying $file_name to $node_ip ..."
	scp -P26 $file_path root@$node_ip:/upgrade

	if [ "$prodcode" = "2076" ];then
		ssh -p26 root@$node_ip $cmd_reset
	fi

	echo_info "Install $node_ip ..."        

        temp=$(echo "$file_name"|awk '{print substr($0,0,3)}')
        if [ "$temp" = "IBM" ];then	
		status="$(get_node_status $node_ip)"
		echo_info "node status is $status"
		if [ "$status" = "Active" ] || [ "$status" = "Starting"  ];then
			 echo_info "Leave cluster forcely ..."
			 if [ "$prodcode" = "2076" ];then
				 # V7000 will add the node automatically so here we have to make the other note leave cluster as well.
				 remote_cmd $node2_ip "satask leavecluster -force"	
				 remote_cmd $node_ip "satask leavecluster -force"	
			 else
			 	remote_cmd $node_ip "satask leavecluster -force" 			
			 fi
		         ensure_node_status $node_ip "Service"
			 remote_cmd $node_ip "satask stopservice" 			
		         ensure_node_status $node_ip "Candidate"
		elif [ "$status" = "Service" ];then
			 remote_cmd $node_ip "satask stopservice" 			
		         ensure_node_status $node_ip "Candidate"
		fi
		
		remote_cmd $node_ip "satask installsoftware -file /upgrade/$file_name -ignore"
	else
		remote_cmd $node_ip "scpinst -l /upgrade/$file_name"
	fi
}

is_connected(){
        rt=`$work_dir/sshcopyid.exp $1`
        found=`echo $rt | awk '{print index($0,"extra")}'`
	if [ "$found" = "0" ]
	then 
		return 1 
else
		return 0
	fi
}

is_not_connected(){
	is_connected $1
	if [ $? = 0 ];then
		return 1
	else
		return 0
	fi
}

send_email(){
	body=$2
	body=${body//\\n/<br>}
	$work_dir/../emailsender.py "$1" "$body" "$useremails" ""
}

send_failure_email(){
	echo_error "$1"
	send_email "Failed to install $file_name and  make cluster $cluster_ip" "$1"	
}

send_success_email(){
	send_email "Succeeded to install $file_name and make cluster $cluster_ip" "$1"
}

remote_cmd(){
	echo_info "Executing '$2' on $1 ..."
	ssh -p26 $1 $2
}

chserviceip(){
	remote_cmd $node1_ip "satask chserviceip -serviceip $node1_ip -gw $gwip -mask 255.255.255.0"
	remote_cmd $node2_ip "satask chserviceip -serviceip $node2_ip -gw $gwip -mask 255.255.255.0"
}

get_status(){
	max_try=5
	status="Unknown"
	while [ $max_try>0 ]
	do
		result="`ssh -p26 root@$1 sainfo lsservicenodes`"
		if [ "$result" = "CMMVC8035E The service assistant CLI is not ready - try again."  ]
		then
			sleep 60
			max_try=$(($max_try-1))
		else
			status=$result
			break	
		fi
	done
	
	if [ $max_try = 0 ]
	then
		echo_error "plmain didn't get up."
		exit 1
	else
		echo "$status"
	fi
}

echo_info(){
	echo -e "[Info] $1"
}

echo_error(){
	echo -e "[Error] $1"
}

mk_cluster(){
	echo_info "Making cluster $cluster_ip"
	if [ "$prodcode" = "2076"  ];then
		remote_cmd $1 "$cmd_reset"
	fi
	remote_cmd $1 "$cmd_mkcluster"
}

ensure_node_status(){
        echo_info "Waiting till $1 status turns to $2 ..."
	timeout_status=15
        timeout_minutes=$timeout_status
	loop_wait $timeout_minutes "compare_nodestatus" $1 $2
	if [ ! 0 = $? ]
	then
		msg="$1 status did not turn to $2 within $timeout_status minutes."
	        send_failure_email "$msg"
		exit 1
	else
		echo_info "$1 status is $2 as expected now"
	fi
}

loop_wait(){ 
	callback=$2
	nodeip=$3
	timeout_minutes=$1
	nodestatus=$4

        while [ "$timeout_minutes" -gt "0" ]
        do
                $callback $nodeip $nodestatus
                if [ 0 = $? ]
                then
                        break
                else
                        sleep 60
                        timeout_minutes=$(($timeout_minutes-1))
                        echo_info "$timeout_minutes minutes left"
                fi
        done

        if [ "$timeout_minutes" = "0" ];then
                return 1
        else
                return 0
        fi
}

compare_nodestatus(){
        node_status="$(get_node_status $1)"
        if [ $node_status = $2 ];then
		return 0;
	else
		return 1;
	fi 
}

ensure_node_up(){
	echo_info "Waiting for $1 becomes connected ..."
	timeout_minutes=$timeout_up
	loop_wait $timeout_minutes "is_connected" $1
	if [ ! 0 = $? ]
	then
		msg="$1 is not up within $timeout_up minutes."
	        send_failure_email "$msg"
		exit 1
	else
		echo_info "$1 is connected now"
	fi	
}

ensure_node_down(){
	echo_info "Waiting for $1 becomes disconnected ..."
	timeout_down=5
	timeout_minutes=$timeout_down
	loop_wait $timeout_minutes "is_not_connected" $1 
	if [ ! 0 = $? ]
	then
		msg="$1 is not down within $timeout_down minutes."
	        send_failure_email "$msg"
		exit 1
	else
		echo_info "$1 is disconnected now"
	fi	
}

get_node_status(){
	#status=$(remote_cmd $1 "$cmd_getnodestatus")
	status=$(ssh -p26 $1 "$cmd_getnodestatus")
	arr=(${status//\/ / })
	if [ ${#arr[*]} -gt 0 ];then
		echo "${arr[${#arr[*]}-1]}"
	else
		echo "Unknown"
	fi
}

handle_node_error(){
	status="$(get_node_status $1)"
        if [ ${status} != "Candidate"  ]
        then
 	        echo_info "$1 status is $status. Trying to reboot it ..."
                remote_cmd $1 "reboot"
		return 1	
	else
		return 0
        fi
}

wait_node_up(){
       	ensure_node_up "$1"
       	if [ $? = 1 ];then
                msg="$1 is not alive after rebooting."
	        send_failure_email "$msg"
                exit 1
        else
		exit 0
        fi
}

ensure_health(){
	echo_info "Verifying the nodes status become Active ..."

	ensure_node_status $node1_ip "Active"
	if [ $? != 0 ]
	then
		msg="After the cluster is made, $node1_ip status is not Active"
		send_failure_email "$msg"
		exit 1
	fi

	if [ "$prodcode" = "2145"  ];then
        	panelname="$(get_panelname $node2_ip)"
		remote_cmd $node1_ip "svctask addnode -iogrp 0 -panelname $panelname"
	fi

	ensure_node_status $node2_ip "Active" 
	if [ $? != 0 ]
	then
		msg="After the cluster is made, $node2_ip status is not Active"
		send_failure_email "$msg"
		exit 1
	fi
}

ensure_version_match(){
	bld_version=$(cat ${file_path/$file_name/version})
	echo_info "Verifying the cluster build version is $bld_version ..."
	#cluster_version=$(remote_cmd $cluster_ip "$cmd_version")	
	cluster_version=$(ssh -p26 $cluster_ip "$cmd_version")	
	echo_info "Expected build version: $bld_version"
	echo_info "Cluster build version: $cluster_version"
	if [ "$cluster_version" != "$bld_version" ];then
		msg="After the cluster is made, cluster version and build version mismatch. Cluster version is $cluster_version, build version is $bld_version."
		send_failure_email "$msg"
		exit 1
	fi
}

upload_commonuirev(){
	remote_path="/data"
	echo_info "Uploading CommonUI.rev to $1"
	#remote_cmd $1 "mount -o remount,rw -n $remote_path"
	scp -P26 "$commonuirev_path" $1:$remote_path
	#remote_cmd $1 "mount -o remount,ro -n $remote_path"
}

ensure_gui_up(){
        echo_info "Waiting till $cluster_url is up ..."
        timeout_minutes=10
        while [ "$timeout_minutes" -gt "0" ]
        do
		s=$(ssh -p26 $cluster_ip "$cmd_curl")
                if [ "$s" == "200" ] 
                then
                        echo_info "$cluster_url is up now"
                        break
                else
                        sleep 60
                        timeout_minutes=$(($timeout_minutes-1))
                        echo_info "$timeout_minutes minutes left"
                fi
        done

        if [ "$timeout_minutes" = "0" ];then
                return 1
        else
                return 0
        fi
}

get_panelname(){
        panelname="`ssh -p26 root@$1 sainfo lsservicenodes -nohdr|grep local|awk '{print $1}'`"
	echo $panelname
}

prodcode="$(read_prodcode $file_name)"
check_prodcode

echo_info "Install build on two nodes..."
ensure_file_exists
install_node $node1_ip $file_path
install_node $node2_ip $file_path
ensure_node_down "$node1_ip"
ensure_node_down "$node2_ip"
ensure_node_up "$node1_ip"
ensure_node_up "$node2_ip"

node1_reboot=1
node2_reboot=1

if [ $? = 1 ]; then
	send_failure_email "$node1_ip is not alive within the expected time."
	exit 1
else
	$work_dir/sshcopyid.exp $node1_ip
	upload_commonuirev $node1_ip
	
	ensure_node_status $node1_ip "Candidate" && ensure_node_status $node2_ip "Candidate"
	
	if [ 0 = $? ];then
		echo_info "Try to make cluster ..."
		mk_cluster $node1_ip
	else
		echo_info "Checking if node status is Candidate, reboot node if necessary ..."
		handle_node_error $node1_ip
		node1_reboot=$?
		
		handle_node_error $node2_ip
		node2_reboot=$?

		if [ "$node1_reboot" = "1" ];then
			ensure_node_down $node1_ip
		 	wait_node_up $node1_ip 
		fi
		if [ "$node2_reboot" = "1" ];then
			ensure_node_down $node2_ip
		 	wait_node_up $node2_ip
		fi

		echo_info "Try to make cluster again ..."	
		ensure_node_status $node1_ip "Candidate" && ensure_node_status $node2_ip "Candidate"

	        if [ 0 = $? ];then
        	        mk_cluster $node1_ip
		else
			status="$(get_status "$node1_ip")"
			msg="Not all nodes are in Candidate states so cluster cannot be made. \n $status"
			send_failure_email "$msg"
			exit 1	
		fi
	fi
fi

echo_info "Verifying the installation result..."
ensure_health
#ensure_version_match
chserviceip

$work_dir/sshcopyid.exp $cluster_ip

if [ "$bypassezsetup" = "0" ]
then
	echo_info "Bypassing the EZSetup ..."
	remote_cmd $cluster_ip "$cmd_chpwd"
	remote_cmd $cluster_ip "$cmd_ezsetup_no"
	remote_cmd $cluster_ip "$cmd_restart_tomcat"
	remote_cmd $cluster_ip "$cmd_settimezone"
	remote_cmd $cluster_ip "$cmd_addenc"
fi

ensure_gui_up
if [ $? != 0 ];then
	msg="$cluster_url did not become accessiable within the defined time limit."
        send_failure_email "$msg"
	exit 1
fi

echo_info "Sending success email ..."

note=""
if [ "$node1_reboot" = "0" ];then
	note="$note$node1_ip was ever rebooted\n"
fi
if [ "$node2_reboot" = "0" ];then
	note="$note$node2_ip was ever rebooted\n"
fi

if [ "$note" = "" ];then
	note="Note: \nNo nodes were ever rebooted"
else
	note="Note: \n$note"
fi

note="$note\nOpen the main GUI via <a href='$cluster_url' target='_blank'>$cluster_url</a>"

status="$(get_status "$cluster_ip")"
content="<pre>$status\n\n$note</pre>"
send_success_email "$content"
exit 0


