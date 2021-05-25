#!/usr/bin/env bash

GFS_DIR='./gfs_data'
SIM_UTC='12'

cd $GFS_DIR 

# remove previous data
dir_count=`ls|wc -l`

if [ $dir_count -ge 1 ]; then
	rm -r ./*
fi

python3 /home/rimes/scripts_cron/download_gfs_recursive.py `date +'%Y%m%d'`

echo 'downlod done initiate copy'
