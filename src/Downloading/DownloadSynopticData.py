"""This codes downloads synoptic data according to date list."""

import os
import cdsapi
import pandas as pd
import numpy as np


# First we need to define the date
DateList = np.load('../DateList_Synoptic_10042021.npy', allow_pickle=True)

# split the data with respect to year,month and day
years = [str(i)[:4] for i in DateList[0:,0]]
months = [str(i)[4:6] for i in DateList[0:,0]]
days = [str(i)[6:] for i in DateList[0:,0]]
dones = [i for i in DateList[0:,2]]

#pressure level
variables_pressure = ["geopotential", "temperature", " specific_humidity", 
                 "u_component_of_wind", "v_component_of_wind", "vertical_velocity",
                 "vorticity"]

pr_levels = ['850', '700', '500', '250']

#single level
variables_single = ["2m_temperature", "10m_u_component_of_wind", "10m_v_component_of_wind", 
             "2m_dewpoint_temperature", "mean_sea_level_pressure",
             "convective_available_potential_energy",]

hours = ["00:00", "02:00", "04:00", "06:00", "08:00", "10:00",
         "12:00", "14:00", "16:00", "18:00", "20:00", "22:00"]

# Define the path
#storm klasörüne geçiş yap
for count in range(len(years)):
    
    # If the date has already processed, than continue to next loop.
    if DateList[count, 2] == 1: continue
        
    # -------------------------------------DATA PATH-----------------------------------------------------
    pre_data_path = r'C:\Users\USER\JupyterLab\Climaturk_Site\Docs\STORM_DATA'
    os.chdir(pre_data_path)

    #storm için yeni data klasörü oluştur
    try:
        post_data_path = years[count] + months[count] + days[count]
        os.mkdir(post_data_path)
    except:
        print('Directory exists')

    full_path_pr = pre_data_path + '\\' + post_data_path + '\\' + 'pressure_data.nc'
    full_path_sn = pre_data_path + '\\' + post_data_path + '\\' + 'single_data.nc'
    
    # ---------------------------------------PRESSURE LEVEL DATA--------------------------------------------------- 
    #request for downloading pressure levels
    c = cdsapi.Client()
    c.retrieve("reanalysis-era5-pressure-levels",
    {
    "variable": variables_pressure,
    "pressure_level": pr_levels,
    "year": years[count],
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
    "year": years[count],
    "month": months[count],
    "day": days[count],
    "time": hours,
    "format": "netcdf"
    }, full_path_sn)
    
    # change 0 to 1 in corresponding date's [done] column (means the date is completed in downloading)
    DateList[count, 2] = 1
    np.save('../DateList_Synoptic_10042021', DateList)