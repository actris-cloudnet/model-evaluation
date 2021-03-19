# Meta information of models and forecast cycles

from collections import namedtuple

FIELDS = (
    'long_name',
    'cycle'
)

Model_metaData = namedtuple('Model_metaData', FIELDS)
Model_metaData.__new__.__defaults__ = (None,) * len(Model_metaData._fields)

MODELS = {
    'ecmwf': Model_metaData(
        long_name='European central of mid-range weather forecast'
    ),
    'icon': Model_metaData(
        long_name='Icosahedral Nonhydrostatic model',
        cycle='12-23, 24-35, 36-47',
    ),
    'gdas1': Model_metaData(
        long_name='Global data assimilation system',
    )
}