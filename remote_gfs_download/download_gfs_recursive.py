#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
This scripts keeps looking for file if not available
waits 1 minute and runs again

Pain Point:
	Config file is not used as this essentially runs on another server

Note: 
	- nomads servers allow only 120 requests per minute
	- spawning 5 threads with 1 minute sleep so max possible request
		within a minute is 5
'''

import sys,os,time
import logging
from tqdm import tqdm
import requests as req
from multiprocessing.pool import ThreadPool
from datetime import datetime as dt,timedelta as dtlt 


logging.basicConfig(
	filename='gfs_download.log', 
	filemode='w', 
	level=logging.INFO,
	format= "%(asctime)s - %(levelname)s - %(message)s"
)


SLEEP_TIME = 1*60 # sec

headers = {
	'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0'
}

def down_from_url(args):

	url,gribfile,dist_dir = args

	try:
		req_dat = req.get(url,headers=headers)

		if req_dat.status_code==200:
			with open(os.path.join(dist_dir,gribfile),'wb') as gf:
				for chunk in req_dat.iter_content(chunk_size=4096):
					if chunk: gf.write(chunk)
		else:
			logging.info(f'{gribfile} status!=200, sleeping then Respawning')
			time.sleep(SLEEP_TIME)
			down_from_url(args)
	except:
		logging.info(f'{gribfile}: sleeping then Respawning')
		time.sleep(SLEEP_TIME)
		down_from_url(args)

	return 0



def build_url_list(out_dir, fdate, sim_utc, grid_res='0p25', lead_day=10):

	dst_dir = os.path.join(out_dir, f'{fdate}{sim_utc}')

	if not os.path.exists(dst_dir): os.makedirs(dst_dir)		

	
	subregion={
		'llon' : 30,
		'rlon' : 130,
		'tlat' : 50,
		'blat' : -10
	}

	URL_LIST=[]

	for FT in range(0,(lead_day*24)+6,6):
		
		gribfile = f'gfs.t{sim_utc}z.pgrb2.{grid_res}.f{FT:03d}'

		URL  = f'https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_{grid_res}.pl?'
		URL += f'file={gribfile}&'
		URL += f'all_lev=on&all_var=on&'
		URL += f'subregion=&leftlon={subregion["llon"]}&rightlon={subregion["rlon"]}&toplat={subregion["tlat"]}&bottomlat={subregion["blat"]}&'
		URL += f'dir=/gfs.{fdate}/{sim_utc}/atmos'

		URL_LIST.append((URL,gribfile,dst_dir))

	return URL_LIST



def main(out_dir, date, sim_utc):

	url_list = build_url_list(out_dir, date, sim_utc)
	total_calls = len(url_list)
	
	thread_pool = ThreadPool(5)
	
	for _ in tqdm (thread_pool.imap_unordered(down_from_url, url_list),total=total_calls): pass
	
	thread_pool.close()
	thread_pool.join()



if __name__ == '__main__':
	if len(sys.argv)==4:
		_, out_dir, date, sim_utc = sys.argv
		main(out_dir, date, int(sim_utc))
	else:
		print('Insufficient arguments. privide output_path, date(yyyymmdd) and sim_utc(00/12)')
