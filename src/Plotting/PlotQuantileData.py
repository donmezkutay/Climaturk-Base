import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cartopy
from visjobs.visualize import easy_plot
import matplotlib.patheffects as PathEffects
import os
import scipy.constants as sc
import salem
import proplot as plot

from pylab import rcParams
rcParams['figure.figsize'] = 21,24

def plot_quantile_map(ds, var, short_title_min, short_title_max, short_title_ave, ul_title):
    # görsel


    #draw map
    m = easy_plot.painter()

    for i in range(len(ds)):

        if i == 0:
            short_title = short_title_min
            saved_method = 'min'

        elif i == 1:
            short_title = short_title_max
            saved_method = 'max'

        elif i == 2:
            short_title = short_title_ave
            saved_method = 'ave'
        
        lon = ds[0]['longitude']
        lat = ds[0]['latitude']

        work_title = '{}'.format(dates,)

        #paint features
        ax = m.paint_ax(1,1,1, check_proj=True)

        #features
        ax.add_feature(cartopy.feature.LAND.with_scale('10m'),  zorder=1, linewidths=1.5, edgecolor='none', facecolor='white')
        m.paint_borders(ax=ax, res='10m', zorder=4, linewidths=1.5, edgecolor='red' )
        m.paint_lakes(ax=ax, res='10m', zorder=2, linewidths=1.5, edgecolor='red', facecolor='none' )
        m.paint_states(ax=ax, res='10m', zorder=4, linewidths=0.4, edgecolor='red',  )
        m.paint_coastline(ax=ax, res='10m', zorder=3, linewidths=1.8, edgecolor='red')

        ax.set_extent([25, 45, 33, 45])
        
        if var == 'z':
            interval = np.arange(np.min(ds[i]), np.max(ds[i]), 6)
            
        if var == 't':
            interval = np.arange(np.min(ds[i]), np.max(ds[i]), 2)
            
        if var == 'd':
            interval = np.arange(np.min(ds[i]), np.max(ds[i]), 2)
            
        if var == 'p':
            interval = np.arange(np.min(ds[i]), np.max(ds[i]), 1)
        
        #make the freezing rain reflectivities contourf
        mesh = ax.contour(lon, lat, ds[i], interval, transform=cartopy.crs.PlateCarree(), zorder=6, alpha=0.9,
                            colors='k' )
        m.plot_clabel(mesh, fontsize=25, inline=1, inline_spacing=7,fmt='%i', rightside_up=True, use_clabeltext=True , ax=ax, zorder=5)


        valid_era = m.set_title(title='ERA-5 Reanalysis', right = 0.850, up=0.010, ax=ax, fontsize=16,
                                     style='italic', color='black', zorder=20, transform=ax.transAxes, weight='bold'
                                     )

        valid_t = m.set_title(title='1991-2020 Baseline', right = 0.850, up=1.010, ax=ax, fontsize=16,
                                     style='italic', color='red', zorder=20, transform=ax.transAxes, weight='bold'
                                     )

        #titles
        title_short = m.set_title(title='{}'.format(short_title), ax=ax, fontsize=20, up=1.030, 
                                 weight='heavy',style='italic',transform=ax.transAxes)

        title1 = m.set_title(title='{}'.format(ul_title), ax=ax, fontsize=16, up=1.010, 
                                 weight='heavy',style='italic',transform=ax.transAxes)
        title2 = m.set_title(title='Climaturk.com', color='white', right=0.00730, up=0.9615000, ax=ax, size=25, 
                                     zorder=53,style='italic',transform=ax.transAxes, weight='bold',
                                        )
        title2.set_path_effects([PathEffects.withStroke(linewidth=6, foreground='k')])
        
        # savefig
        #storm için yeni data klasörü oluştur
        os.chdir(r'D:\JupyterLab\Climaturk_Site\Docs\STORMS\Quantiles')
        try:
            os.mkdir('{}'.format(str(DateList[count, 0])))
        except:
            print('Directory exists')
        
        #save figure
        plt.savefig(r'D:\JupyterLab\Climaturk_Site\Docs\STORMS\Quantiles\{}\{}_{}_{}.jpeg'.format(str(DateList[count, 0]),
                                                                                                        '2D',
                                                                                                          var,
                                                                                                          saved_method),
                        bbox_inches='tight', optimize=True, progressive=True, dpi=150,
                        )
        plt.close()
        
def plot_yearly_series(data, var, coordinate_pairs, short_title_min, short_title_max,
                       short_title_ave, ylabel, ultitle):

    urtitle = 'Climaturk.com'
    for i in range(3):

        if i == 0:
            short_title = short_title_min
            saved_method = 'min'

        elif i == 1:
            short_title = short_title_max
            saved_method = 'max'

        elif i == 2:
            short_title = short_title_ave
            saved_method = 'ave'
            
        fig_array = [[1,1]]
        fig, axs = plot.subplots(fig_array, 
                                 aspect=2, axwidth=5,
                                  hratios=(1), includepanels=True, share=0)
        
        # turn dataset into pandas for temporarily
        quick_pandas = {}

        for city in coordinate_pairs.keys():

            tmp_dt = data[city][var][i]
            quick_pandas[city] = tmp_dt.values

        quick_pandas_df = pd.DataFrame(quick_pandas)
        
        # -----------
        
        # Lineplot
        #cycle = plot.Cycle('dark green', space='hpl', N=len(coordinate_pairs))
        axs[0].plot(quick_pandas_df, cycle='Set2', lw=1, legend='ll')

        axs[0].format(ylabel=ylabel, xlabel='Years', 
                             xlocator=(range(0, 30, 1)), 
                             xformatter=[str(j) for j in np.arange(1991, 2021, dtype = int)],
                             axeslabelweight='bold', ticklabelweight='bold',
                             xrotation = 90)

        axs[0].format(title=short_title)
        axs[0].format(ultitle=ultitle)
        axs[0].format(urtitle=urtitle)
        

        # savefig
        #storm için yeni data klasörü oluştur
        os.chdir(r'D:\JupyterLab\Climaturk_Site\Docs\STORMS\Quantiles')
        try:
            os.mkdir('{}'.format(str(DateList[count, 0])))
        except:
            print('Directory exists')

        #save figure
        plt.savefig(r'D:\JupyterLab\Climaturk_Site\Docs\STORMS\Quantiles\{}\{}_{}_{}.jpeg'.format(str(DateList[count, 0]),
                                                                                                'timeseries',
                                                                                                var,
                                                                                                saved_method
                                                                                                 ),
                                                bbox_inches='tight',
                                                optimize=True,
                                                progressive=True,
                                                dpi=150,
                        )
        plt.close()
        
def adjust_data_units(pressure_data, single_data):
    
    pressure_data['z'] = np.divide(pressure_data['z'], sc.g) # geop. to height
    
    single_data['t2m'] = single_data['t2m'] - 273.15 # K to C
    single_data['d2m'] = single_data['d2m'] - 273.15 # K to C
    single_data['msl'] = single_data['msl'] / 100 # Pa to hPa
    
    return pressure_data, single_data

def find_min_max_ave(data, var):
    
    return data[var].min(dim='time'), \
           data[var].max(dim='time'), \
           data[var].mean(dim='time')

def groupby_yearly_min_max_ave(data, var):
    
    return (data[var].groupby('time.year').min(),
            data[var].groupby('time.year').max(),
            data[var].groupby('time.year').mean())


# aşağıdakini açarsın
DateList = np.load(r'C:\Users\USER\JupyterLab\Climaturk_Site\GITHUB\version_17_05_2021\Climaturk-Base\src/DateList_Quantile_10042021.npy', allow_pickle=True)

# Define the path
#storm klasörüne geçiş yap
for count in range(len(DateList)):
    
    print('THE DATES IS: ', str(DateList[count, 0]))
    
    # If the date has already processed, than continue to next loop. first cond
    # If the plot already done continue to next loop. second cond
    if DateList[count, 2] == 0 or DateList[count, 3] == 1: continue

    dates = str(DateList[count, 0])
    #dates_s =  str(DateList[count, 1])
    ul_title = 'M/D: ' + str(DateList[count, 0])[4:6] + '/' + str(DateList[count, 0])[6:]
    
    pre_data_path = r'D:\JupyterLab\Climaturk_Site\Docs\STORM_DATA'
    full_path_pr = pre_data_path + '\\' + dates + '\\' + 'quantile_pressure_data.nc'
    full_path_sn = pre_data_path + '\\' + dates + '\\' + 'quantile_single_data.nc'

    pressure_data = xr.open_dataset(full_path_pr)
    single_data = xr.open_dataset(full_path_sn)
    
    #adjust dataset units
    adjusted_pressure, adjusted_single = adjust_data_units(pressure_data, single_data)
    
    
    
    ## 2D MAPS PREPARATION **************************************
    # min - max - ave for z
    zmin_daily, zmax_daily, zave_daily = find_min_max_ave(adjusted_pressure, 'z')
    
    # min - max - ave for t
    tmin_daily, tmax_daily, tave_daily = find_min_max_ave(adjusted_single, 't2m')
    
    # min - max - ave for d
    dmin_daily, dmax_daily, dave_daily = find_min_max_ave(adjusted_single, 'd2m')
    
    # min - max - ave for p
    pmin_daily, pmax_daily, pave_daily = find_min_max_ave(adjusted_single, 'msl')

    ds_z = [zmin_daily, zmax_daily, zave_daily]
    ds_t = [tmin_daily, tmax_daily, tave_daily]    
    ds_d = [dmin_daily, dmax_daily, dave_daily]    
    ds_p = [pmin_daily, pmax_daily, pave_daily]
    
    ## END OF 2D MAPS PREPARATION **************************************
    
    
    ## TIME SERIES MAPS PREPARATION *********************************
    # Coordinates to be used
    coordinate_pairs = {'istanbul':[41.015652, 28.924274],
                            'ankara'  :[39.929645, 32.832453],
                            'izmir'   :[38.436153, 27.149811],
                            'adana'   :[36.977732, 35.326788],
                            'samsun'  :[41.284951, 36.340072],
                            'rize'    :[41.024368, 40.521516],
                            'erzurum' :[39.902315, 41.266793],
                            'mardin'  :[37.316895, 40.729067]} # lon lat
    
    
    city_pressure_data = {}
    city_single_data = {}

    for city in coordinate_pairs.keys():
        city_pressure_data[city] = adjusted_pressure.sel(latitude = coordinate_pairs[city][0], longitude = coordinate_pairs[city][1], method = 'nearest')
        city_single_data[city] = adjusted_single.sel(latitude = coordinate_pairs[city][0], longitude = coordinate_pairs[city][1], method = 'nearest')

    separate_city_data = {}

    for city in coordinate_pairs.keys():
        z_gr_min, z_gr_max, z_gr_ave = groupby_yearly_min_max_ave(city_pressure_data[city], 'z')
        t_gr_min, t_gr_max, t_gr_ave = groupby_yearly_min_max_ave(city_single_data[city], 't2m')
        d_gr_min, d_gr_max, d_gr_ave = groupby_yearly_min_max_ave(city_single_data[city], 'd2m')
        p_gr_min, p_gr_max, p_gr_ave = groupby_yearly_min_max_ave(city_single_data[city], 'msl')

        separate_city_data[city] = {}
        separate_city_data[city]['z'] = [z_gr_min, z_gr_max, z_gr_ave]
        separate_city_data[city]['t'] = [t_gr_min, t_gr_max, t_gr_ave]    
        separate_city_data[city]['d'] = [d_gr_min, d_gr_max, d_gr_ave]    
        separate_city_data[city]['p'] = [p_gr_min, p_gr_max, p_gr_ave]   
    
    ## END OF TIME SERIES MAPS PREPARATION *********************************
    

    # PLOTS
    
    # z
    var = 'z'
    short_title_max = '500 mb Maximum Geopotential Height (m)'
    short_title_min = '500 mb Minimum Geopotential Height (m)'
    short_title_ave = '500 mb Average Geopotential Height (m)'
    
    # 2D MAP PLOT
    plot_quantile_map(ds_z, var, short_title_min, short_title_max, short_title_ave, 
                     ul_title)
    
    # Time Series PLOT
    plot_yearly_series(separate_city_data, var = var, coordinate_pairs=coordinate_pairs,
                   short_title_min=short_title_min, short_title_max=short_title_max, short_title_ave=short_title_ave,
                   ylabel = 'Geopotential Height (m)',
                   ultitle = ul_title)
    
    print(f'exitted Plotting: {var}')
    
    # t
    var = 't'
    short_title_max = '2m  Maximum Temperature (degC)'
    short_title_min = '2m  Minimum Temperature (degC)'
    short_title_ave = '2m  Average Temperature (degC)'
    
    # 2D MAP PLOT
    plot_quantile_map(ds_t, var, short_title_min, short_title_max, short_title_ave, 
                     ul_title)
    
    # Time Series PLOT
    plot_yearly_series(separate_city_data, var = var, coordinate_pairs=coordinate_pairs,
                   short_title_min=short_title_min, short_title_max=short_title_max, short_title_ave=short_title_ave,
                   ylabel = 'Temperature (degC)',
                   ultitle = ul_title)
    
    
    print(f'exitted Plotting: {var}')
    
    # d
    var = 'd'
    short_title_max = '2m  Maximum Dewpoint Temperature (degC)'
    short_title_min = '2m  Minimum Dewpoint Temperature (degC)'
    short_title_ave = '2m  Average Dewpoint Temperature (degC)'
    
    # 2D MAP PLOT
    plot_quantile_map(ds_d, var, short_title_min, short_title_max, short_title_ave, 
                     ul_title)
    
    # Time Series PLOT
    plot_yearly_series(separate_city_data, var = var, coordinate_pairs=coordinate_pairs,
                   short_title_min=short_title_min, short_title_max=short_title_max, short_title_ave=short_title_ave,
                   ylabel = 'Dewpoint Temperature (degC)',
                   ultitle = ul_title)
    
    print(f'exitted Plotting: {var}')
    
    # p
    var = 'p'
    short_title_max = 'Maximum Mean Sea Level Pressure (mb)'
    short_title_min = 'Minimum Mean Sea Level Pressure (mb)'
    short_title_ave = 'Average Mean Sea Level Pressure (mb)'
    
    # 2D MAP PLOT
    plot_quantile_map(ds_p, var, short_title_min, short_title_max, short_title_ave, 
                     ul_title)
    
    # Time Series PLOT
    plot_yearly_series(separate_city_data, var = var, coordinate_pairs=coordinate_pairs,
                   short_title_min=short_title_min, short_title_max=short_title_max, short_title_ave=short_title_ave,
                   ylabel = 'Mean Sea Level Pressure (mb)',
                   ultitle = ul_title)
    
    print(f'exitted Plotting: {var}')
    
    ## TIME SERIES MAP *******************************************
    
    # change 0 to 1 in corresponding plot's [done] column (means the plot is completed in plotting)
    DateList[count, 3] = 1
    np.save(r'C:\Users\USER\JupyterLab\Climaturk_Site\GITHUB\version_17_05_2021\Climaturk-Base\src/DateList_Quantile_10042021', DateList)
    print('Plot Done: ', str(DateList[count, 0]))
    
    