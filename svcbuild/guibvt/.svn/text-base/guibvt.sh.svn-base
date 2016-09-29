#!/bin/sh

work_dir=$(cd "$(dirname "$0")"; pwd)
. $work_dir/config.sh

if [ $bvtenabled = 0 ];then
	#$work_dir/down_bvt_build.sh && $work_dir/install_bvt_build.sh && $work_dir/run_guibvt.sh
	$work_dir/install_bvt_build.sh && $work_dir/run_guibvt.sh
else
	echo "[Info] BVT is not enabled."
fi
