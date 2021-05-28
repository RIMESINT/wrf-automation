&share
 wrf_core = 'ARW',
 max_dom = 1,
 start_date = '{{start_date}}','2006-08-16_12:00:00',
 end_date   = '{{end_date}}','2006-08-16_12:00:00',
 interval_seconds = 21600
 io_form_geogrid = 2,
/

&geogrid
 parent_id         =   1,   1,
 parent_grid_ratio =   1,   3,
 i_parent_start    =   1,  31,
 j_parent_start    =   1,  17,
 e_we              = 215, 112,
 e_sn              = 215,  97,
 !
 !!!!!!!!!!!!!!!!!!!!!!!!!!!! IMPORTANT NOTE !!!!!!!!!!!!!!!!!!!!!!!!!!!!
 ! The default datasets used to produce the HGT_M, GREENFRAC, 
 ! and LU_INDEX/LANDUSEF fields have changed in WPS v3.8. The HGT_M field
 ! is now interpolated from 30-arc-second USGS GMTED2010, the GREENFRAC 
 ! field is interpolated from MODIS FPAR, and the LU_INDEX/LANDUSEF fields 
 ! are interpolated from 21-class MODIS.
 !
 ! To match the output given by the default namelist.wps in WPS v3.7.1, 
 ! the following setting for geog_data_res may be used:
 !
 ! geog_data_res = 'gtopo_10m+usgs_10m+nesdis_greenfrac+10m','gtopo_2m+usgs_2m+nesdis_greenfrac+2m',
 !
 !!!!!!!!!!!!!!!!!!!!!!!!!!!! IMPORTANT NOTE !!!!!!!!!!!!!!!!!!!!!!!!!!!!
 !
 geog_data_res = 'default','default',
 dx = 0.080951647,
 dy = 0.080951647,
 map_proj = 'lat-lon',
 ref_lat   =  22.0,
 ref_lon   =  90.0,
 truelat1  =  22.0,
 truelat2  =  22.0,
 stand_lon =  90.0,
 geog_data_path = '{{geog_data}}'
/

&ungrib
 out_format = 'WPS',
 prefix = 'GFS',
/

&metgrid
 fg_name = 'GFS'
 io_form_metgrid = 2, 
/

