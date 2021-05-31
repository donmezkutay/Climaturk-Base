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

class Compact_plot():
    
    def __init__(self, pressure_data, single_data, dates):
        self.pressure_data = pressure_data
        self.single_data = single_data
        self.dates = dates
        #self.dates_s = dates_s
        
        # get variables
        start_compute = datetime.now()
        self.data_u_press  = np.multiply(self.pressure_data['u'], 1.94384449) # knot
        self.data_v_press  = np.multiply(self.pressure_data['v'], 1.94384449) # knot
        self.data_z_press  = np.divide(self.pressure_data['z'], sc.g) # metres
        self.data_q_press  = self.pressure_data['q'] # g/kg
        self.data_w_press  = np.multiply(self.pressure_data['w'], 36) # mb/hr
        self.data_vo_press = np.multiply(self.pressure_data['vo'], 1e+5) # 1e+5*s-1
        self.data_t_press  = np.subtract(self.pressure_data['t'], 273.15) # Celsius

        #Proper Units for single level data
        self.data_2t_single   = np.subtract(self.single_data['t2m'], 273.15) # Celsius
        self.data_2d_single   = np.subtract(self.single_data['d2m'], 273.15) # Celsius
        self.data_msl_single  = np.divide(self.single_data['msl'], 100) # mb
        self.data_cape_single = self.single_data['cape'] # J/Kg
        self.data_10u_single  = np.multiply(self.single_data['u10'], 1.94384449) # knot
        self.data_10v_single  = np.multiply(self.single_data['v10'], 1.94384449) # knot
        self.data_cape_single = xr.where(self.data_cape_single<0, 0, self.data_cape_single)
        self.mslp_smooth = gaussian_filter(self.data_msl_single, sigma=1)
        end_compute = datetime.now()
        print('Data Unit Handled.. -->', end_compute - start_compute)
        
        self.lon = self.data_vo_press['longitude']
        self.lat = self.data_vo_press['latitude']
        
    def ax_loop_parameters(self, ax, i):
        
        year_of = str(self.data_vo_press.sel(level=500)[::2]['time'][i].values)[:13]
        ax.set_title("Valid: {}".format(year_of), fontsize=12, loc = 'left', weight='heavy',style='italic',)
        ax.set_title(None, fontsize=12, loc = 'center')

        ax.set_extent([25, 46, 35, 43])
        ax.set_aspect('equal')
        ax.tick_params(
            axis='both',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,
            left = False,
            right = False,# ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            labelbottom=False,
            labelleft = False) # labels along the bottom edge are off

        ax.set_xlabel(xlabel = None)
        ax.set_ylabel(ylabel = None)
        
    
    def ax_title(self, ax, i):
        # set title climaturk
        if i == 1:
            title_climaturk = ax.set_title("Climaturk", fontsize=15, loc = 'right', color='white', style='italic',
                                          fontname = 'Constantia')
            title_climaturk.set_path_effects([PathEffects.withStroke(linewidth=2, foreground='k')])


    def Compact_500mb_vort_height(self, ):

        #get cmap
        cmap = plot.Colormap('Blue6',
            'Green1_r', 'Orange5',
            ratios=(50, 20, 30), name='SciVisColor', )

        g = self.data_vo_press.sel(level=500)[::2].plot.contourf(x="longitude", y="latitude", col="time", col_wrap=2, 
                           cmap = cmap, robust=True, 
                           levels = np.arange(-50, 51, 0.5,),
                            aspect=77/60,
                            subplot_kws = {'projection':cartopy.crs.Mercator()},
                               transform=ccrs.PlateCarree(),

                            cbar_kwargs={
                                        "orientation": "horizontal",
                                        "shrink": 0.8,
                                        "aspect": 40,
                                        "pad": 0.01,
                                        "ticks": np.arange(-50, 51, 5),
                                        "label": 'ERA-5 Reanalysis | 500 hPa REL. VORT.(1e-5/s) | GEO. HEIGHT(m)',
                                         },)
        
        for i, ax in enumerate(g.axes.flat):
            
            # ax common parameters
            self.ax_loop_parameters(ax, i)
            
            # ax non-common parameters
            ax.add_feature(cartopy.feature.BORDERS, linewidth = 2, color='red')
            ax.add_feature(cartopy.feature.COASTLINE, linewidth = 2, color='red')
            
            #contourplot
            mesh = ax.contour(self.lon, self.lat, self.data_z_press.sel(level=500)[::2][i,:,:], np.arange(4680, 6121,20),
                       colors='white', linewidths=0.8, 
                       transform=cartopy.crs.PlateCarree(), zorder=6,
                                          linestyles='solid')
            ax.clabel(mesh, fontsize=12, inline=1, inline_spacing=7, fmt='%i', rightside_up=True, use_clabeltext=True , zorder=5)
            
            self.ax_title(ax, i)
            
            #save figure
        plt.savefig(r'D:\JupyterLab\Climaturk_Site\Docs\STORMS\{}\500mb_vort_height.jpeg'.format(self.dates, ),
                        bbox_inches='tight', optimize=True, progressive=True, dpi=150,
                        )
        plt.close()
    def Compact_850mb_temp_height(self, ):
        
        #get cmap
        cmap = plot.Colormap(
            'PuRd_r', 'Blue3' , 'Green1_r', 'Orange5', 'Purples_r',
            ratios=(10/65, 10/65, 15/65, 15/65, 15/65), name='SciVisColor', )
        
        g = self.data_t_press.sel(level=850)[::2].plot.contourf(x="longitude", y="latitude", col="time", col_wrap=2, 
                       cmap = cmap, robust=True, 
                       levels = np.arange(-20, 46, 1,),
                        aspect=77/60,
                        subplot_kws = {'projection':cartopy.crs.Mercator()},
                           transform=ccrs.PlateCarree(),
                           
                        cbar_kwargs={
                                    "orientation": "horizontal",
                                    "shrink": 0.8,
                                    "aspect": 40,
                                    "pad": 0.01,
                                    "ticks": np.arange(-20, 46, 2),
                                    "label": 'ERA-5 | 850 hPa TEMPERATURE(C) | GEO. HEIGHT(m) | WIND BARBS',
                                     },)
        
        for i, ax in enumerate(g.axes.flat):
            
            # ax common parameters
            self.ax_loop_parameters(ax, i)
            
            ax.add_feature(cartopy.feature.BORDERS, linewidth = 2,)
            ax.add_feature(cartopy.feature.COASTLINE, linewidth = 2,)
            
            #contourplot
            mesh = ax.contour(self.lon, self.lat, self.data_z_press.sel(level=850)[i,:,:], np.arange(1300, 1601,10,),
                       colors='k', linewidths=0.8, 
                       transform=cartopy.crs.PlateCarree(), zorder=6,
                                          linestyles='solid')
            ax.clabel(mesh, fontsize=12, inline=1, inline_spacing=7, fmt='%i', rightside_up=True, use_clabeltext=True , zorder=5)


            #windbarbs
            ax.barbs(self.lon, self.lat, self.data_u_press.sel(level=850)[i].values, self.data_v_press.sel(level=850)[i].values, length=5,
                 regrid_shape=10, transform=cartopy.crs.PlateCarree(), zorder=30)
            
            self.ax_title(ax, i)
            
            
        #save figure
        plt.savefig(r'D:\JupyterLab\Climaturk_Site\Docs\STORMS\{}\850mb_temp_height.jpeg'.format(self.dates, ),
                        bbox_inches='tight', optimize=True, progressive=True, dpi=150,
                        )
        plt.close()
    def Compact_700mb_vvel_streamlines(self, ):
        
        #get cmap
        cmap = plot.Colormap(
            'vik',
             name='SciVisColor', )
        
        g = self.data_w_press.sel(level=700)[::2].plot.contourf(x="longitude", y="latitude", col="time", col_wrap=2, 
                       cmap = cmap, robust=True, 
                       levels = np.arange(-150, 151, 5,),
                        aspect=77/60,
                        subplot_kws = {'projection':cartopy.crs.Mercator()},
                           transform=ccrs.PlateCarree(),
                           
                        cbar_kwargs={
                                    "orientation": "horizontal",
                                    "shrink": 0.8,
                                    "aspect": 40,
                                    "pad": 0.01,
                                    "ticks": np.arange(-150,151,10),
                                    "label": 'ERA-5 | 700 hPa VERT. VELOCITY(mb/hr) | STREAMLINES',
                                     },)
        
        for i, ax in enumerate(g.axes.flat):
            
            # ax common parameters
            self.ax_loop_parameters(ax, i)
            
            ax.add_feature(cartopy.feature.BORDERS, linewidth = 2, color='red')
            ax.add_feature(cartopy.feature.COASTLINE, linewidth = 2, color='red')
            
            #streamlines
            ax.streamplot(self.lon, self.lat, self.data_u_press.sel(level=700)[i].values, self.data_v_press.sel(level=700)[i].values,
                  color='k', linewidth=0.5, 
                  density=1.2, arrowsize=2, transform=cartopy.crs.PlateCarree() )
            
            self.ax_title(ax, i)
            
         #save figure
        plt.savefig(r'D:\JupyterLab\Climaturk_Site\Docs\STORMS\{}\700mb_vvel_streamline.jpeg'.format(self.dates, ),
            bbox_inches='tight', optimize=True, progressive=True, dpi=150,
            )
        plt.close()
    def Compact_250mb_wind_streamlines(self, ):
        
        #get cmap
        cmap = plot.Colormap('Blue2','Green5_r',
            'Orange5', 'RedPurple6_r', 'Brown1',
            ratios=(65/260, 37.5/260, 37.5/260, 60/260, 60/260), name='SciVisColor', save=True)
        
        u =  self.data_u_press.sel(level=250)
        v = self.data_v_press.sel(level=250)
        ww = np.sqrt(u**2 + v**2)
        
        g = ww[::2].plot.contourf(x="longitude", y="latitude", col="time", col_wrap=2, 
                       cmap = cmap, robust=True, 
                       levels = np.arange(0, 261, 5),
                        aspect=77/60,
                        subplot_kws = {'projection':cartopy.crs.Mercator()},
                           transform=ccrs.PlateCarree(),
                           
                        cbar_kwargs={
                                    "orientation": "horizontal",
                                    "shrink": 0.8,
                                    "aspect": 40,
                                    "pad": 0.01,
                                    "ticks": np.arange(0,261,10),
                                    "label": 'ERA-5 | 250 hPa WIND(knot) | STREAMLINES | MSLP(white)',
                                     },)
        
        for i, ax in enumerate(g.axes.flat):
            
            # ax common parameters
            self.ax_loop_parameters(ax, i)
            
            ax.add_feature(cartopy.feature.BORDERS, linewidth = 2, color='red')
            ax.add_feature(cartopy.feature.COASTLINE, linewidth = 2, color='red')
            
            #streamlines
            ax.streamplot(self.lon, self.lat, self.data_u_press.sel(level=250)[i].values, self.data_v_press.sel(level=250)[i].values,
                          color='k', linewidth=0.5, 
                          density=1.2, arrowsize=2, transform=cartopy.crs.PlateCarree() )

            #contourplot
            mesh = ax.contour(self.lon, self.lat, self.mslp_smooth[i,:,:], np.arange(920, 1060, 2, ),
                       colors='white', linewidths=1, 
                       transform=cartopy.crs.PlateCarree(), zorder=6,
                                          linestyles='solid')
            ax.clabel(mesh, fontsize=8, inline=1, inline_spacing=7, fmt='%i', rightside_up=True, use_clabeltext=True , zorder=5)
            
            self.ax_title(ax, i)
            
        #save figure
        plt.savefig(r'D:\JupyterLab\Climaturk_Site\Docs\STORMS\{}\250mb_wind_height.jpeg'.format(self.dates, ),
            bbox_inches='tight', optimize=True, progressive=True, dpi=200,
            ) 
        plt.close()
    def Compact_2m_temp_mslp(self, ):      
        
        #get cmap
        cmap = plot.Colormap(
            'PuRd_r', 'Blue3' ,'Green1_r','Orange5', 'Purples_r',
            ratios=(10/65, 10/65, 15/65, 15/65, 15/65), name='SciVisColor', )
        
        g = self.data_2t_single[::2].plot.contourf(x="longitude", y="latitude", col="time", col_wrap=2, 
                       cmap = cmap, robust=True, 
                       levels = np.arange(-20, 46, 1,),
                        aspect=77/60,
                        subplot_kws = {'projection':cartopy.crs.Mercator()},
                           transform=ccrs.PlateCarree(),
                           
                        cbar_kwargs={
                                    "orientation": "horizontal",
                                    "shrink": 0.8,
                                    "aspect": 40,
                                    "pad": 0.01,
                                    "ticks": np.arange(-20, 46, 2),
                                    "label": 'ERA-5 | 2M TEMPERATURE(C) | MSLP(hPa) | WIND BARBS',
                                     },)
        
        for i, ax in enumerate(g.axes.flat):
            
            # ax common parameters
            self.ax_loop_parameters(ax, i)
            
            ax.add_feature(cartopy.feature.BORDERS, linewidth = 2,)
            ax.add_feature(cartopy.feature.COASTLINE, linewidth = 2,)
            
            #contourplot
            mesh = ax.contour(self.lon, self.lat, self.mslp_smooth[i,:,:], np.arange(920, 1060, 2, ),
                       colors='white', linewidths=1, 
                       transform=cartopy.crs.PlateCarree(), zorder=6,
                                          linestyles='solid')
            ax.clabel(mesh, fontsize=8, inline=1, inline_spacing=7, fmt='%i', rightside_up=True, use_clabeltext=True , zorder=5)


            #windbarbs
            ax.barbs(self.lon, self.lat, self.data_10u_single[i].values, self.data_10v_single[i].values, length=5,
                 regrid_shape=10, transform=cartopy.crs.PlateCarree(), zorder=30)
            
            self.ax_title(ax, i)
            
            
        #save figure
        plt.savefig(r'D:\JupyterLab\Climaturk_Site\Docs\STORMS\{}\2mtemp_mslp.jpeg'.format(self.dates, ),
                    bbox_inches='tight', optimize=True, progressive=True, dpi=150,
                    )  
        plt.close()
    def Compact_2m_dew_mslp(self, ):  
        
        #get cmap
        cmap = plot.Colormap(
                'Brown7_r','Green2', 'Blue4', 'RedPurple6', 'RedPurple3', 'RedPurple5',
            ratios=(20/51, 10/51, 6/51, 5/51, 5/51, 5/51), name='SciVisColor', save=True)
        
        g = self.data_2d_single[::2].plot.contourf(x="longitude", y="latitude", col="time", col_wrap=2, 
                       cmap = cmap, robust=True, 
                       levels = np.arange(-20, 32.5, 0.5,),
                        aspect=77/60,
                        subplot_kws = {'projection':cartopy.crs.Mercator()},
                           transform=ccrs.PlateCarree(),
                           
                        cbar_kwargs={
                                    "orientation": "horizontal",
                                    "shrink": 0.8,
                                    "aspect": 40,
                                    "pad": 0.01,
                                    "ticks": np.arange(-20, 32.5, 2,),
                                    "label": 'ERA-5 | 2M DEWPOINT(C) | MSLP(hPa) | 10m WIND BARBS',
                                     },)
        
        for i, ax in enumerate(g.axes.flat):
            
            # ax common parameters
            self.ax_loop_parameters(ax, i)
            
            ax.add_feature(cartopy.feature.BORDERS, linewidth = 2, color='red')
            ax.add_feature(cartopy.feature.COASTLINE, linewidth = 2, color='red')
            
            #contourplot
            mesh = ax.contour(self.lon, self.lat, self.mslp_smooth[i,:,:], np.arange(920, 1060, 2, ),
                       colors='white', linewidths=1, 
                       transform=cartopy.crs.PlateCarree(), zorder=6,
                                          linestyles='solid')
            ax.clabel(mesh, fontsize=8, inline=1, inline_spacing=7, fmt='%i', rightside_up=True, use_clabeltext=True , zorder=5)


            #windbarbs
            ax.barbs(self.lon, self.lat, self.data_10u_single[i].values, self.data_10v_single[i].values, length=5,
                 regrid_shape=10, transform=cartopy.crs.PlateCarree(), zorder=30)
            
            self.ax_title(ax, i)
            
        #save figure
        plt.savefig(r'D:\JupyterLab\Climaturk_Site\Docs\STORMS\{}\dewpoint_2m.jpeg'.format(self.dates, ),
                    bbox_inches='tight', optimize=True, progressive=True, dpi=150,
                    )
        plt.close()
    def Compact_700mb_temp_height_spehum(self, ):  
        
        #get cmap
        cmap = plot.Colormap(
            'tokyo_r',
             name='SciVisColor', )
        
        temp_smooth = gaussian_filter(self.data_t_press.sel(level=700), sigma=1)
        
        g = (self.data_q_press.sel(level=700)[::2]*1000).plot.contourf(x="longitude", y="latitude", col="time", col_wrap=2, 
                       cmap = cmap, robust=True, 
                       levels = np.arange(0, 13.5, 0.5,),
                        aspect=77/60,
                        subplot_kws = {'projection':cartopy.crs.Mercator()},
                           transform=ccrs.PlateCarree(),
                           
                        cbar_kwargs={
                                    "orientation": "horizontal",
                                    "shrink": 0.8,
                                    "aspect": 40,
                                    "pad": 0.01,
                                    "ticks": np.arange(0, 13.5, 1),
                                    "label": 'ERA-5 | 700 hPa SPE.HUM.(g/kg) | TEMP.(blue,C) | GEO. HEIGHT(dam)',
                                     },)
        
        for i, ax in enumerate(g.axes.flat):
            
            # ax common parameters
            self.ax_loop_parameters(ax, i)
            
            ax.add_feature(cartopy.feature.BORDERS, linewidth = 2, color='red')
            ax.add_feature(cartopy.feature.COASTLINE, linewidth = 2, color='red')
            
            #contourplot
            mesh = ax.contour(self.lon, self.lat, self.data_z_press.sel(level=700)[i,:,:]/10, np.arange(250, 350, 2,),
                       colors='k', linewidths=0.8, 
                       transform=cartopy.crs.PlateCarree(), zorder=6,
                                          linestyles='solid')
            ax.clabel(mesh, fontsize=12, inline=1, inline_spacing=7, fmt='%i', rightside_up=True, use_clabeltext=True , zorder=5)

            #contourplot
            mesh = ax.contour(self.lon, self.lat, temp_smooth[i,:,:], np.arange(-60, 61, 2,),
                       colors='darkblue', linewidths=0.8, 
                       transform=cartopy.crs.PlateCarree(), zorder=6,
                                          linestyles='solid')
            ax.clabel(mesh, fontsize=12, inline=1, inline_spacing=7, fmt='%i', rightside_up=True, use_clabeltext=True , zorder=5)
            
            #windbarbs
            ax.barbs(self.lon, self.lat, self.data_u_press.sel(level=700)[i].values, self.data_v_press.sel(level=700)[i].values, length=5,
                 regrid_shape=10, transform=cartopy.crs.PlateCarree(), zorder=30, color='white')
            
            self.ax_title(ax, i)
            
        #save figure
        plt.savefig(r'D:\JupyterLab\Climaturk_Site\Docs\STORMS\{}\700mb_temp_spehum_height.jpeg'.format(self.dates, ),
                    bbox_inches='tight', optimize=True, progressive=True, dpi=150,
                    )
        plt.close()
    def Compact_cape_mslp_10mstreamlines(self, ):  
        
        #get cmap
        cmap = plot.Colormap(
            'oslo', 'acton_r' ,'bilbao_r','lajolla',
            ratios=(1000/6000, 1000/6000, 2000/6000, 2000/6000), name='SciVisColor', )
        
        g = self.data_cape_single[::2].plot.contourf(x="longitude", y="latitude", col="time", col_wrap=2, 
                       cmap = cmap, robust=True, 
                       levels = np.arange(0, 6001, 100,),
                        aspect=77/60,
                        subplot_kws = {'projection':cartopy.crs.Mercator()},
                           transform=ccrs.PlateCarree(),
                           
                        cbar_kwargs={
                                    "orientation": "horizontal",
                                    "shrink": 0.8,
                                    "aspect": 40,
                                    "pad": 0.01,
                                    "ticks": np.arange(0, 6001, 400,),
                                    "label": 'ERA-5 | CAPE(J/kg) | MSLP(hPa) | 10M WIND BARBS',
                                     },)
        
        for i, ax in enumerate(g.axes.flat):
            
            # ax common parameters
            self.ax_loop_parameters(ax, i)
            
            ax.add_feature(cartopy.feature.BORDERS, linewidth = 2, edgecolor='red')
            ax.add_feature(cartopy.feature.COASTLINE, linewidth = 2, edgecolor='red')
            
            #contourplot
            mesh = ax.contour(self.lon, self.lat, self.mslp_smooth[i,:,:], np.arange(920, 1060, 2, ),
                       colors='white', linewidths=1, 
                       transform=cartopy.crs.PlateCarree(), zorder=6,
                                          linestyles='solid')
            ax.clabel(mesh, fontsize=8, inline=1, inline_spacing=7, fmt='%i', rightside_up=True, use_clabeltext=True , zorder=5)


            #windbarbs
            ax.barbs(self.lon, self.lat, self.data_10u_single[i].values, self.data_10v_single[i].values, length=5,
                 regrid_shape=10, transform=cartopy.crs.PlateCarree(), zorder=30)
            
            self.ax_title(ax, i)
            
        #save figure
        plt.savefig(r'D:\JupyterLab\Climaturk_Site\Docs\STORMS\{}\cape_10mstreamlines.jpeg'.format(self.dates, ),
                    bbox_inches='tight', optimize=True, progressive=True, dpi=150,
                    )
        plt.close()