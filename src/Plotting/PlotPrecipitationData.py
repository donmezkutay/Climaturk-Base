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
import asyncio
from dask.distributed import Client, LocalCluster, fire_and_forget
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER , LATITUDE_FORMATTER
from mpl_toolkits.axes_grid1 import make_axes_locatable

import sys
# import own packages
sys.path.append(r'..\src')
import Compact_Maps
from OpenThermodynamicData import opendownloadeddata
from Hodograph import hodograph
from Skewt import skewt
from Precipitation_Compact_Maps import Compact_precipitation

DateList = np.load('../DateList_Precipitation_10042021.npy', allow_pickle=True)

# Define the path
#storm klasörüne geçiş yap
for count in range(len(DateList)):
    
    print('THE DATES IS: ', str(DateList[count, 0]))
    # If the date has already processed, than continue to next loop. first cond
    # If the plot already done continue to next loop. second cond
    if DateList[count, 2] == 1: continue
        
    # define dates
    dates = str(DateList[count, 0])
    year = int(dates[:4])
    month = int(dates[4:6])
    day = int(dates[6:])

    datetime_object = datetime(year, month, day)
    
    # data paths
    pre_data_path = r'C:\Users\USER\JupyterLab\Climaturk_Site\Docs\STORM_DATA\precipitation'
    full_path_era5 = pre_data_path + '\\' + 'DAILY_ERA5' + '\\' + 'DAILY_ERA5.nc'
    full_path_merra2 = pre_data_path + '\\' + 'DAILY_MERRA2' + '\\' + 'DAILY_MERRA2.nc'
    full_path_jra55 = pre_data_path + '\\' + 'DAILY_JRA55' + '\\' + 'DAILY_JRA55.nc'
    full_path_cfsr_cfsv2 = pre_data_path + '\\' + 'DAILY_CFSR_CFSV2' + '\\' + 'DAILY_CFSR_CFSV2.nc'
    
    #storm için yeni data klasörü oluştur
    os.chdir(r'C:\Users\USER\JupyterLab\Climaturk_Site\Docs\STORMS\precipitation')
    try:
        os.mkdir('{}'.format(str(DateList[count, 0])))
    except:
        print('Directory exists')
    
    # clip datasets into datelist
    dt_era5 = xr.open_dataset(full_path_era5).sel(time = datetime_object)['tp'] * 1000 #m - saatlik = 1000 ile çarp
    dt_merra2 = xr.open_dataset(full_path_merra2).sel(time = datetime_object)['PRECTOTCORR'] * 3600 # kg/m2s-1 - saatlik = 3600 ile çarp günlük toplamı
    dt_jra55 = xr.open_dataset(full_path_jra55).sel(initial_time0_hours = datetime_object)['TPRAT_GDS4_SFC_ave3h'] * 2 / 4 # mm/day - 6 hourly - 3hour forecast = 2 ile çarp (kalan 12 saat) ve 4 'e böl(mm/dayden mm/6hour'a)
    dt_cfsr_cfsv2 = xr.open_dataset(full_path_cfsr_cfsv2).sel(time = datetime_object)['A_PCP_L1_Accum_1'] * 6 # kg/m2 - 6hourly - 1 hour accumulation = 6 ile çarp
    
    # rename dimensions
    dt_merra2 = dt_merra2.rename({'lat':'latitude', 'lon':'longitude'})
    dt_jra55 = dt_jra55.rename({'g4_lat_1':'latitude', 'g4_lon_2':'longitude', 'initial_time0_hours':'time'})
    dt_cfsr_cfsv2 = dt_cfsr_cfsv2.rename({'lat':'latitude', 'lon':'longitude'})
    
    
    # visualize and save
    Compact_precipitation(dt_era5, 'era5', str(DateList[count, 0]))
    Compact_precipitation(dt_merra2, 'merra2', str(DateList[count, 0]))
    Compact_precipitation(dt_jra55, 'jra55', str(DateList[count, 0]))
    Compact_precipitation(dt_cfsr_cfsv2, 'cfsr_cfsv2', str(DateList[count, 0]))
    
    # ...
    
    # change 0 to 1 in corresponding plot's [done] column (means the plot is completed in plotting)
    DateList[count, 2] = 1
    os.chdir(r'C:\Users\USER\JupyterLab\Climaturk_Site\GITHUB\version_17_05_2021\Climaturk-Base\development')
    np.save('../DateList_Precipitation_10042021', DateList)
    print('Plot Done: \n\n', str(DateList[count, 0]))
    
    