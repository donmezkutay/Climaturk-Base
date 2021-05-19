"""By Kutay/Berkay DÖNMEZ"""

#should get bs4, html5lib, lxml packages first
import scipy.constants as sc
import xarray as xr
import numpy as np
from datetime import datetime, timedelta
from dask.distributed import Client
import os
import matplotlib.pyplot as plt
from metpy.plots import  SkewT
from metpy.units import units
import metpy.calc as mpcalc
import numpy as np
import matplotlib.colors as colors
from datetime import datetime
import cdsapi
import proplot as plot
from metpy.plots import Hodograph
import matplotlib.patheffects as pe

def opendownloadeddata(dates, ):
    df = xr.open_dataset(r'C:\Users\USER\JupyterLab\Climaturk_Site\Docs\STORM_DATA\{}\thermodynamic_data.nc'.format(dates))

    # veri çevir
    #Proper Units for pressure level data
    start_compute = datetime.now()
    df['u'] = np.multiply(df['u'], 1.94384449) # knot
    df['v']  = np.multiply(df['v'], 1.94384449) # knot
    df['z']  = np.divide(df['z'], sc.g) # metres
    df['t']  = np.subtract(df['t'], 273.15) # Celsius
    df['r'] = xr.where(df['r'] > 100, 100, df['r']) / 100
    dew = np.array(mpcalc.dewpoint_from_relative_humidity(df['t'].values * units.celsius, df['r'] ))
    df = df.assign({'d':( 
                            ('time', 'level', 'latitude', 'longitude'), dew)})

    coordinate_pairs = {'istanbul':[41.015652, 28.924274],
                        'ankara'  :[39.929645, 32.832453],
                        'izmir'   :[38.436153, 27.149811],
                        'adana'   :[36.977732, 35.326788],
                        'samsun'  :[41.284951, 36.340072],
                        'rize'    :[41.024368, 40.521516],
                        'erzurum' :[39.902315, 41.266793],
                        'mardin'  :[37.316895, 40.729067]} # lon lat
    
    return df, coordinate_pairs