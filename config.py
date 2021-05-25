
import os


base_dir = os.path.dirname(os.path.realpath(__file__))

num_day  = 10   # number of days to simulate
physics  = 3    # not using right now

# template location
template_root_dir  = os.path.join(base_dir,'templates')

# namelist template files
namelist_arwpost_t = os.path.join(template_root_dir, 'namelist.ARWpost.T')
namelist_wps_t     = os.path.join(template_root_dir, 'namelist.wps.T')
namelist_input_t   = os.path.join(template_root_dir, 'namelist.input.T')

# output location
namelist_arwpost_o = './test/namelist.ARWpost'
namelist_wps_o     = './test/namelist.wps'
namelist_input_o   = './test/namelist.input'


# arwpost output location wrfout_d01_2021-05-25_12:00:00


wrf_file_dir         = './test/WRF/run/'  # where the wrf output file is located
arwpost_output_dir   = './test/ARWpost'   # where the output files will be
arwpost_date_sep_dir = True               # wheather to create directory with date

# date formats [leave it if needed otherwise]
full_date_fmt    = lambda sim_utc: f'%Y-%m-%d_{sim_utc:02d}:00:00'
wrf_file_fmt     = lambda sim_utc: f'wrfout_d01_{full_date_fmt(sim_utc)}'
arwpost_file_fmt = lambda sim_utc: f'%Y%m%d{sim_utc:02d}'


