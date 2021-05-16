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

def hodograph(df, coordinate_pairs, cmap, dates,):
    os.chdir(r'C:\Users\USER\JupyterLab\Climaturk_Site\Codes\SkewT_Pictures')
    for sehir_id in coordinate_pairs.keys():
        pressure = df['level'].values * units.hectopascal
        t_tempor = df['t'].sel(latitude = coordinate_pairs[sehir_id][0], longitude = coordinate_pairs[sehir_id][1], method='nearest')
        temperature = t_tempor.fillna(np.mean(t_tempor)).values * units.celsius

        df['t']
        d_tempor = df['d'].sel(latitude = coordinate_pairs[sehir_id][0], longitude = coordinate_pairs[sehir_id][1], method='nearest')
        dew_point = d_tempor.fillna(np.mean(d_tempor)).values * units.celsius

        u_wind = df['u'].sel(latitude = coordinate_pairs[sehir_id][0], longitude = coordinate_pairs[sehir_id][1], method='nearest').values * units.knot
        v_wind = df['v'].sel(latitude = coordinate_pairs[sehir_id][0], longitude = coordinate_pairs[sehir_id][1], method='nearest').values * units.knot
        heights = df['z'].sel(latitude = coordinate_pairs[sehir_id][0], longitude = coordinate_pairs[sehir_id][1], method='nearest').values * units.meters

        interval = np.logspace(2. , 3.041392685158225) * units.hectopascal
        idx = mpcalc.resample_nn_1d(pressure , interval)

        fig, axs = plot.subplots(ncols=2, nrows=3, share=0)

        #format the plot
        axs.format(
            )
        for utc in range(0,6):
            h = Hodograph(axs[utc], component_range=60.)
            h.add_grid(increment=20)

            # rüzgar gücü intervalı ayarla
            mini = np.hypot(u_wind[::2][utc], v_wind[::2][utc]).min()
            maxi = np.hypot(u_wind[::2][utc], v_wind[::2][utc]).max()

            # 16: 250mb ve aşağısı anlamına geliyor
            l = h.plot_colormapped(u_wind[::2][utc][16:], v_wind[::2][utc][16:],  pressure[16:], 
                               linewidth = 2, cmap = cmap, path_effects=[pe.Stroke(linewidth=4, foreground='k'), pe.Normal()],)

            h.ax.set_title('{}UTC   |{}|  {} | 1000-250mb [kt]'.format(str(df['time'][::2].values[utc])[11:13], dates, sehir_id), 
                              fontdict = {'fontsize':8})

        os.chdir('{}'.format(dates))
        try:
            os.mkdir(r'{}'.format('hodograph'))
        except:  
            print('directory exists')

        plt.savefig('hodograph\{}.png'.format(sehir_id), bbox_inches='tight', dpi = 150)
        plt.close()
        
        os.chdir(r'C:\Users\USER\JupyterLab\Climaturk_Site\Codes\SkewT_Pictures')