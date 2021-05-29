#!/usr/bin/env bash

BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

GFS_DIR='./test/gfs_data'
DATE=`date +'%Y%m%d'`
SIM_UTC='12'

# chec if the directory exists

if [ -f $GFS_DIR ]; then 

	# remove previous data
	dir_count=`ls $GFS_DIR | wc -l`

	if [ $dir_count -ge 1 ]; then
		rm -r $GFS_DIR/*
	fi

else
	mkdir -p $GFS_DIR
fi

python3 $BASE_DIR/download_gfs_recursive.py $GFS_DIR $DATE $SIM_UTC

echo 'downlod done initiate copy'
