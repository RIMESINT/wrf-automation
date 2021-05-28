#!/usr/bin/env bash
#: wrf model automation script
#: written by Quamrul Hasan, Meteorologis, BMD
#: modified by Nazmul Ahasan, CIL, RIMES

export WRF_EM_CORE=1
export WRF_NMM_CORE=0
export WRFIO_NCD_LARGE_FILE_SUPPORT=1
ulimit -s unlimited

# script source directory
BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# var definations
INIT_DATE=`date +%Y%m%d`                       # init date
INIT_TIME='12'                                 # init time
NCORE=90                                       # number of cores to be used for simulation
GFS_DIR=/disk1/quamrul/GFS_Data                # gfs data directory
WRF_DIR=/disk1/quamrul/WRF413/WRF/run          # wrf run directory
ARWPOST_DIR=/disk1/quamrul/WRF413/ARWpost      # arwpost directory
WPS_DIR=/disk1/quamrul/WRF413/WPS              # wps directory
LOG_DIR=/disk1/quamrul/logs                    # log output directory
DEBUG_LOG=$LOG_DIR/debug_12.log                # debug log location
PERF_LOG=$LOG_DIR/perf_12.log                  # perf log location
DOWN_LOG=$LOG_DIR/gfs_down_12.log              # gfs data download log

# download-gfs-data

cd $GFS_DIR

echo "::started gfs download @ `date`" >> $DEBUG_LOG

# donwload on this server
# recursively download gfs data 
#./download_gfs_recursive_failsafe.py `date +%Y%m%d`


# download gfs files in another server then copy to this server
REMOTE_SCRIPT_LOC=/home/rimes/scripts_cron/gfs_12_utc/download_gfs_wrap_v2.sh
REMOTE_FILE_DIR=/home/rimes/gfs_data/${INIT_DATE}${INIT_TIME}

ssh rimes@srv02.rimes.bmd $REMOTE_SCRIPT_LOC > $DOWN_LOG
scp -r rimes@srv02.rimes.bmd:$REMOTE_FILE_DIR ./
echo "::end gfs download     @ `date`" >> $DEBUG_LOG

# change configuration files [always for 10 day]
python3 $BASE_DIR/namelist_editor.py $INIT_DATE $INIT_TIME


# execute wps.exe
cd $WPS_DIR
rm GRIBFILE*
rm met_em.d01*
rm GFS*

# link gfs grib files
./link_grib.csh ${GFS_DIR}/${INIT_DATE}${INIT_TIME}/gfs* ./

# execute geogrid+ungrib_metgrid
./geogrid.exe
./ungrib.exe
./metgrid.exe


cd $WRF_DIR


rm ./met_em_d01*
ln -sf $WPS_DIR/met_em.d01* ./
./real.exe

# drop caches before running wrf
sudo $BASE_DIR/drop_memcache.sh > $PERF_LOG

# disable ASLR and NUMA Balancing
sudo $BASE_DIR/disable_aslr_numabal.sh >> $PERF_LOG

# configure cpu idle state & frequency govornor
sudo cpupower idle-set -d 2 >> $PERF_LOG
sudo cpupower frequency-set -g performance >> $PERF_LOG

# run wrf.exe
echo "::started wrf.exe @ `date` - ${NCORE} core" >> $DEBUG_LOG

mpirun.mpich -np $NCORE ./wrf.exe

echo "::end wrf.exe     @ `date`" >> $DEBUG_LOG


# revert to initial cpu state
sudo cpupower idle-set -e 2 >> $PERF_LOG
sudo cpupower frequency-set -g ondemand >> $PERF_LOG

# wrf data postprocessing
cd $ARWPOST_DIR
./ARWpost.exe

# >> do data processing here <<


# again drop cache to clean the system at the end of run
sudo $BASE_DIR/drop_memcache.sh >> $PERF_LOG


# file checking and cleanup
