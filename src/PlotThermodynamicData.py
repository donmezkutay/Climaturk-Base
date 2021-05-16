"""By Kutay/Berkay DÖNMEZ"""

#should get bs4, html5lib, lxml packages first
import scipy.constants as sc
import xarray as xr
import numpy as np
from pydap.client import open_url
from pydap.cas.urs import setup_session
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
from OpenThermodynamicData import opendownloadeddata
from Hodograph import hodograph
from Skewt import skewt

DateList = np.load('DateList_Thermodynamic_10042021.npy', allow_pickle=True)

# Define the path
#storm klasörüne geçiş yap
for count in range(len(DateList)):
    
    print('THE DATES IS: ', str(DateList[count, 0]))
    # If the date has already processed, than continue to next loop. first cond
    # If the plot already done continue to next loop. second cond
    if DateList[count, 2] == 0 or DateList[count, 3] == 1: continue

    dates = str(DateList[count, 0])
    #dates_s =  str(DateList[count, 1])
    
    #storm için yeni data klasörü oluştur
    os.chdir(r'C:\Users\USER\JupyterLab\Climaturk_Site\Codes\SkewT_Pictures')
    try:
        os.mkdir('{}'.format(str(DateList[count, 0])))
    except:
        print('Directory exists')
    
    # open data
    df, coordinate_pairs = opendownloadeddata(dates)
    
    #plot
    cmap = plot.Colormap(
    'mono_r', name='SciVisColor', )

    hodograph(df, coordinate_pairs, cmap, dates,)
    skewt(df, coordinate_pairs, cmap, dates,)
    
    # change 0 to 1 in corresponding plot's [done] column (means the plot is completed in plotting)
    DateList[count, 3] = 1
    np.save('DateList_Thermodynamic_10042021', DateList)
    print('Plot Done: ', str(DateList[count, 0]))
    