"""By Kutay/Berkay DÖNMEZ"""

#should get bs4, html5lib, lxml packages first
import scipy.constants as sc
import xarray as xr
import numpy as np
from datetime import datetime, timedelta
from dask.distributed import Client
import matplotlib.pyplot as plt
from metpy.plots import  SkewT
from metpy.units import units
from scipy.ndimage import gaussian_filter
import cartopy
import metpy.calc as mpcalc
from scipy.ndimage.filters import minimum_filter, maximum_filter
import numpy as np
import matplotlib.colors as colors
from datetime import datetime
import matplotlib.patheffects as PathEffects
import cdsapi
import proplot as plot
import os
import cartopy.crs as ccrs
import Compact_Maps

DateList = np.load('../DateList_Synoptic_10042021.npy', allow_pickle=True)

# Define the path
#storm klasörüne geçiş yap
for count in range(len(DateList)):
    
    print('THE DATES IS: ', str(DateList[count, 0]))
    # If the date has already processed, than continue to next loop. first cond
    # If the plot already done continue to next loop. second cond
    if DateList[count, 2] == 0 or DateList[count, 3] == 1: continue

    dates = str(DateList[count, 0])
    #dates_s =  str(DateList[count, 1])

    pre_data_path = r'C:\Users\USER\JupyterLab\Climaturk_Site\Docs\STORM_DATA'
    full_path_pr = pre_data_path + '\\' + dates + '\\' + 'pressure_data.nc'
    full_path_sn = pre_data_path + '\\' + dates + '\\' + 'single_data.nc'
    
    #storm için yeni data klasörü oluştur
    os.chdir(r'C:\Users\USER\JupyterLab\Climaturk_Site\Docs\STORMS')
    try:
        os.mkdir('{}'.format(str(DateList[count, 0])))
    except:
        print('Directory exists')

    pressure_data = xr.open_dataset(full_path_pr).sel(latitude = slice(44,35), longitude = slice(25,46))
    single_data = xr.open_dataset(full_path_sn).sel(latitude = slice(44,35), longitude = slice(25,46))

    plotting = Compact_Maps.Compact_plot(pressure_data, single_data, dates)

    plotting.Compact_250mb_wind_streamlines()
    plotting.Compact_2m_dew_mslp()
    plotting.Compact_2m_temp_mslp()
    plotting.Compact_500mb_vort_height()
    plotting.Compact_700mb_temp_height_spehum()
    plotting.Compact_700mb_vvel_streamlines()
    plotting.Compact_850mb_temp_height()
    plotting.Compact_cape_mslp_10mstreamlines()
    
    # change 0 to 1 in corresponding plot's [done] column (means the plot is completed in plotting)
    DateList[count, 3] = 1
    np.save('../DateList_Synoptic_10042021', DateList)
    print('Plot Done: ', str(DateList[count, 0]))