# Information of metadata for file reading, and maybe for saving data?
from collections import namedtuple

FIELDS = (
    'long_name',
    'units',
    'comment',
    'standard_name',
    'axis',
    'positive')

MetaData = namedtuple('MetaData', FIELDS)
MetaData.__new__.__defaults__ = (None,) * len(MetaData._fields)


MODEL_ATTRIBUTES = {
    'time': MetaData(
        long_name='Time UTC',
        comment='Starting time of control run + cycle.',
        axis='T',
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
        comment='Level 1 describes the highest height from ground.',
        axis='Z',
        positive='down'
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
        comment='Height have been calculated using pressure, temperature and specific humidity.',
        positive='up'
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
        comment='With respect to liquid above 0 degrees C and with respect to ice below 0 degrees C'
    )
}

MODEL_L3_ATTRIBUTES = {
    'cf': MetaData(
        long_name='Cloud fraction of model grid point',
        units='1'
    ),
    'cf_cirrus': MetaData(
            long_name='Cloud fraction of model grid point with filtered cirrus fraction',
            units='1',
            comment='High level cirrus fraction is reduce do to lack if a radar capability to observe '
                    'correctly particles small and high.'
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

REGRID_PRODUCT_ATTRIBUTES = {
    'cf_V': MetaData(
        long_name='Observed cloud fraction by volume',
        units='1',
        comment="Cloud fraction generated from observations and regenerated "
                "to fit model grid by averaging to grid volume."
    ),
    'cf_A': MetaData(
        long_name='Observed cloud fraction by area',
        units='1',
        comment="Cloud fraction generated from observation and regenerated "
                "to fit model grid by averaging to grid time column area."
    ),
    'cf_V_adv': MetaData(
        long_name='Observed cloud fraction by advection volume',
        units='1',
        comment="Cloud fraction generated from observation and regenerated "
                "to fit model grid by averaging to grid volume. "
                "Effect of advection is noticed while regenerate observation to model grid."
    ),
    'cf_A_adv': MetaData(
        long_name='Observed cloud fraction by advection area',
        units='1',
        comment="Cloud fraction generated from observation and regenerated "
                "to fit model grid by averaging to grid time column area. "
                "Effect of advection is noticed while regenerate observation to model grid."
    ),
    'iwc': MetaData(
        long_name='Observed ice water content reshaped to model dimensions by averaging',
        units='kg m-3',
        comment='Read from iwc-file produce with CloudnetPy.'
    ),
    'iwc_mask': MetaData(
        long_name='Observed and masked ice water content reshaped to model grid by averaging',
        units='kg m-3',
        comment='Read from iwc-file  produce with CloudnetPy, but bits other than retrieval status of '
                'Reliable retrieval and Uncorrected liquid attenuation is masked away.'
    ),
    'iwc_att': MetaData(
        long_name='Observed ice water content with attenuation reshaped to model grid by averaging',
        units='kg m-3',
        comment='Read from iwc-file produce with CloudnetPy. By Masking data bit from retrieval status with '
                'attenuation is remain.'
    ),
    'iwc_rain': MetaData(
        long_name='Observed ice water content with raining reshaped to model grid by averaging',
        units='kg m-3',
        comment='Read from iwc-file produce with CloudnetPy.'
    ),
    'iwc_adv': MetaData(
        long_name='Observed ice water content reshaped to model advection grid by averaging',
        units='kg m-3',
        comment='Read from iwc-file produce with CloudnetPy. Regriding produce take notice of '
                'mass advection cross grid area.'
    ),
    'iwc_mask_adv': MetaData(
        long_name='Observed and masked ice water content reshaped to model advection grid by averaging',
        units='kg m-3',
        comment='Read from iwc-file  produce with CloudnetPy, but bits other than retrieval status of '
                'Reliable retrieval and Uncorrected liquid attenuation is masked away. '
                'Regriding produce take notice of mass advection cross grid area.'
    ),
    'iwc_att_adv': MetaData(
        long_name='Observed ice water content with attenuation reshaped to model advection grid by averaging',
        units='kg m-3',
        comment='Read from iwc-file produce with CloudnetPy. By Masking data bit from retrieval status with '
                'attenuation is remain. Regriding produce take notice of '
                'mass advection cross grid area.'
    ),
    'iwc_rain_adv': MetaData(
        long_name='Observed ice water content with raining reshaped to model advection grid by averaging',
        units='kg m-3',
        comment='Read from iwc-file produce with CloudnetPy. Rain below clouds is not masked away. '
                'Regriding produce take notice of mass advection cross grid area.'
    ),
    'lwc': MetaData(
        long_name='Observed liquid water content reshaped to model grid by averaging',
        units='kg m-3',
        comment='Read from lwc-file produce with CloudnetPy. Rain below clouds is not masked away.'
    ),
    'lwc_adv': MetaData(
        long_name='Observed liquid water content reshaped to model advection grid by averaging',
        units='kg m-3',
        comment='Read from lwc-file produce with CloudnetPy.  Regriding produce take notice of '
                'mass advection cross grid area.'
    )
}
