#!/bin/sh

work_dir=$(cd "$(dirname "$0")"; pwd)
. $work_dir/config.sh

cluster_url="https://$cluster_ip"
cmd_curl="curl -k $cluster_url --connect-timeout 300"

echo_info(){
	echo -e "[Info]$1"
}
ensure_gui_up(){
        echo_info "Waiting till $cluster_url is up ..."
        timeout_minutes=10
        while [ "$timeout_minutes" -gt "0" ]
        do
		s="$($cmd_curl)"
                if [ "$s" != "" ] 
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

ensure_gui_up
if [ $? = 0 ];then
	ssh Ting@9.125.92.33 "/cygdrive/c/guibvt/start_guibvt.bat"
	#ssh ilovepumpkin@9.123.239.145 ./start_guibvt.sh
	#ssh Administrator@9.123.199.28	"/cygdrive/c/guiauto/waterbear_svc_730/start_guibvt.bat"
else
	$work_dir/../emailsender.py "Failed to launch Storwize GUI BVT" "$cluster_url didn't show up within give time"  "shenrui@cn.ibm.com" ""	
fi
