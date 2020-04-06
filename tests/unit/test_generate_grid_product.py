import numpy as np
import numpy.testing as testing
import pytest
from model_evaluation.products.generate_grid_product import ObservationManager
from model_evaluation.products.model_products import ModelGrid


MODEL = 'ecmwf'
OUTPUT_FILE = '/home/korpinen/Documents/ACTRIS/model_evaluation/test_data_ecmwf.nc'
PRODUCT = 'iwc'


class CategorizeBits:
    def __init__(self):
        self.category_bits = {'droplet': np.asarray([[1, 0, 1, 1, 1, 1],
                                                     [0, 1, 1, 1, 0, 0]], dtype=bool),
                              'falling': np.asarray([[0, 0, 0, 0, 1, 0],
                                                     [0, 0, 0, 1, 1, 1]], dtype=bool),
                              'cold': np.asarray([[0, 0, 1, 1, 0, 0],
                                                  [0, 1, 1, 1, 0, 1]], dtype=bool),
                              'melting': np.asarray([[1, 0, 1, 0, 0, 0],
                                                     [1, 1, 0, 0, 0, 0]], dtype=bool),
                              'aerosol': np.asarray([[1, 0, 1, 0, 0, 0],
                                                     [0, 0, 0, 0, 0, 0]], dtype=bool),
                              'insect': np.asarray([[1, 1, 0, 0, 0, 0],
                                                    [0, 0, 1, 0, 0, 0]], dtype=bool),
                              }
        self.quality_bits = {'radar': np.asarray([[0, 0, 0, 1, 1, 1],
                                                  [1, 0, 0, 1, 1, 1]], dtype=bool),
                             'lidar': np.asarray([[1, 1, 1, 1, 0, 0],
                                                  [1, 1, 0, 1, 1, 0]], dtype=bool),
                             'clutter': np.asarray([[0, 0, 1, 1, 0, 0],
                                                    [0, 0, 0, 0, 0, 0]], dtype=bool),
                             'molecular': np.asarray([[1, 0, 0, 1, 0, 0],
                                                      [0, 1, 0, 0, 0, 0]], dtype=bool),
                             'attenuated': np.asarray([[1, 1, 1, 0, 0, 1],
                                                       [0, 1, 1, 0, 0, 0]], dtype=bool),
                             'corrected': np.asarray([[1, 0, 0, 0, 0, 0],
                                                      [1, 1, 0, 0, 0, 0]], dtype=bool)}


def test_regridded_array(model_file, obs_file):
    from model_evaluation.products.generate_grid_product import regrid_array
    m_obj = ModelGrid(str(model_file), MODEL, OUTPUT_FILE, PRODUCT)
    m_obj.append_data(np.array([[1, 2], [3, 1], [2, 3]]), 'data')
    m_obj.keys['data'] = 'data'
    o_obj = ObservationManager('data', str(obs_file))
    regrid_array(o_obj, m_obj, MODEL, 'data')
    x = m_obj.data['data_obs_ecmwf'][:]
    compare = np.array([[3.5, 6.25], [4.5, 2], [4.5, 4]])
    testing.assert_array_almost_equal(compare, x)


def test_time2datetime():
    assert True


def test_get_date():
    assert True


def test_generate_product():
    assert True


def test_generate_cv():
    assert True


def test_get_rainrate_threshold():
    assert True


def test_rain_index():
    assert True
