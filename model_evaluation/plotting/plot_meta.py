""" Initialization info of variable, maybe also plot type """
"""Metadata for plotting module."""
from collections import namedtuple

FIELDS = ('name',
          'cbar',
          'clabel',
          'ylabel',
          'plot_range',
          'plot_type')

PlotMeta = namedtuple('PlotMeta', FIELDS)
PlotMeta.__new__.__defaults__ = (None,) * len(FIELDS)

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
        plot_type='mesh'
    ),
    'v_air': PlotMeta(
        name='Vertical air velocity',
        cbar='RdBu_r',
        clabel=_MS1,
        plot_range=(-2, 2),
        plot_type='mesh'
    ),
    'uwind': PlotMeta(
        name='Model zonal wind',
        cbar='RdBu_r',
        clabel=_MS1,
        plot_range=(-50, 50),
        plot_type='model'
    ),
    'vwind': PlotMeta(
        name='Model meridional wind',
        cbar='RdBu_r',
        clabel=_MS1,
        plot_range=(-50, 50),
        plot_type='model'
    ),
    'temperature': PlotMeta(
        name='Model temperature',
        cbar='RdBu_r',
        clabel='K',
        plot_range=(223.15, 323.15),
        plot_type='model'
    ),
    'cloud_fraction': PlotMeta(
        name='Cloud fraction',
        cbar='Blues',
        clabel='',
        plot_range=(0, 1),
        plot_type='model'
    ),
    'specific_humidity': PlotMeta(
        name='Model specific humidity',
        cbar='viridis',
        clabel='',
        plot_range=(1e-5, 1e-2),
        plot_type='model'
    ),
    'q': PlotMeta(
        name='Model specific humidity',
        cbar='viridis',
        clabel='',
        plot_range=(1e-5, 1e-2),
        plot_type='model'
    ),
    'pressure': PlotMeta(
        name='Model pressure',
        cbar='viridis',
        clabel='Pa',
        plot_range=(1e4, 1.5e5),
        plot_type='model'
    ),
    'v': PlotMeta(
        name='Doppler velocity',
        cbar='RdBu_r',
        clabel=_MS1,
        plot_range=(-4, 4),
        plot_type='mesh'
     ),
    'lwp': PlotMeta(
        name='Liquid water path',
        cbar='Blues',
        ylabel=_KGM2,
        plot_range=(0, 1),
        plot_type='bar'
    ),
    'iwc': PlotMeta(
        name='Ice water content',
        cbar='viridis',
        clabel=_KGM3,
        plot_range=(1e-7, 1e-3),
        plot_type='mesh'
    ),
    'lwc': PlotMeta(
        name='Liquid water content',
        cbar='Blues',
        clabel=_KGM3,
        plot_range=(1e-5, 1e-2),
        plot_type='mesh'
    )
}