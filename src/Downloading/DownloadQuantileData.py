"""This codes downloads quantile data according to date list."""

import os
import cdsapi
import matplotlib.pyplot as plt
import xarray as xr
import numpy as np

# First we need to define the date
DateList = np.load(r'C:\Users\USER\JupyterLab\Climaturk_Site\GITHUB\version_17_05_2021\Climaturk-Base\src/DateList_Quantile_10042021.npy', allow_pickle=True)

# split the data with respect to year,month and day
years = [str(i)[:4] for i in DateList[0:,0]]
months = [str(i)[4:6] for i in DateList[0:,0]]
days = [str(i)[6:] for i in DateList[0:,0]]
dones = [i for i in DateList[0:,2]]

#pressure level
variables_pressure = ["geopotential",]

pr_levels = ['500']

#single level
variables_single = ["2m_temperature", "2m_dewpoint_temperature",
                    "mean_sea_level_pressure",]

hours = ["00:00", "02:00", "04:00", "06:00", "08:00", "10:00",
         "12:00", "14:00", "16:00", "18:00", "20:00", "22:00"]
year_list = [str(i) for i in np.arange(1991, 2021, 1, dtype = int)]

# Define the path
#storm klasörüne geçiş yap
for count in range(len(years)):

    # If the date has already processed, than continue to next loop.
    if DateList[count, 2] == 1: continue
        
    # -------------------------------------DATA PATH-----------------------------------------------------
    pre_data_path = r'D:\JupyterLab\Climaturk_Site\Docs\STORM_DATA'
    os.chdir(pre_data_path)

    #storm için yeni data klasörü oluştur
    try:
        post_data_path = years[count] + months[count] + days[count]
        os.mkdir(post_data_path)
    except:
        print('Directory exists')

    full_path_pr = pre_data_path + '\\' + post_data_path + '\\' + 'quantile_pressure_data.nc'
    full_path_sn = pre_data_path + '\\' + post_data_path + '\\' + 'quantile_single_data.nc'

    # ---------------------------------------PRESSURE LEVEL DATA--------------------------------------------------- 
    #request for downloading pressure levels
    c = cdsapi.Client()
    c.retrieve("reanalysis-era5-pressure-levels",
        {
        "variable": variables_pressure,
        "pressure_level": pr_levels,
        "year": year_list,
        "month": months[count],
        "day": days[count],
        "product_type": "reanalysis",
        "area":'50.00/20.00/30.00/47.00', # NWSE    
        "time": hours,
        "format": "netcdf"
        }, full_path_pr)

    # ----------------------------------------SINGLE LEVEL DATA--------------------------------------------------
    #request for downloading single levels
    c = cdsapi.Client()
    c.retrieve("reanalysis-era5-single-levels",
        {
        "variable": variables_single,
        "product_type": "reanalysis",
        "area":'50.00/20.00/30.00/47.00', # NWSE    
        "year": year_list,
        "month": months[count],
        "day": days[count],
        "time": hours,
        "format": "netcdf"
        }, full_path_sn)
    
    # change 0 to 1 in corresponding date's [done] column (means the date is completed in downloading)
    DateList[count, 2] = 1
    np.save(r'C:\Users\USER\JupyterLab\Climaturk_Site\GITHUB\version_17_05_2021\Climaturk-Base\src/DateList_Quantile_10042021', DateList)
    
    