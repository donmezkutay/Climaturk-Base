# -*- coding: utf-8 -*-
"""This codes downloads thermodynamic data according to date list."""

import os
import cdsapi
import pandas as pd
import numpy as np

# First we need to define the date
DateList = np.load(r'C:\Users\USER\JupyterLab\Climaturk_Site\GITHUB\version_17_05_2021\Climaturk-Base\src/DateList_Thermodynamic_10042021.npy', allow_pickle=True)

# dimensions: (dates, dates_s, synoptic_done, thermodynamic_done)
# split the data with respect to year,month and day
years = [str(i)[:4] for i in DateList[0:,0]]
months = [str(i)[4:6] for i in DateList[0:,0]]
days = [str(i)[6:] for i in DateList[0:,0]]
thermodynamic_dones = [i for i in DateList[0:,2]]

hours = ["00:00", "02:00", "04:00", "06:00", "08:00", "10:00",
         "12:00", "14:00", "16:00", "18:00", "20:00", "22:00"]

variables_pressure = ["geopotential", "temperature", "relative_humidity", 
                 "u_component_of_wind", "v_component_of_wind",]

levels = ['1',
 '2',
 '3',
 '5',
 '7',
 '10',
 '20',
 '30',
 '50',
 '70',
 '100',
 '125',
 '150',
 '175',
 '200',
 '225',
 '250',
 '300',
 '350',
 '400',
 '450',
 '500',
 '550',
 '600',
 '650',
 '700',
 '750',
 '775',
 '800',
 '825',
 '850',
 '875',
 '900',
 '925',
 '950',
 '975',
 '1000']

# Define the path
#storm klasörüne geçiş yap
for count in range(len(years)):
    
    print('THE DATES IS: ', str(DateList[count, 0]))
    # If the date has already processed, than continue to next loop.
    if DateList[count, 2] == 1: continue
        
    pre_data_path = r'D:\JupyterLab\Climaturk_Site\Docs\STORM_DATA'
    os.chdir(pre_data_path)

    #storm için yeni data klasörü oluştur
    try:
        post_data_path = years[count] + months[count] + days[count]
        os.mkdir(post_data_path)
    except:
        print('Directory exists')
        
    full_path = pre_data_path + '\\' + post_data_path + '\\' + 'thermodynamic_data.nc'
    
    c = cdsapi.Client()
    c.retrieve("reanalysis-era5-pressure-levels",
    {
    "variable": variables_pressure,
    "pressure_level": levels,
    "year": years[count],
    "month": months[count],
    "day": days[count],
    "product_type": "reanalysis",
    "area":'42.00/26.00/36.00/45.00', # NWSE    
    "time": hours,
    "format": "netcdf"
    }, full_path)
    
    # change 0 to 1 in corresponding date's [done] column (means the date is completed in downloading)
    DateList[count, 2] = 1
    np.save(r'C:\Users\USER\JupyterLab\Climaturk_Site\GITHUB\version_17_05_2021\Climaturk-Base\src/DateList_Thermodynamic_10042021', DateList)