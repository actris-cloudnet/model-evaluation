# Meta information of models and forecast cycles

from collections import namedtuple

FIELDS = (
    'long_name',
    'unit',
    'comment'
)

Model_metaData = namedtuple('Model_metaData', FIELDS)
Model_metaData.__new__.__defaults__ = (None,) * len(Model_metaData._fields)


MODEL_ATTRIBUTES = {
    'time': Model_metaData(
        long_name=''
    ),
    'forecast_time': Model_metaData(
        long_name=''
    ),
    'horizontal_resolution': Model_metaData(
        long_name=''
    ),
    'height': Model_metaData(
        long_name=''
    ),
    'uwind': Model_metaData(
        long_name=''
    ),
    'vwind': Model_metaData(
        long_name=''
    ),
    'wwind': Model_metaData(
        long_name=''
    ),
    'cloud_fraction': Model_metaData(
        long_name=''
    ),
    'temperature': Model_metaData(
        long_name=''
    ),
    'pressure': Model_metaData(
        long_name=''
    ),
    'ql': Model_metaData(
        long_name=''
    ),
    'qi': Model_metaData(
        long_name=''
    ),
    'gas_atten': Model_metaData(
        long_name=''
    ),
    'frequency': Model_metaData(
        long_name=''
    ),
    'flx_ls_snow': Model_metaData(
        long_name=''
    ),
    'qs': Model_metaData(
        long_name=''
    ),
    'qg': Model_metaData(
        long_name=''
    ),
    'omega': Model_metaData(
        long_name=''
    ),
    'flx_height': Model_metaData(
        long_name=''
    ),
    'sfc_pressure': Model_metaData(
        long_name=''
    )
}

