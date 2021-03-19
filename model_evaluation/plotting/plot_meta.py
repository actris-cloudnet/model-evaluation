""" Initialization info of variable visualization """
"""Metadata for plotting module."""
from collections import namedtuple

FIELDS = ('name',
          'cbar',
          'clabel',
          'ylabel',
          'plot_range',
          'plot_scale',
<<<<<<< HEAD
          'plot_type')
=======
          'plot_type',
          'hist_bin',
          'hist_limits',
<<<<<<< HEAD
<<<<<<< HEAD
          'hist_x_title')
>>>>>>> fed6cde... Fix histogram bins for plot
=======
          'x_title')
>>>>>>> 26c037e... All statistic visualizations done
=======
          'hist_bin_vertical',
          'hist_x_title')
>>>>>>> b1591f2... Adds Statistical plotting

PlotMeta = namedtuple('PlotMeta', FIELDS)
PlotMeta.__new__.__defaults__ = (None,) * len(FIELDS)

_LOG = 'logarithmic'
_LIN = 'linear'

_M3 = '$m^{-3}$'
_MS1 = 'm s$^{-1}$'
_SR1M1 = 'sr$^{-1}$ m$^{-1}$'
_KGM2 = 'kg m$^{-2}$'
_KGM3 = 'kg m$^{-3}$'
_KGM2S1 = 'kg m$^{-2}$ s$^{-1}$'


ATTRIBUTES = {
    'drizzle_N': PlotMeta(
        name='Drizzle number concentration',
        cbar='viridis',
        clabel=_M3,
        plot_range=(1e4, 1e9),
        plot_scale=_LIN,
        plot_type='mesh'
    ),
    'v_air': PlotMeta(
        name='Vertical air velocity',
        cbar='RdBu_r',
        clabel=_MS1,
        plot_range=(-2, 2),
        plot_scale=_LIN,
        plot_type='mesh'
    ),
    'uwind': PlotMeta(
        name='Model zonal wind',
        cbar='RdBu_r',
        clabel=_MS1,
        plot_range=(-50, 50),
        plot_scale=_LIN,
        plot_type='model'
    ),
    'vwind': PlotMeta(
        name='Model meridional wind',
        cbar='RdBu_r',
        clabel=_MS1,
        plot_range=(-50, 50),
        plot_scale=_LIN,
        plot_type='model'
    ),
    'temperature': PlotMeta(
        name='Model temperature',
        cbar='RdBu_r',
        clabel='K',
        plot_range=(223.15, 323.15),
        plot_scale=_LIN,
        plot_type='model'
    ),
    'cf': PlotMeta(
        name='Cloud fraction',
        cbar='Blues',
        clabel='',
        plot_range=(0, 1),
        plot_scale=_LIN,
        plot_type='model'
    ),
    'specific_humidity': PlotMeta(
        name='Model specific humidity',
        cbar='viridis',
        clabel='',
        plot_range=(1e-5, 1e-2),
        plot_scale=_LIN,
        plot_type='model'
    ),
    'q': PlotMeta(
        name='Model specific humidity',
        cbar='viridis',
        clabel='',
        plot_range=(1e-5, 1e-2),
        plot_scale=_LIN,
        plot_type='model'
    ),
    'pressure': PlotMeta(
        name='Model pressure',
        cbar='viridis',
        clabel='Pa',
        plot_range=(1e4, 1.5e5),
        plot_scale=_LIN,
        plot_type='model'
    ),
    'v': PlotMeta(
        name='Doppler velocity',
        cbar='RdBu_r',
        clabel=_MS1,
        plot_range=(-4, 4),
        plot_scale=_LIN,
        plot_type='mesh'
     ),
    'lwp': PlotMeta(
        name='Liquid water path',
        cbar='Blues',
        ylabel=_KGM2,
        plot_range=(0, 1),
        plot_scale=_LIN,
        plot_type='bar'
    ),
<<<<<<< HEAD
=======
    'cf': PlotMeta(
        name='Cloud fraction',
        cbar='Blues',
        clabel='',
        plot_range=(0, 1),
        plot_scale=_LIN,
        plot_type='model',
        hist_bin=10,
        hist_limits=(0.0, 1.1, 0.1),
        hist_bin_vertical=12,
        hist_x_title=''
    ),
>>>>>>> fed6cde... Fix histogram bins for plot
    'iwc': PlotMeta(
        name='Ice water content',
        cbar='viridis',
        clabel=_KGM3,
        plot_range=(1e-7, 1e-3),
        plot_scale=_LOG,
<<<<<<< HEAD
        plot_type='mesh'
=======
        plot_type='mesh',
        hist_bin=11,
        hist_limits=(0.0, 3.4e-5, 0.3e-5),
<<<<<<< HEAD
<<<<<<< HEAD
        hist_x_title='g/kg'
>>>>>>> fed6cde... Fix histogram bins for plot
=======
        x_title='g/kg'
>>>>>>> 26c037e... All statistic visualizations done
=======
        hist_bin_vertical=12,
        hist_x_title='g/kg'
>>>>>>> b1591f2... Adds Statistical plotting
    ),
    'lwc': PlotMeta(
        name='Liquid water content',
        cbar='Blues',
        clabel=_KGM3,
        plot_range=(1e-5, 1e-2),
        plot_scale=_LOG,
<<<<<<< HEAD
        plot_type='mesh'
=======
        plot_type='mesh',
        hist_bin=10,
        hist_limits=(0.0, 3.4e-5, 0.3e-5),
<<<<<<< HEAD
<<<<<<< HEAD
        hist_x_title='g/kg'
>>>>>>> fed6cde... Fix histogram bins for plot
=======
        x_title='g/kg'
>>>>>>> 26c037e... All statistic visualizations done
=======
        hist_bin_vertical=12,
        hist_x_title='g/kg'
>>>>>>> b1591f2... Adds Statistical plotting
    )
}
