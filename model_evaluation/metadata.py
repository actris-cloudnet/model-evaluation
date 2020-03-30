# Information of metadata for file reading, and maybe for saving data?
from collections import namedtuple

FIELDS = (
    'long_name',
    'units',
    'comment',
    'standard_name')

MetaData = namedtuple('MetaData', FIELDS)
MetaData.__new__.__defaults__ = (None,) * len(MetaData._fields)


MODEL_ATTRIBUTES = {
    'time': MetaData(
        long_name='Time UTC',
        units='decimal hours since midnight',
        comment='Starting time of control run + cycle'
    ),
    'latitude': MetaData(
        long_name='Latitude of grid point',
        units='dergee_North'
    ),
    'longitude': MetaData(
        long_name='Longitude of grid point',
        units='degree_East'
    ),
    'horizontal_resolution': MetaData(
        long_name='Horizontal resolution of model',
        units='km',
        comment='Distance between two grid point'
    ),
    'level': MetaData(
        long_name='Model level',
        units='1',
        comment='Level 1 describes the highest height from ground.'
    )
}

CYCLE_ATTRIBUTES = {
    'forecast_time': MetaData(
        long_name='Time since initialization of forecast',
        units='hours',
        comment='The time elapsed since the initialization time of the forecast from which it was taken. \n'
                'Note that the profiles in this file may be taken from more than one forecast.'
    ),
    'height': MetaData(
        long_name='Height above ground',
        units='m',
        comment='Height have been calculated using pressure, temperature and specific humidity.'
    ),
    'pressure': MetaData(
        long_name='Pressure',
        units='Pa'
    ),
    'temperature': MetaData(
        long_name='Temperature',
        units='K'
    ),
    'uwind': MetaData(
        long_name='Zonal wind',
        units='m s-1',
        standard_name='eastward_wind'
    ),
    'vwind': MetaData(
        long_name='Meridional wind',
        units='m s-1',
        standard_name='northward_wind'
    ),
    'wwind': MetaData(
        long_name='Vertical wind',
        units='m s-1',
        standard_name='upward_wind',
        comment='The vertical wind has been calculated from omega (Pa s-1),\n'
                ' height and pressure using: w=omega*dz/dp'
    ),
    'omega': MetaData(
        long_name='Vertical wind in pressure coordinates',
        units='PA s-1',
        standard_name='omega'
    ),
    'q': MetaData(
        long_name='Specific humidity',
        units='1'
    ),
    'rh': MetaData(
        long_name='Relative humidity',
        units='1',
        comment='With respect to liquid above 0 degrees C and with respect to ice below 0 degrees C.'
    )
}

L3_ATTRIBUTES = {
    'cv': MetaData(
        long_name='Cloud fraction of model grid point',
        units='1'
    ),
    'iwc': MetaData(
        long_name='Ice water content of model grid point',
        units='kg m-3',
        comment='Calculated using model ice water mixing ration, pressure and temperature: qi*P/287*T'

    ),
    'lwc': MetaData(
        long_name='Liquid water content of model grid point',
        units='kg m-3',
        comment='Calculated using model liquid water mixing ration, pressure and temperature: ql*P/287*T'
    )
}

PRODUCT_ATTRIBUTES = {
    'cv': MetaData(
        long_name='Cloud fraction reshaped to model dimensions by averaging',
        units='1',
        comment="Calculated using categorize-file with produce CloudnetPy"
    ),
    'iwc': MetaData(
        long_name='Ice water content reshaped to model dimensions by averaging',
        units='kg m-3',
        comment='Read from iwc-file  produce with CloudnetPy'

    ),
    'lwc': MetaData(
        long_name='Liquid water content reshaped to model dimensions by averaging',
        units='kg m-3',
        comment='Read from lwc-file produce with CloudnetPy'
    )
}