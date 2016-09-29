#!/bin/sh

: ${SAHI_HOME:?"The environment variable SAHI_HOME is required."}

keyword=$1
work_dir=$(cd "$(dirname "$0")"; pwd)
current_dir=$PWD
sahi_found=false

browser="chrome"

# clean
songstxt_path=$current_dir/songs.txt
rm -rf $SAHI_HOME/userdata/logs/traffic/*
rm -rf $songstxt_path
rm -rf /tmp/googlemusic_keyword.txt

sahi_pid=`lsof -Pnl +M|grep 9999|awk '{print $2}'`
if [ -n "$sahi_pid" ] 
then
    echo "Found a sahi server [$sahi_pid] is running, kill it!"
    kill -9 $sahi_pid
fi

cd $SAHI_HOME/userdata/bin
./start_sahi.sh &
sleep 5
sahi_pid=`lsof -Pnl +M|grep 9999|awk '{print $2}'`
echo "sahi server pid = $sahi_pid"

cd $SAHI_HOME/userdata/bin
echo $keyword>/tmp/googlemusic_keyword.txt
./testrunner.sh googlemusic/googlemusic.sah http://www.google.cn/music/player $browser

echo "killing started sahi server [$sahi_pid]"
kill -9 $sahi_pid

grep songstreaming $SAHI_HOME/userdata/logs/traffic/*/*_songstreaming/request.header_unmodified.txt|awk '{print $2}'>$songstxt_path

cd $current_dir
$work_dir/download.sh $songstxt_path "$keyword"
