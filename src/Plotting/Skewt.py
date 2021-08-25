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

def skewt(df, coordinate_pairs, cmap, dates,):
    os.chdir(r'D:\JupyterLab\Climaturk_Site\Codes\SkewT_Pictures')
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

        fig = plt.figure(figsize=(15,15))

        for utc in range(0,6):

            right = 0.3
            up = 0.8
            up_diff = 0.15

            # 00 utc - 0
            if utc == 0:
                skew = SkewT(fig=fig,rect=(right-(0.15*1), up, .15, .1))

            #04 utc - 1
            if utc == 1:
                skew = SkewT(fig=fig,rect=(right-(0.15*0), up, .15, .1))

            # 08 utc - 2
            if utc == 2:
                skew = SkewT(fig=fig,rect=(right-(0.15*1), up-up_diff, .15, .1))

            #12 utc - 3
            if utc == 3:
                skew = SkewT(fig=fig,rect=(right-(0.15*0), up-(up_diff), .15, .1))

            # 16 utc - 4
            if utc == 4:
                skew = SkewT(fig=fig,rect=(right-(0.15*1), up-(2*up_diff), .15, .1))

            #20 utc - 5
            if utc == 5:
                skew = SkewT(fig=fig,rect=(right-(0.15*0), up-(2*up_diff), .15, .1))



            skew.plot(pressure , temperature[::2][utc] , color='red')
            skew.plot(pressure , dew_point[::2][utc] , color='green')

            #skew.plot_barbs(pressure[idx] , u_wind[::2][utc][idx] , v_wind[::2][utc][idx],
            #                xloc = 1, length=4, linewidth = 0.3)

            skew.ax.axvline(0, color='purple', linestyle='--',)

            skew.plot_dry_adiabats(linewidths=0.3)
            skew.plot_moist_adiabats(linewidths=0.3)
            skew.plot_mixing_lines(linewidths=0.3)

            skew.ax.set_xlim(-50 , 40)
            skew.ax.set_title('{}UTC   |{}|  {}'.format(str(df['time'][::2].values[utc])[11:13], dates, sehir_id), 
                              fontdict = {'fontsize':8})

        os.chdir('{}'.format(dates))
        try:
            os.mkdir(r'{}'.format('skewt'))
        except:  
            print('directory exists')

        plt.savefig('skewt\{}.jpeg'.format(sehir_id), bbox_inches='tight', dpi = 150, optimize=True, progressive=True,)
        plt.close()

        os.chdir(r'D:\JupyterLab\Climaturk_Site\Codes\SkewT_Pictures')