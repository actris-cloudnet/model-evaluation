# Meta information of models and forecast cycles

from collections import namedtuple

FIELDS = (
    'model_name',
    'long_name',
    'level',
    'cycle',
    'common_var',
    'cycle_var')

Model_metaData = namedtuple('Model_metaData', FIELDS)
Model_metaData.__new__.__defaults__ = (None,) * len(Model_metaData._fields)

MODELS = {
    'ecmwf': Model_metaData(
        model_name='ECMWF',
        long_name='European Centre for Medium-Range Weather Forecasts',
        level=88
    ),
    'icon': Model_metaData(
        model_name='ICON-Iglo',
        long_name='Icosahedral Nonhydrostatic Model',
        level=62,
        cycle='12-23, 24-35, 36-47'
    ),
    'era5': Model_metaData(
        model_name='ERA5',
        long_name='Earth Re-Analysis System',
        level=88,
        cycle='1-12, 7-18'
    ),
    'harmonie': Model_metaData(
        model_name='HARMONIE-AROME',
        long_name='the HIRLAM–ALADIN Research on Mesoscale Operational NWP in Euromed',
        level=65,
        cycle='6-11'
    )
}

VARIABLES = {
    'variables': Model_metaData(
        common_var='time, level, latitude, longitude, horizontal_resolution',
        cycle_var='forecast_time, height'
    ),
    'T': Model_metaData(
        long_name='temperature'
    ),
    'p': Model_metaData(
        long_name='pressure'
    ),
    'h': Model_metaData(
        long_name='height'
    ),
    'iwc': Model_metaData(
        long_name='qi'
    ),
    'lwc': Model_metaData(
        long_name='ql'
    ),
    'cf': Model_metaData(
        long_name='cloud_fraction'
    )
}
