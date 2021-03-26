# Meta information of models and forecast cycles

from collections import namedtuple

FIELDS = (
    'model_name',
    'long_name',
    'cycle'
)

Model_metaData = namedtuple('Model_metaData', FIELDS)
Model_metaData.__new__.__defaults__ = (None,) * len(Model_metaData._fields)

MODELS = {
    'ecmwf': Model_metaData(
        model_name='ECMWF',
        long_name='European Centre for Medium-Range Weather Forecasts'
    ),
    'icon': Model_metaData(
        model_name='ICON-Iglo',
        long_name='Icosahedral Nonhydrostatic Model',
        cycle='12-23, 24-35, 36-47',
    ),
    'era5': Model_metaData(
        model_name='ERA5',
        long_name='Earth Re-Analysis System'
    )
}