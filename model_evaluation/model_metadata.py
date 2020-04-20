# Meta information of models and forecast cycles

from collections import namedtuple

FIELDS = (
    'long_name',
    'unit',
    'comment'
)

Model_metaData = namedtuple('Model_metaData', FIELDS)
Model_metaData.__new__.__defaults__ = (None,) * len(Model_metaData._fields)
