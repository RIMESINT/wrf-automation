#!/usr/bin/env python3
'''
	namelist file generation for wps wrf and arwpost
	nazmul@rimes.int
'''

import sys, os 
import config as conf
from jinja2 import Template
from datetime import datetime as dt, timedelta as delt

print(conf.base_dir)

def render_template(template_file:str,data:dict)->str:
	print('rendering template ',template_file)

	with open(template_file,'r') as tf:
	
		template = Template(tf.read())
		return template.render(data)


def save_namelist_wps(data:dict)->int:

	with open(conf.namelist_wps_o,'w') as wf:
		out_data  = render_template(conf.namelist_wps_t, data)
		wf.write(out_data)
		return 0

def save_namelist_input(data:dict)->int:

	with open(conf.namelist_input_o,'w') as wf:
		out_data  = render_template(conf.namelist_input_t, data)
		wf.write(out_data)
		return 0

def save_namelist_arwpost(data:dict)->int:

	with open(conf.namelist_arwpost_o,'w') as wf:
		out_data  = render_template(conf.namelist_arwpost_t, data)
		wf.write(out_data)
		return 0


def main(start_date:str, sim_utc:str):

	start_date = dt.strptime(start_date, '%Y%m%d')
	end_date = start_date+delt(days=conf.num_day)

	full_start_date = start_date.strftime(conf.full_date_fmt(sim_utc))
	full_end_date = end_date.strftime(conf.full_date_fmt(sim_utc))

	# namelist.wps file generation 2006-08-16_12:00:00
	data_nw = {
		'start_date': full_start_date,
		'end_date'  : full_end_date,
		'geog_data' : conf.geog_data,
	}

	save_namelist_wps(data_nw)

	# namelist.input file generation 
	data_ni = {
		'start_year' : start_date.year,
		'start_month': start_date.month,
		'start_day'  : start_date.day,
		'start_hour' : sim_utc,

		'end_year' : end_date.year,
		'end_month': end_date.month,
		'end_day'  : end_date.day,
		'end_hour' : sim_utc,
	}

	save_namelist_input(data_ni)

	# namelist.ARWpost generation
	
	arwpost_out_dir = os.path.join(
						conf.arwpost_output_dir,
						start_date.strftime( conf.arwpost_file_fmt(sim_utc) )
					) \
					if conf.arwpost_date_sep_dir \
					else os.path.join(conf.arwpost_output_dir)
	
	# create directory
	if not os.path.exists(arwpost_out_dir) and conf.arwpost_date_sep_dir:
		os.makedirs(arwpost_out_dir)

	data_na = {
		'start_date' : full_start_date,
		'end_date'   : full_end_date,
		'input_root' : os.path.join(conf.wrf_dir, start_date.strftime(conf.wrf_file_fmt(sim_utc))),
		'output_root': os.path.join(arwpost_out_dir,start_date.strftime(conf.arwpost_file_fmt(sim_utc)))
	}


	save_namelist_arwpost(data_na)

	


if __name__=='__main__':
	
	if len(sys.argv) == 3:
		_, start_date, sim_utc = sys.argv
		main(start_date,int(sim_utc))
	else:
		print('insuffient argument; provide sim start date (yyyymmdd) and sim utc (00/12)')


