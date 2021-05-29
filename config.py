import os


base_dir = os.path.dirname(os.path.realpath(__file__))

num_day  = 10   # number of days to simulate
physics  = 3    # not using right now

# [modify these dirs]
arwpost_dir = './test/'
wps_dir     = './test/'
wrf_dir     = './test/'                   # namelist.input & output file location
geog_data   = '/disk1/quamrul/WPS_GEOG/'  # path where geog data is located
arwpost_output_dir   = './test/ARWpost'   # where the output files will be
arwpost_date_sep_dir = True               # wheather to create directory with date

gfs_down_dir         = './test/gfs_data/' # gfs data download location
gfs_res              = '0p25'
gfs_crop_region      = {
                        'llon' : 30,
                        'rlon' : 130,
                        'tlat' : 50,
                        'blat' : -10
                    }

# template location
template_root_dir  = os.path.join(base_dir,'templates')

# namelist template files
namelist_arwpost_t = os.path.join(template_root_dir, 'namelist.ARWpost.T')
namelist_wps_t     = os.path.join(template_root_dir, 'namelist.wps.T')
namelist_input_t   = os.path.join(template_root_dir, 'namelist.input.T')


# final name list locations
namelist_arwpost_o = os.path.join(arwpost_dir, 'namelist.ARWpost')
namelist_wps_o     = os.path.join(wps_dir, 'namelist.wps')
namelist_input_o   = os.path.join(wrf_dir, 'namelist.input')



# date formats [leave it unedited if needed otherwise]
full_date_fmt    = lambda sim_utc: f'%Y-%m-%d_{sim_utc:02d}:00:00'
wrf_file_fmt     = lambda sim_utc: f'wrfout_d01_{full_date_fmt(sim_utc)}'
arwpost_file_fmt = lambda sim_utc: f'%Y%m%d{sim_utc:02d}'


